#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
from collections import Counter, OrderedDict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote


DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_OUTPUT_DIR = "output"
CHUNK_CHAR_BUDGET = 40_000
DIRECT_PASS_CHAR_BUDGET = 20_000
CODE_BLOCK_CHAR_BUDGET = 4_000
SHORT_IMMUTABLE_TAGS = {"~#iR", "~#iM", "~#iL", "~#iS"}
TRANSIT_CACHE_BASE = 43
MAP_AS_ARRAY = "^ "
DEPENDENCY_PATTERN = re.compile(r"\{\{\s*(.*?)\s*\}\}", re.DOTALL)
RETRY_DELAY_PATTERN = re.compile(r"Please retry in ([0-9.]+)s", re.IGNORECASE)
MAX_429_RETRIES = 6
DEFAULT_429_DELAY_SECONDS = 30.0


class ConfigError(RuntimeError):
    pass


class ParseError(RuntimeError):
    pass


class GeminiError(RuntimeError):
    pass


class PdfError(RuntimeError):
    pass


class Gemini429Throttler:
    def __init__(self) -> None:
        self.min_interval_seconds = 0.0
        self.next_request_not_before = 0.0
        self.last_request_started_at = 0.0

    def wait_for_slot(self, label: str) -> None:
        target_time = max(
            self.next_request_not_before,
            self.last_request_started_at + self.min_interval_seconds,
        )
        sleep_seconds = target_time - time.monotonic()
        if sleep_seconds > 0:
            log(f"Throttling Gemini request before {label} for {sleep_seconds:.1f}s")
            time.sleep(sleep_seconds)

    def mark_request_start(self) -> None:
        self.last_request_started_at = time.monotonic()

    def apply_rate_limit(self, error: Any) -> tuple[float, int | None]:
        retry_delay = extract_retry_delay_seconds(error)
        quota_rpm = extract_quota_value(error)
        if quota_rpm and quota_rpm > 0:
            self.min_interval_seconds = max(
                self.min_interval_seconds, 60.0 / float(quota_rpm)
            )
        self.next_request_not_before = max(
            self.next_request_not_before, time.monotonic() + retry_delay
        )
        return retry_delay, quota_rpm


@dataclass
class AppConfig:
    input_path: Path
    prompt_path: Path
    output_dir: Path
    model: str = DEFAULT_MODEL
    gemini_api_key: str | None = None


class TransitTag:
    def __init__(self, tag: str) -> None:
        self.tag = tag


class RollingCache:
    def __init__(self) -> None:
        self._values: list[str] = []

    def encache(self, value: str) -> None:
        self._values.append(value)

    def decode(self, key: str) -> str:
        index = 0
        for char in key[1:]:
            index = (index * TRANSIT_CACHE_BASE) + (ord(char) - 48)
        try:
            return self._values[index]
        except IndexError as exc:
            raise ParseError(
                f"Retool Transit cache reference {key!r} could not be resolved."
            ) from exc


class TransitDecoder:
    def __init__(self) -> None:
        self.cache = RollingCache()

    def decode(self, node: Any, *, as_map_key: bool = False) -> Any:
        if isinstance(node, str):
            return self._decode_string(node, as_map_key=as_map_key)
        if isinstance(node, list):
            return self._decode_list(node, as_map_key=as_map_key)
        if isinstance(node, dict):
            output: OrderedDict[str, Any] = OrderedDict()
            for key, value in node.items():
                decoded_key = self.decode(key, as_map_key=True)
                decoded_value = self.decode(value, as_map_key=False)
                output[str(decoded_key)] = decoded_value
            return output
        return node

    def _decode_string(self, value: str, *, as_map_key: bool) -> Any:
        if self._is_cache_key(value):
            resolved = self.cache.decode(value)
            return self._parse_string(resolved, as_map_key=as_map_key)

        if self._is_cacheable(value, as_map_key=as_map_key):
            self.cache.encache(value)

        return self._parse_string(value, as_map_key=as_map_key)

    def _decode_list(self, node: list[Any], *, as_map_key: bool) -> Any:
        if not node:
            return []

        first = self.decode(node[0], as_map_key=as_map_key)

        if first == MAP_AS_ARRAY:
            output: OrderedDict[str, Any] = OrderedDict()
            for index in range(1, len(node), 2):
                decoded_key = self.decode(node[index], as_map_key=True)
                decoded_value = self.decode(node[index + 1], as_map_key=False)
                output[str(decoded_key)] = decoded_value
            return output

        if isinstance(first, TransitTag):
            rep = self.decode(node[1], as_map_key=False) if len(node) > 1 else None
            return self._decode_tag(first.tag, rep)

        return [self.decode(item, as_map_key=as_map_key) for item in node]

    def _parse_string(self, value: str, *, as_map_key: bool) -> Any:
        if not value.startswith("~") or len(value) < 2:
            return value

        marker = value[1]
        if marker == "#":
            return TransitTag(value[2:])
        if marker == "m":
            try:
                milliseconds = int(value[2:])
            except ValueError:
                return value
            return datetime.fromtimestamp(
                milliseconds / 1000, tz=timezone.utc
            ).isoformat()
        if marker in {"~", "^"}:
            return value[1:]
        return value

    def _decode_tag(self, tag: str, rep: Any) -> Any:
        if tag in {"iM", "iOM"}:
            if not isinstance(rep, list):
                return rep
            output: OrderedDict[str, Any] = OrderedDict()
            for index in range(0, len(rep), 2):
                output[str(rep[index])] = rep[index + 1]
            return output

        if tag in {"iL", "iS"}:
            return list(rep) if isinstance(rep, (list, tuple)) else rep

        if tag == "iR":
            if isinstance(rep, dict):
                return OrderedDict(
                    [
                        ("__record__", rep.get("n")),
                        ("value", rep.get("v")),
                    ]
                )
            return OrderedDict([("__record__", None), ("value", rep)])

        return OrderedDict([("__tag__", tag), ("rep", rep)])

    @staticmethod
    def _is_cache_key(value: str) -> bool:
        return len(value) > 1 and value.startswith("^") and value != MAP_AS_ARRAY

    @staticmethod
    def _is_cacheable(value: str, *, as_map_key: bool) -> bool:
        if len(value) < 4:
            return False
        if as_map_key:
            return True
        return value in SHORT_IMMUTABLE_TAGS or value.startswith("~$") or value.startswith("~:")


def log(message: str) -> None:
    print(f"[retool-docs] {message}")


def load_config(config_path: Path) -> AppConfig:
    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"Config file not found: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Config file is not valid JSON: {config_path}") from exc

    if not isinstance(raw, dict):
        raise ConfigError("Config file must contain a JSON object.")

    base_dir = config_path.parent
    input_path = resolve_relative_path(base_dir, raw.get("input_path"))
    prompt_path = resolve_relative_path(base_dir, raw.get("prompt_path"))
    output_dir = resolve_relative_path(base_dir, raw.get("output_dir", DEFAULT_OUTPUT_DIR))
    model = str(raw.get("model", DEFAULT_MODEL)).strip() or DEFAULT_MODEL
    gemini_api_key = str(raw.get("gemini_api_key", "")).strip() or None

    if input_path is None:
        raise ConfigError("Config is missing required field: input_path")
    if prompt_path is None:
        raise ConfigError("Config is missing required field: prompt_path")

    if not input_path.is_file():
        raise ConfigError(f"Retool export JSON was not found: {input_path}")
    if not prompt_path.is_file():
        raise ConfigError(f"Gemini prompt file was not found: {prompt_path}")

    return AppConfig(
        input_path=input_path,
        prompt_path=prompt_path,
        output_dir=output_dir,
        model=model,
        gemini_api_key=gemini_api_key,
    )


def resolve_relative_path(base_dir: Path, value: Any) -> Path | None:
    if value is None:
        return None
    path = Path(str(value))
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def resolve_gemini_api_key(config: AppConfig) -> str:
    api_key = config.gemini_api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ConfigError(
            "Gemini API key is missing. Set gemini_api_key in config.json or GEMINI_API_KEY in the environment."
        )
    return api_key


def load_retool_export(input_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        outer_data = json.loads(input_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ParseError(f"Retool export JSON was not found: {input_path}") from exc
    except json.JSONDecodeError as exc:
        raise ParseError(f"Retool export JSON is invalid: {input_path}") from exc

    try:
        app_state_raw = outer_data["page"]["data"]["appState"]
    except KeyError as exc:
        raise ParseError(
            "Retool export is missing page.data.appState."
        ) from exc

    if not isinstance(app_state_raw, str):
        raise ParseError("Retool page.data.appState must be a JSON string.")

    try:
        app_state_payload = json.loads(app_state_raw)
    except json.JSONDecodeError as exc:
        raise ParseError("Retool appState is not valid JSON.") from exc

    decoded_state = TransitDecoder().decode(app_state_payload)
    normalized_state = deep_unwrap_records(decoded_state)

    if not isinstance(normalized_state, dict):
        raise ParseError("Decoded Retool appState is not an object.")
    if not isinstance(normalized_state.get("plugins"), dict):
        raise ParseError("Decoded Retool appState does not contain a plugins map.")

    return outer_data, normalized_state


def deep_unwrap_records(node: Any) -> Any:
    if isinstance(node, dict):
        normalized = {normalize_key(key): deep_unwrap_records(value) for key, value in node.items()}
        if set(normalized.keys()) == {"__record__", "value"}:
            value = normalized["value"]
            if isinstance(value, dict):
                merged = dict(value)
                merged["__record__"] = normalized["__record__"]
                return merged
            return normalized
        return normalized
    if isinstance(node, list):
        return [deep_unwrap_records(item) for item in node]
    return node


def normalize_key(key: Any) -> str:
    if isinstance(key, str):
        return key
    return str(key)


def build_normalized_model(
    outer_data: dict[str, Any], app_state: dict[str, Any], input_path: Path
) -> dict[str, Any]:
    title = human_title_from_path(input_path)
    plugins_map = app_state.get("plugins", {})

    plugins: list[dict[str, Any]] = []
    for map_key, raw_plugin in plugins_map.items():
        if not isinstance(raw_plugin, dict):
            continue
        plugin = dict(raw_plugin)
        plugin.setdefault("id", map_key)
        plugin["map_key"] = map_key
        if not isinstance(plugin.get("template"), dict):
            plugin["template"] = {}
        plugin["dependencies"] = collect_dependencies(plugin)
        plugin["events"] = normalize_events(plugin["template"].get("events"))
        plugins.append(plugin)

    plugins.sort(key=lambda item: (str(item.get("folder") or ""), str(item.get("id") or "")))

    plugin_type_counts = dict(sorted(Counter(str(item.get("type") or "unknown") for item in plugins).items()))
    folder_counts = dict(
        sorted(
            Counter(str(item.get("folder") or "(root)") for item in plugins).items(),
            key=lambda item: (-item[1], item[0]),
        )
    )

    sql_queries = [
        summarize_sql_query(plugin)
        for plugin in plugins
        if is_sql_like_datasource(plugin)
    ]
    js_logic = [
        summarize_js_logic(plugin)
        for plugin in plugins
        if is_javascript_logic(plugin)
    ]
    widgets = [
        summarize_widget(plugin)
        for plugin in plugins
        if str(plugin.get("type")) == "widget"
    ]
    other_entities = [
        summarize_other_entity(plugin)
        for plugin in plugins
        if str(plugin.get("type")) not in {"widget"} and not is_sql_like_datasource(plugin) and not is_javascript_logic(plugin)
    ]

    page_data = outer_data.get("page", {})
    migrations = extract_migration_notes(page_data.get("changesRecordV2", []))

    return {
        "title": title,
        "source_file": str(input_path),
        "root_record": app_state.get("__record__"),
        "app_version": app_state.get("version"),
        "save_platform": app_state.get("savePlatform"),
        "root_screen": app_state.get("rootScreen"),
        "created_at": outer_data.get("createdAt") or page_data.get("createdAt") or app_state.get("createdAt"),
        "updated_at": outer_data.get("updatedAt") or page_data.get("updatedAt") or app_state.get("updatedAt"),
        "folders": list(app_state.get("folders", [])),
        "module_count": len(outer_data.get("modules", {})) if isinstance(outer_data.get("modules"), dict) else 0,
        "plugin_type_counts": plugin_type_counts,
        "folder_counts": folder_counts,
        "plugin_count": len(plugins),
        "migrations": migrations,
        "sql_queries": sql_queries,
        "js_logic": js_logic,
        "widgets": widgets,
        "other_entities": other_entities,
    }


def human_title_from_path(input_path: Path) -> str:
    decoded_name = unquote(input_path.name)
    return Path(decoded_name).stem


def safe_filename(name: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]+", "_", name).strip()
    return cleaned or "retool_documentation"


def extract_migration_notes(changes_record_v2: Any) -> list[str]:
    notes: list[str] = []
    if not isinstance(changes_record_v2, list):
        return notes
    for entry in changes_record_v2:
        if not isinstance(entry, dict):
            continue
        data = entry.get("data")
        if isinstance(data, dict):
            value = data.get("value")
            if value:
                notes.append(str(value))
    return notes


def is_sql_like_datasource(plugin: dict[str, Any]) -> bool:
    if str(plugin.get("type")) != "datasource":
        return False
    subtype = str(plugin.get("subtype") or "")
    if subtype == "JavascriptQuery":
        return False
    template = plugin.get("template", {})
    if not isinstance(template, dict):
        return False
    return bool(
        template.get("query")
        or template.get("actionType")
        or subtype == "SqlQueryUnified"
        or template.get("editorMode") == "sql"
    )


def is_javascript_logic(plugin: dict[str, Any]) -> bool:
    template = plugin.get("template", {})
    if not isinstance(template, dict):
        return False
    if str(plugin.get("type")) == "function":
        return bool(template.get("funcBody"))
    return str(plugin.get("subtype")) == "JavascriptQuery" or bool(template.get("funcBody"))


def summarize_sql_query(plugin: dict[str, Any]) -> dict[str, Any]:
    template = plugin.get("template", {})
    return {
        "id": plugin.get("id"),
        "folder": plugin.get("folder"),
        "subtype": plugin.get("subtype"),
        "resource_name": plugin.get("resourceName"),
        "resource_display_name": plugin.get("resourceDisplayName"),
        "editor_mode": template.get("editorMode"),
        "action_type": template.get("actionType"),
        "table_name": template.get("tableName"),
        "run_when_page_loads": template.get("runWhenPageLoads"),
        "query_disabled": template.get("queryDisabled"),
        "success_message": template.get("successMessage"),
        "query": compact_text(template.get("query"), CODE_BLOCK_CHAR_BUDGET),
        "transformer": compact_text(template.get("transformer"), CODE_BLOCK_CHAR_BUDGET),
        "error_transformer": compact_text(template.get("errorTransformer"), CODE_BLOCK_CHAR_BUDGET),
        "dependencies": plugin.get("dependencies", []),
        "events": plugin.get("events", []),
    }


def summarize_js_logic(plugin: dict[str, Any]) -> dict[str, Any]:
    template = plugin.get("template", {})
    code = template.get("funcBody") or template.get("query") or ""
    return {
        "id": plugin.get("id"),
        "folder": plugin.get("folder"),
        "type": plugin.get("type"),
        "subtype": plugin.get("subtype"),
        "run_when_page_loads": template.get("runWhenPageLoads"),
        "success_message": template.get("successMessage"),
        "code": compact_text(code, CODE_BLOCK_CHAR_BUDGET),
        "dependencies": plugin.get("dependencies", []),
        "events": plugin.get("events", []),
    }


def summarize_widget(plugin: dict[str, Any]) -> dict[str, Any]:
    template = plugin.get("template", {})
    return {
        "id": plugin.get("id"),
        "folder": plugin.get("folder"),
        "subtype": plugin.get("subtype"),
        "container": plugin.get("container"),
        "screen": plugin.get("screen"),
        "layout": summarize_layout(plugin.get("position2")),
        "interesting_props": extract_widget_props(template, plugin.get("subtype")),
        "dependencies": plugin.get("dependencies", []),
        "events": plugin.get("events", []),
    }


def summarize_other_entity(plugin: dict[str, Any]) -> dict[str, Any]:
    template = plugin.get("template", {})
    return {
        "id": plugin.get("id"),
        "folder": plugin.get("folder"),
        "type": plugin.get("type"),
        "subtype": plugin.get("subtype"),
        "details": extract_small_details(template),
        "dependencies": plugin.get("dependencies", []),
        "events": plugin.get("events", []),
    }


def summarize_layout(position: Any) -> str | None:
    if not isinstance(position, dict):
        return None

    parts: list[str] = []
    if position.get("__record__"):
        parts.append(str(position["__record__"]))
    for key in ("type", "container", "subcontainer"):
        value = position.get(key)
        if value not in (None, ""):
            parts.append(f"{key}={value}")
    for key in ("row", "col", "height", "width"):
        value = position.get(key)
        if value not in (None, ""):
            parts.append(f"{key}={value}")
    return ", ".join(parts) if parts else None


def collect_dependencies(node: Any) -> list[str]:
    matches: set[str] = set()
    for text in iter_strings(node):
        for expression in DEPENDENCY_PATTERN.findall(text):
            cleaned = " ".join(expression.strip().split())
            if cleaned:
                matches.add(cleaned)
    return sorted(matches)


def iter_strings(node: Any) -> Iterable[str]:
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from iter_strings(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_strings(item)


def normalize_events(raw_events: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_events, list):
        return []

    events: list[dict[str, Any]] = []
    for event in raw_events:
        if not isinstance(event, dict):
            continue
        normalized: dict[str, Any] = {}
        for key in ("event", "type", "pluginId", "method", "targetId", "waitType", "waitMs", "id"):
            if event.get(key) not in (None, ""):
                normalized[key] = event.get(key)
        params = event.get("params")
        if isinstance(params, list) and params:
            normalized["params"] = params
        if normalized:
            events.append(normalized)
    return events


def extract_widget_props(template: dict[str, Any], subtype: Any) -> list[tuple[str, str]]:
    keys = [
        "text",
        "value",
        "label",
        "placeholder",
        "tooltipText",
        "hidden",
        "disabled",
        "defaultValue",
        "format",
        "data",
        "selectedItem",
        "src",
        "styleVariant",
    ]
    props: list[tuple[str, str]] = []
    for key in keys:
        if key not in template:
            continue
        rendered = render_small_value(template.get(key))
        if rendered is not None:
            props.append((key, rendered))

    columns = extract_widget_columns(template, subtype)
    if columns:
        props.append(("columns", ", ".join(columns[:20]) + (" ..." if len(columns) > 20 else "")))

    return props[:8]


def extract_widget_columns(template: dict[str, Any], subtype: Any) -> list[str]:
    subtype_text = str(subtype or "")
    if "TableWidget" not in subtype_text:
        return []

    column_label_map = template.get("_columnLabel")
    if isinstance(column_label_map, dict):
        labels = [str(value) for value in column_label_map.values() if value not in ("", None)]
        if labels:
            return labels

    header_names = template.get("columnHeaderNames")
    if isinstance(header_names, dict):
        labels = [str(value) for value in header_names.values() if value not in ("", None)]
        if labels:
            return labels

    column_type_properties = template.get("columnTypeProperties")
    if isinstance(column_type_properties, dict):
        return [str(key) for key in column_type_properties.keys()]

    return []


def extract_small_details(template: dict[str, Any]) -> list[tuple[str, str]]:
    details: list[tuple[str, str]] = []
    for key in ("value", "data", "hidden", "disabled", "label", "text"):
        if key not in template:
            continue
        rendered = render_small_value(template.get(key))
        if rendered is not None:
            details.append((key, rendered))
    return details[:6]


def render_small_value(value: Any, *, max_chars: int = 220) -> str | None:
    if value in (None, "", [], {}):
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return compact_inline(value, max_chars)
    if isinstance(value, list):
        preview = value[:4]
        return compact_inline(json.dumps(preview, ensure_ascii=False), max_chars)
    if isinstance(value, dict):
        preview = list(value.items())[:4]
        return compact_inline(json.dumps(dict(preview), ensure_ascii=False), max_chars)
    return compact_inline(str(value), max_chars)


def compact_text(value: Any, max_chars: int) -> str:
    text = str(value or "").strip()
    if len(text) <= max_chars:
        return text
    omitted = len(text) - max_chars
    return f"{text[:max_chars].rstrip()}\n\n-- truncated {omitted} characters --"


def compact_inline(text: str, max_chars: int) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max_chars - 3].rstrip() + "..."


def build_source_units(model: dict[str, Any]) -> list[str]:
    units: list[str] = [render_overview_unit(model)]

    for query in model["sql_queries"]:
        units.append(render_sql_query_unit(query))

    for item in model["js_logic"]:
        units.append(render_js_logic_unit(item))

    for widget in model["widgets"]:
        units.append(render_widget_unit(widget))

    if model["other_entities"]:
        units.append(render_other_entities_unit(model["other_entities"]))

    return units


def render_overview_unit(model: dict[str, Any]) -> str:
    lines = [
        "# App Overview",
        f"- Title: {model['title']}",
        f"- Source file: {model['source_file']}",
        f"- Root record: {model.get('root_record') or 'unknown'}",
        f"- Retool version: {model.get('app_version') or 'unknown'}",
        f"- Save platform: {model.get('save_platform') or 'unknown'}",
        f"- Created at: {model.get('created_at') or 'unknown'}",
        f"- Updated at: {model.get('updated_at') or 'unknown'}",
        f"- Root screen: {model.get('root_screen') or 'unknown'}",
        f"- Module count: {model.get('module_count', 0)}",
        f"- Total plugins/entities: {model['plugin_count']}",
        f"- Plugin type counts: {json.dumps(model['plugin_type_counts'], ensure_ascii=False)}",
        f"- Folder counts: {json.dumps(model['folder_counts'], ensure_ascii=False)}",
        f"- Folders: {', '.join(model['folders']) if model['folders'] else '(none)'}",
    ]
    if model["migrations"]:
        lines.append(f"- Migrations: {' | '.join(model['migrations'])}")
    return "\n".join(lines)


def render_sql_query_unit(query: dict[str, Any]) -> str:
    lines = [
        f"## SQL Query `{query['id']}`",
        f"- Folder: {query.get('folder') or '(root)'}",
        f"- Subtype: {query.get('subtype') or 'unknown'}",
        f"- Resource display name: {query.get('resource_display_name') or 'n/a'}",
        f"- Resource name: {query.get('resource_name') or 'n/a'}",
        f"- Editor mode: {query.get('editor_mode') or 'n/a'}",
        f"- Action type: {query.get('action_type') or 'n/a'}",
        f"- Table name: {query.get('table_name') or 'n/a'}",
        f"- Run when page loads: {query.get('run_when_page_loads')}",
        f"- Query disabled: {query.get('query_disabled') or 'n/a'}",
        f"- Dependencies: {format_dependencies(query.get('dependencies', []))}",
        f"- Events: {format_events(query.get('events', []))}",
    ]
    if query.get("success_message"):
        lines.append(f"- Success message: {compact_inline(str(query['success_message']), 180)}")
    if query.get("query"):
        lines.extend(["", "```sql", query["query"], "```"])
    if query.get("transformer"):
        lines.extend(["", "Transformer:", "```javascript", query["transformer"], "```"])
    if query.get("error_transformer"):
        lines.extend(["", "Error transformer:", "```javascript", query["error_transformer"], "```"])
    return "\n".join(lines)


def render_js_logic_unit(item: dict[str, Any]) -> str:
    lines = [
        f"## JavaScript Logic `{item['id']}`",
        f"- Folder: {item.get('folder') or '(root)'}",
        f"- Type: {item.get('type') or 'unknown'}",
        f"- Subtype: {item.get('subtype') or 'unknown'}",
        f"- Run when page loads: {item.get('run_when_page_loads')}",
        f"- Dependencies: {format_dependencies(item.get('dependencies', []))}",
        f"- Events: {format_events(item.get('events', []))}",
    ]
    if item.get("success_message"):
        lines.append(f"- Success message: {compact_inline(str(item['success_message']), 180)}")
    if item.get("code"):
        lines.extend(["", "```javascript", item["code"], "```"])
    return "\n".join(lines)


def render_widget_unit(widget: dict[str, Any]) -> str:
    lines = [
        f"## Widget `{widget['id']}`",
        f"- Folder: {widget.get('folder') or '(root)'}",
        f"- Subtype: {widget.get('subtype') or 'unknown'}",
        f"- Container: {widget.get('container') or '(none)'}",
        f"- Screen: {widget.get('screen') or '(none)'}",
        f"- Layout: {widget.get('layout') or 'n/a'}",
        f"- Dependencies: {format_dependencies(widget.get('dependencies', []))}",
        f"- Events: {format_events(widget.get('events', []))}",
    ]
    if widget.get("interesting_props"):
        lines.append("- Interesting props:")
        for key, value in widget["interesting_props"]:
            lines.append(f"  - {key}: {value}")
    return "\n".join(lines)


def render_other_entities_unit(entities: list[dict[str, Any]]) -> str:
    lines = ["# Other Entities"]
    for entity in entities:
        lines.append(f"## {entity.get('type')}/{entity.get('subtype')} `{entity.get('id')}`")
        lines.append(f"- Folder: {entity.get('folder') or '(root)'}")
        lines.append(f"- Dependencies: {format_dependencies(entity.get('dependencies', []))}")
        lines.append(f"- Events: {format_events(entity.get('events', []))}")
        if entity.get("details"):
            lines.append("- Details:")
            for key, value in entity["details"]:
                lines.append(f"  - {key}: {value}")
    return "\n".join(lines)


def format_dependencies(dependencies: list[str], *, limit: int = 12) -> str:
    if not dependencies:
        return "(none)"
    displayed = dependencies[:limit]
    suffix = " ..." if len(dependencies) > limit else ""
    return ", ".join(displayed) + suffix


def format_events(events: list[dict[str, Any]], *, limit: int = 4) -> str:
    if not events:
        return "(none)"
    parts: list[str] = []
    for event in events[:limit]:
        label = f"{event.get('event', 'unknown')} -> {event.get('type', 'unknown')}.{event.get('method', 'unknown')}"
        target = event.get("pluginId") or event.get("targetId")
        if target:
            label += f"({target})"
        parts.append(label)
    if len(events) > limit:
        parts.append("...")
    return "; ".join(parts)


def chunk_source_units(units: list[str], max_chars: int) -> list[str]:
    chunks: list[str] = []
    current_units: list[str] = []
    current_size = 0

    for unit in units:
        for piece in split_large_unit(unit, max_chars):
            piece_size = len(piece)
            if current_units and current_size + piece_size + 2 > max_chars:
                chunks.append("\n\n".join(current_units))
                current_units = []
                current_size = 0
            current_units.append(piece)
            current_size += piece_size + 2

    if current_units:
        chunks.append("\n\n".join(current_units))

    return chunks


def split_large_unit(unit: str, max_chars: int) -> list[str]:
    if len(unit) <= max_chars:
        return [unit]

    lines = unit.splitlines()
    if not lines:
        return [unit]

    header = lines[0]
    pieces: list[str] = []
    current = [header]
    current_size = len(header) + 1

    for line in lines[1:]:
        line_size = len(line) + 1
        if current and current_size + line_size > max_chars:
            pieces.append("\n".join(current))
            current = [f"{header} (continued)"]
            current_size = len(current[0]) + 1
        current.append(line)
        current_size += line_size

    if current:
        pieces.append("\n".join(current))

    return pieces


def build_metadata_brief(model: dict[str, Any]) -> str:
    metadata = {
        "title": model["title"],
        "plugin_count": model["plugin_count"],
        "plugin_type_counts": model["plugin_type_counts"],
        "folder_counts": model["folder_counts"],
        "folders": model["folders"],
        "app_version": model.get("app_version"),
        "save_platform": model.get("save_platform"),
    }
    return json.dumps(metadata, ensure_ascii=False, indent=2)


def generate_markdown_document(
    prompt_text: str,
    model_name: str,
    source_units: list[str],
    normalized_model: dict[str, Any],
    api_key: str,
) -> str:
    client, genai_types, genai_errors = build_gemini_client(api_key)
    generation_config = build_generation_config(genai_types)
    throttler = Gemini429Throttler()

    chunks = chunk_source_units(source_units, CHUNK_CHAR_BUDGET)
    if len(chunks) == 1 and len(chunks[0]) <= DIRECT_PASS_CHAR_BUDGET:
        log("Generating documentation in a single Gemini pass")
        request_text = build_final_request(
            prompt_text=prompt_text,
            metadata_brief=build_metadata_brief(normalized_model),
            source_material=chunks[0],
            source_label="source package",
        )
        response = generate_content_with_rate_limit_retry(
            client=client,
            genai_errors=genai_errors,
            throttler=throttler,
            model_name=model_name,
            contents=request_text,
            generation_config=generation_config,
            label="single-pass documentation generation",
        )
        return clean_markdown_response(extract_response_text(response))

    log(f"Generating documentation in two Gemini passes across {len(chunks)} chunks")
    chunk_summaries: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        log(f"Summarizing chunk {index}/{len(chunks)}")
        response = generate_content_with_rate_limit_retry(
            client=client,
            genai_errors=genai_errors,
            throttler=throttler,
            model_name=model_name,
            contents=build_chunk_summary_request(
                normalized_model["title"], chunk, index, len(chunks)
            ),
            generation_config=generation_config,
            label=f"chunk summary {index}/{len(chunks)}",
        )
        chunk_summaries.append(extract_response_text(response))

    final_source = "\n\n".join(
        f"## Chunk Summary {index}\n{summary.strip()}"
        for index, summary in enumerate(chunk_summaries, start=1)
    )
    response = generate_content_with_rate_limit_retry(
        client=client,
        genai_errors=genai_errors,
        throttler=throttler,
        model_name=model_name,
        contents=build_final_request(
            prompt_text=prompt_text,
            metadata_brief=build_metadata_brief(normalized_model),
            source_material=final_source,
            source_label="chunk summaries",
        ),
        generation_config=generation_config,
        label="final documentation synthesis",
    )
    return clean_markdown_response(extract_response_text(response))


def build_gemini_client(api_key: str) -> tuple[Any, Any, Any]:
    try:
        from google import genai
        from google.genai import errors
        from google.genai import types
    except ImportError as exc:
        raise GeminiError(
            "The google-genai package is not installed. Run `pip install -r requirements.txt`."
        ) from exc

    return genai.Client(api_key=api_key), types, errors


def build_generation_config(genai_types: Any) -> Any:
    kwargs: dict[str, Any] = {"temperature": 0.2}
    thinking_config_cls = getattr(genai_types, "ThinkingConfig", None)
    if thinking_config_cls is not None:
        kwargs["thinking_config"] = thinking_config_cls(thinking_budget=0)
    return genai_types.GenerateContentConfig(**kwargs)


def generate_content_with_rate_limit_retry(
    *,
    client: Any,
    genai_errors: Any,
    throttler: Gemini429Throttler,
    model_name: str,
    contents: str,
    generation_config: Any,
    label: str,
) -> Any:
    attempt = 0
    while True:
        throttler.wait_for_slot(label)
        throttler.mark_request_start()
        try:
            return client.models.generate_content(
                model=model_name,
                contents=contents,
                config=generation_config,
            )
        except genai_errors.ClientError as exc:
            if getattr(exc, "code", None) != 429:
                raise

            attempt += 1
            retry_delay, quota_rpm = throttler.apply_rate_limit(exc)
            quota_note = f"; observed quota {quota_rpm} RPM" if quota_rpm else ""

            if attempt > MAX_429_RETRIES:
                raise GeminiError(
                    f"Gemini hit repeated 429 rate limits during {label} even after waiting."
                ) from exc

            log(
                f"429 rate limit during {label}; retrying in {retry_delay:.1f}s "
                f"(attempt {attempt}/{MAX_429_RETRIES}{quota_note})"
            )


def extract_retry_delay_seconds(error: Any) -> float:
    error_root = extract_error_root(error)
    details = error_root.get("details")
    if isinstance(details, list):
        for item in details:
            if not isinstance(item, dict):
                continue
            if str(item.get("@type", "")).endswith("RetryInfo"):
                retry_delay = parse_duration_seconds(item.get("retryDelay"))
                if retry_delay is not None:
                    return retry_delay

    message = str(error_root.get("message") or getattr(error, "message", "") or "")
    match = RETRY_DELAY_PATTERN.search(message)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass

    return DEFAULT_429_DELAY_SECONDS


def extract_quota_value(error: Any) -> int | None:
    error_root = extract_error_root(error)
    details = error_root.get("details")
    if isinstance(details, list):
        for item in details:
            if not isinstance(item, dict):
                continue
            if not str(item.get("@type", "")).endswith("QuotaFailure"):
                continue
            violations = item.get("violations")
            if not isinstance(violations, list):
                continue
            for violation in violations:
                if not isinstance(violation, dict):
                    continue
                quota_value = violation.get("quotaValue")
                try:
                    if quota_value is not None:
                        return int(quota_value)
                except (TypeError, ValueError):
                    continue

    message = str(error_root.get("message") or getattr(error, "message", "") or "")
    message_match = re.search(r"limit:\s*([0-9]+)", message, re.IGNORECASE)
    if message_match:
        try:
            return int(message_match.group(1))
        except ValueError:
            return None

    return None


def parse_duration_seconds(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return None

    normalized = value.strip().lower()
    if normalized.endswith("s"):
        normalized = normalized[:-1]
    try:
        return float(normalized)
    except ValueError:
        return None


def extract_error_root(error: Any) -> dict[str, Any]:
    details = getattr(error, "details", None)
    if isinstance(details, dict):
        nested = details.get("error")
        if isinstance(nested, dict):
            return nested
        return details
    return {}


def build_chunk_summary_request(title: str, chunk: str, index: int, total: int) -> str:
    return f"""
You are summarizing extracted technical context from a Retool web app.
Do not invent missing details.
Return concise Markdown under these exact headings:

## Functional Areas
## Queries and Data Access
## JavaScript Logic
## Widgets and UX
## Dependencies and Risks

Guidance:
- Keep this factual and compressed.
- Mention concrete query IDs, logic IDs, widget IDs, and key dependencies when present.
- If something is unclear, say it is unclear rather than guessing.

Document title: {title}
Chunk: {index}/{total}

Source context:

{chunk}
""".strip()


def build_final_request(
    *,
    prompt_text: str,
    metadata_brief: str,
    source_material: str,
    source_label: str,
) -> str:
    return f"""
{prompt_text.strip()}

Use the following extracted material to write the final documentation.
Return Markdown only.

Metadata:
```json
{metadata_brief}
```

Extracted {source_label}:

{source_material}
""".strip()


def extract_response_text(response: Any) -> str:
    text = getattr(response, "text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()

    candidates = getattr(response, "candidates", None)
    if candidates:
        parts: list[str] = []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            if content is None:
                continue
            for part in getattr(content, "parts", []) or []:
                part_text = getattr(part, "text", None)
                if part_text:
                    parts.append(part_text)
        joined = "\n".join(parts).strip()
        if joined:
            return joined

    raise GeminiError("Gemini returned an empty response.")


def clean_markdown_response(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            return "\n".join(lines[1:-1]).strip()
    return stripped


def write_markdown(output_dir: Path, base_name: str, markdown_text: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = output_dir / f"{base_name}.md"
    markdown_path.write_text(markdown_text, encoding="utf-8")
    return markdown_path


def prompt_for_pdf_export() -> bool:
    try:
        choice = input("Export PDF? [y/N]: ").strip().lower()
    except EOFError:
        return False
    return choice in {"y", "yes"}


def write_pdf(markdown_path: Path, markdown_text: str, title: str) -> Path:
    try:
        import markdown as markdown_lib
    except ImportError as exc:
        raise PdfError(
            "The markdown package is not installed. Run `pip install -r requirements.txt`."
        ) from exc

    try:
        from xhtml2pdf import pisa
    except ImportError as exc:
        raise PdfError(
            "The xhtml2pdf package is not installed. Run `pip install -r requirements.txt`."
        ) from exc

    html_body = markdown_lib.markdown(
        markdown_text,
        extensions=["fenced_code", "tables", "sane_lists"],
        output_format="html5",
    )
    document_html = build_pdf_html(title, html_body)
    pdf_path = markdown_path.with_suffix(".pdf")

    with pdf_path.open("wb") as handle:
        result = pisa.CreatePDF(document_html, dest=handle)

    if getattr(result, "err", 0):
        raise PdfError(f"PDF generation failed for {pdf_path}.")

    return pdf_path


def build_pdf_html(title: str, body_html: str) -> str:
    escaped_title = html.escape(title)
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{escaped_title}</title>
  <style>
    body {{
      font-family: Helvetica, Arial, sans-serif;
      font-size: 11pt;
      color: #111827;
      line-height: 1.45;
      margin: 24px;
    }}
    h1, h2, h3, h4 {{
      color: #0f172a;
      margin-top: 18px;
      margin-bottom: 8px;
    }}
    p, li {{
      margin-bottom: 6px;
    }}
    code {{
      font-family: Courier, monospace;
      font-size: 9pt;
      background: #f3f4f6;
      padding: 1px 3px;
    }}
    pre {{
      font-family: Courier, monospace;
      font-size: 9pt;
      background: #f3f4f6;
      border: 1px solid #d1d5db;
      padding: 8px;
      white-space: pre-wrap;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0;
    }}
    th, td {{
      border: 1px solid #d1d5db;
      padding: 6px;
      vertical-align: top;
    }}
    th {{
      background: #f8fafc;
      text-align: left;
    }}
  </style>
</head>
<body>
{body_html}
</body>
</html>"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate Markdown documentation for a Retool export using Gemini."
    )
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to the JSON config file. Defaults to config.json",
    )
    args = parser.parse_args(argv)

    config_path = Path(args.config).resolve()

    try:
        log(f"Loading config: {config_path}")
        config = load_config(config_path)
        api_key = resolve_gemini_api_key(config)

        log(f"Loading prompt: {config.prompt_path}")
        prompt_text = config.prompt_path.read_text(encoding="utf-8")

        log(f"Parsing Retool export: {config.input_path}")
        outer_data, app_state = load_retool_export(config.input_path)

        log("Normalizing app structure")
        normalized_model = build_normalized_model(outer_data, app_state, config.input_path)
        source_units = build_source_units(normalized_model)

        log(f"Generating Markdown with Gemini model {config.model}")
        markdown_text = generate_markdown_document(
            prompt_text=prompt_text,
            model_name=config.model,
            source_units=source_units,
            normalized_model=normalized_model,
            api_key=api_key,
        )

        base_name = safe_filename(normalized_model["title"])
        markdown_path = write_markdown(config.output_dir, base_name, markdown_text)
        log(f"Markdown written: {markdown_path}")

        if prompt_for_pdf_export():
            pdf_path = write_pdf(markdown_path, markdown_text, normalized_model["title"])
            log(f"PDF written: {pdf_path}")
        else:
            log("PDF export skipped")

        return 0

    except (ConfigError, ParseError, GeminiError, PdfError) as exc:
        print(f"[retool-docs] ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
