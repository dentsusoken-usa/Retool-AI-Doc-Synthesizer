#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_MODEL = "gemini-2.5-flash-lite"
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_PROMPT_PATH = (
    Path(__file__).resolve().parent / "prompts" / "db_schema_prompt.md"
).resolve()
RETRY_DELAY_PATTERN = re.compile(r"Please retry in ([0-9.]+)s", re.IGNORECASE)
MAX_429_RETRIES = 6
DEFAULT_429_DELAY_SECONDS = 30.0
PROMPT_TOO_LARGE_PATTERNS = (
    "too many tokens",
    "too large",
    "context length",
    "prompt is too long",
    "input token count",
    "request size",
    "maximum context",
)


class ConfigError(RuntimeError):
    pass


class GeminiError(RuntimeError):
    pass


class PdfError(RuntimeError):
    pass


class DatabaseSchemaError(RuntimeError):
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
    host: str
    port: int
    user: str
    password: str
    database: str
    prompt_path: Path
    output_dir: Path
    model: str = DEFAULT_MODEL
    gemini_api_key: str | None = None
    include_tables: list[str] | None = None
    exclude_tables: list[str] | None = None


def log(message: str) -> None:
    print(f"[db-docs] {message}")


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
    prompt_path = resolve_relative_path(
        base_dir, raw.get("prompt_path", str(DEFAULT_PROMPT_PATH))
    )
    output_dir = resolve_relative_path(base_dir, raw.get("output_dir", DEFAULT_OUTPUT_DIR))
    model = str(raw.get("model", DEFAULT_MODEL)).strip() or DEFAULT_MODEL
    gemini_api_key = str(raw.get("gemini_api_key", "")).strip() or None

    host = require_non_empty_string(raw, "host")
    user = require_non_empty_string(raw, "user")
    password = require_non_empty_string(raw, "password")
    database = require_non_empty_string(raw, "database")
    port = parse_port(raw.get("port", 3306))
    include_tables = parse_optional_string_list(raw.get("include_tables"), "include_tables")
    exclude_tables = parse_optional_string_list(raw.get("exclude_tables"), "exclude_tables")

    if include_tables and exclude_tables:
        overlap = sorted(set(include_tables).intersection(exclude_tables))
        if overlap:
            raise ConfigError(
                f"include_tables and exclude_tables overlap: {', '.join(overlap)}"
            )

    if prompt_path is None or not prompt_path.is_file():
        raise ConfigError(f"Gemini prompt file was not found: {prompt_path}")

    return AppConfig(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        prompt_path=prompt_path,
        output_dir=output_dir,
        model=model,
        gemini_api_key=gemini_api_key,
        include_tables=include_tables,
        exclude_tables=exclude_tables,
    )


def require_non_empty_string(raw: dict[str, Any], field_name: str) -> str:
    value = str(raw.get(field_name, "")).strip()
    if not value:
        raise ConfigError(f"Config is missing required field: {field_name}")
    return value


def parse_port(value: Any) -> int:
    try:
        port = int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError("Config field port must be an integer.") from exc
    if port <= 0:
        raise ConfigError("Config field port must be a positive integer.")
    return port


def parse_optional_string_list(value: Any, field_name: str) -> list[str] | None:
    if value in (None, "", []):
        return None
    if not isinstance(value, list):
        raise ConfigError(f"Config field {field_name} must be a list of strings.")
    items: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ConfigError(f"Config field {field_name} must contain only non-empty strings.")
        items.append(item.strip())
    return items or None


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
            "Gemini API key is missing. Set gemini_api_key in DBconfig.json or GEMINI_API_KEY in the environment."
        )
    return api_key


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
    kwargs: dict[str, Any] = {
        "temperature": 0.2,
        "response_mime_type": "application/json",
        "max_output_tokens": 32768,
    }
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
            message = str(getattr(exc, "message", "") or "").lower()
            if getattr(exc, "code", None) != 429:
                if any(pattern in message for pattern in PROMPT_TOO_LARGE_PATTERNS):
                    raise GeminiError(
                        "Gemini rejected the schema package because it is too large for one request. "
                        "Reduce scope with include_tables in DBconfig.json."
                    ) from exc
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
    match = re.search(r"limit:\s*([0-9]+)", message, re.IGNORECASE)
    if match:
        try:
            return int(match.group(1))
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


def load_mysql_schema(config: AppConfig) -> dict[str, Any]:
    try:
        import mysql.connector
        from mysql.connector import Error as MySQLError
    except ImportError as exc:
        raise DatabaseSchemaError(
            "The mysql-connector-python package is not installed. Run `pip install -r requirements.txt`."
        ) from exc

    try:
        connection = mysql.connector.connect(
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
            database=config.database,
        )
    except MySQLError as exc:
        raise DatabaseSchemaError(
            f"Unable to connect to MySQL database {config.database!r} on {config.host}:{config.port}: {exc}"
        ) from exc

    cursor: Any | None = None
    try:
        cursor = connection.cursor(dictionary=True)
        tables = fetch_tables(cursor, config.database)
        table_names = apply_table_filters(
            [row["TABLE_NAME"] for row in tables],
            include_tables=config.include_tables,
            exclude_tables=config.exclude_tables,
        )
        if not table_names:
            raise DatabaseSchemaError(
                "No tables remain after applying include/exclude filters."
            )

        tables_by_name = {row["TABLE_NAME"]: row for row in tables if row["TABLE_NAME"] in table_names}
        columns = fetch_columns(cursor, config.database, table_names)
        primary_keys = fetch_primary_keys(cursor, config.database, table_names)
        foreign_keys = fetch_foreign_keys(cursor, config.database, table_names)
        return build_schema_model(
            database=config.database,
            tables=tables_by_name,
            columns=columns,
            primary_keys=primary_keys,
            foreign_keys=foreign_keys,
        )
    except MySQLError as exc:
        raise DatabaseSchemaError(f"MySQL schema introspection failed: {exc}") from exc
    finally:
        try:
            if cursor is not None:
                cursor.close()
        except Exception:
            pass
        try:
            connection.close()
        except Exception:
            pass


def fetch_tables(cursor: Any, database: str) -> list[dict[str, Any]]:
    cursor.execute(
        """
        SELECT
            TABLE_NAME,
            TABLE_COMMENT,
            TABLE_TYPE
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = %s
          AND TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
        """,
        (database,),
    )
    rows = list(cursor.fetchall())
    if not rows:
        raise DatabaseSchemaError(f"No base tables found in schema {database!r}.")
    return rows


def apply_table_filters(
    table_names: list[str],
    *,
    include_tables: list[str] | None,
    exclude_tables: list[str] | None,
) -> list[str]:
    available = set(table_names)
    if include_tables:
        missing = sorted(set(include_tables) - available)
        if missing:
            raise DatabaseSchemaError(
                f"include_tables contains tables that do not exist in the schema: {', '.join(missing)}"
            )
        selected = [name for name in table_names if name in include_tables]
    else:
        selected = list(table_names)

    if exclude_tables:
        exclude_set = set(exclude_tables)
        selected = [name for name in selected if name not in exclude_set]

    return selected


def fetch_columns(
    cursor: Any, database: str, table_names: list[str]
) -> list[dict[str, Any]]:
    placeholders = ", ".join(["%s"] * len(table_names))
    cursor.execute(
        f"""
        SELECT
            TABLE_NAME,
            ORDINAL_POSITION,
            COLUMN_NAME,
            DATA_TYPE,
            COLUMN_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            NUMERIC_PRECISION,
            NUMERIC_SCALE,
            DATETIME_PRECISION,
            IS_NULLABLE,
            COLUMN_DEFAULT,
            COLUMN_COMMENT,
            EXTRA
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = %s
          AND TABLE_NAME IN ({placeholders})
        ORDER BY TABLE_NAME, ORDINAL_POSITION
        """,
        (database, *table_names),
    )
    return list(cursor.fetchall())


def fetch_primary_keys(
    cursor: Any, database: str, table_names: list[str]
) -> dict[tuple[str, str], dict[str, Any]]:
    placeholders = ", ".join(["%s"] * len(table_names))
    cursor.execute(
        f"""
        SELECT
            kcu.TABLE_NAME,
            kcu.COLUMN_NAME,
            kcu.ORDINAL_POSITION
        FROM information_schema.TABLE_CONSTRAINTS tc
        JOIN information_schema.KEY_COLUMN_USAGE kcu
          ON tc.CONSTRAINT_SCHEMA = kcu.CONSTRAINT_SCHEMA
         AND tc.TABLE_NAME = kcu.TABLE_NAME
         AND tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
        WHERE tc.TABLE_SCHEMA = %s
          AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
          AND tc.TABLE_NAME IN ({placeholders})
        ORDER BY kcu.TABLE_NAME, kcu.ORDINAL_POSITION
        """,
        (database, *table_names),
    )
    return {
        (row["TABLE_NAME"], row["COLUMN_NAME"]): row
        for row in cursor.fetchall()
    }


def fetch_foreign_keys(
    cursor: Any, database: str, table_names: list[str]
) -> list[dict[str, Any]]:
    placeholders = ", ".join(["%s"] * len(table_names))
    cursor.execute(
        f"""
        SELECT
            kcu.TABLE_NAME,
            kcu.COLUMN_NAME,
            kcu.CONSTRAINT_NAME,
            kcu.REFERENCED_TABLE_NAME,
            kcu.REFERENCED_COLUMN_NAME,
            rc.UPDATE_RULE,
            rc.DELETE_RULE
        FROM information_schema.KEY_COLUMN_USAGE kcu
        JOIN information_schema.REFERENTIAL_CONSTRAINTS rc
          ON rc.CONSTRAINT_SCHEMA = kcu.CONSTRAINT_SCHEMA
         AND rc.TABLE_NAME = kcu.TABLE_NAME
         AND rc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
        WHERE kcu.TABLE_SCHEMA = %s
          AND kcu.TABLE_NAME IN ({placeholders})
          AND kcu.REFERENCED_TABLE_NAME IS NOT NULL
        ORDER BY kcu.TABLE_NAME, kcu.CONSTRAINT_NAME, kcu.ORDINAL_POSITION
        """,
        (database, *table_names),
    )
    return list(cursor.fetchall())


def build_schema_model(
    *,
    database: str,
    tables: dict[str, dict[str, Any]],
    columns: list[dict[str, Any]],
    primary_keys: dict[tuple[str, str], dict[str, Any]],
    foreign_keys: list[dict[str, Any]],
) -> dict[str, Any]:
    fk_map = {
        (row["TABLE_NAME"], row["COLUMN_NAME"]): row
        for row in foreign_keys
    }
    relationships = [
        {
            "from_table": row["TABLE_NAME"],
            "from_column": row["COLUMN_NAME"],
            "to_table": row["REFERENCED_TABLE_NAME"],
            "to_column": row["REFERENCED_COLUMN_NAME"],
            "constraint_name": row["CONSTRAINT_NAME"],
            "update_rule": row["UPDATE_RULE"],
            "delete_rule": row["DELETE_RULE"],
        }
        for row in foreign_keys
    ]

    tables_out: list[dict[str, Any]] = []
    current_table_name: str | None = None
    current_table: dict[str, Any] | None = None
    for row in columns:
        table_name = row["TABLE_NAME"]
        if table_name != current_table_name:
            current_table_name = table_name
            table_metadata = tables.get(table_name, {})
            current_table = {
                "table_name": table_name,
                "table_comment": clean_comment(table_metadata.get("TABLE_COMMENT")),
                "columns": [],
            }
            tables_out.append(current_table)

        assert current_table is not None
        pk = (table_name, row["COLUMN_NAME"]) in primary_keys
        fk_row = fk_map.get((table_name, row["COLUMN_NAME"]))
        current_table["columns"].append(
            {
                "ordinal": int(row["ORDINAL_POSITION"]),
                "column_name": row["COLUMN_NAME"],
                "data_type": row["DATA_TYPE"],
                "column_type": row["COLUMN_TYPE"],
                "length_precision": format_length_precision(row),
                "is_primary_key": pk,
                "foreign_key_reference": format_fk_reference(fk_row),
                "is_not_null": str(row["IS_NULLABLE"]).upper() == "NO",
                "default": format_default(row.get("COLUMN_DEFAULT")),
                "column_comment": clean_comment(row.get("COLUMN_COMMENT")),
                "extra": row.get("EXTRA") or "",
            }
        )

    if not tables_out:
        raise DatabaseSchemaError("No columns were returned for the selected tables.")

    return {
        "database": database,
        "tables": tables_out,
        "relationships": relationships,
    }


def clean_comment(value: Any) -> str:
    text = str(value or "").strip()
    return text


def format_length_precision(row: dict[str, Any]) -> str:
    char_len = row.get("CHARACTER_MAXIMUM_LENGTH")
    if char_len is not None:
        return str(char_len)

    precision = row.get("NUMERIC_PRECISION")
    scale = row.get("NUMERIC_SCALE")
    if precision is not None:
        if scale not in (None, 0):
            return f"{precision},{scale}"
        return str(precision)

    dt_precision = row.get("DATETIME_PRECISION")
    if dt_precision not in (None, 0):
        return str(dt_precision)

    return ""


def format_default(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def format_fk_reference(fk_row: dict[str, Any] | None) -> str:
    if not fk_row:
        return ""
    return f"{fk_row['REFERENCED_TABLE_NAME']}.{fk_row['REFERENCED_COLUMN_NAME']}"


def build_enrichment_request(prompt_text: str, schema_model: dict[str, Any]) -> str:
    return f"""
{prompt_text.strip()}

Here is the MySQL schema metadata. Preserve all structural facts exactly.
Generate logical names and missing descriptions only where appropriate.

Schema metadata:
```json
{json.dumps(schema_model, ensure_ascii=False, indent=2)}
```
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


def extract_json_response(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            stripped = "\n".join(lines[1:-1]).strip()
            if stripped.lower().startswith("json"):
                stripped = stripped[4:].strip()

    try:
        data = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise GeminiError("Gemini returned invalid JSON for schema enrichment.") from exc

    if not isinstance(data, dict):
        raise GeminiError("Gemini schema enrichment response must be a JSON object.")
    return data


def build_enrichment_maps(ai_data: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[tuple[str, str], dict[str, Any]], list[str], str]:
    table_map: dict[str, dict[str, Any]] = {}
    column_map: dict[tuple[str, str], dict[str, Any]] = {}

    tables = ai_data.get("tables")
    if isinstance(tables, list):
        for table in tables:
            if not isinstance(table, dict):
                continue
            table_name = str(table.get("table_name", "")).strip()
            if not table_name:
                continue
            table_map[table_name] = table
            columns = table.get("columns")
            if isinstance(columns, list):
                for column in columns:
                    if not isinstance(column, dict):
                        continue
                    column_name = str(column.get("column_name", "")).strip()
                    if column_name:
                        column_map[(table_name, column_name)] = column

    raw_notes = ai_data.get("notes")
    notes = []
    if isinstance(raw_notes, list):
        notes = [str(note).strip() for note in raw_notes if str(note).strip()]
    summary = str(ai_data.get("summary", "")).strip()
    return table_map, column_map, notes, summary


def humanize_identifier(name: str) -> str:
    parts = [part for part in re.split(r"[_\s]+", name.strip()) if part]
    if not parts:
        return name
    return " ".join(part.upper() if len(part) <= 2 else part.capitalize() for part in parts)


def build_mermaid_identifier(name: str) -> str:
    identifier = re.sub(r"[^A-Za-z0-9_]", "_", name)
    if not identifier:
        identifier = "TABLE"
    if identifier[0].isdigit():
        identifier = f"T_{identifier}"
    return identifier


def build_markdown_document(schema_model: dict[str, Any], ai_data: dict[str, Any]) -> str:
    table_map, column_map, notes, summary = build_enrichment_maps(ai_data)
    database = schema_model["database"]
    title = str(ai_data.get("document_title", "")).strip() or f"{database} Schema Definition"

    lines: list[str] = [f"# {title}", ""]
    if summary:
        lines.extend([summary, ""])

    lines.extend(
        [
            "## Schema Overview",
            "",
            f"- Database: `{database}`",
            f"- Tables documented: {len(schema_model['tables'])}",
            f"- Relationships documented: {len(schema_model['relationships'])}",
            "",
            "## ERD",
            "",
            "```mermaid",
            render_mermaid_erd(schema_model),
            "```",
            "",
        ]
    )

    for table in schema_model["tables"]:
        table_name = table["table_name"]
        ai_table = table_map.get(table_name, {})
        logical_name = str(ai_table.get("logical_name", "")).strip() or humanize_identifier(table_name)
        description = table["table_comment"] or str(ai_table.get("description", "")).strip()

        lines.extend([f"## {table_name}", "", f"**Logical Name:** {logical_name}", ""])
        if description:
            lines.extend([description, ""])

        lines.extend(
            [
                "| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )

        for column in table["columns"]:
            ai_column = column_map.get((table_name, column["column_name"]), {})
            logical_column_name = (
                str(ai_column.get("logical_name", "")).strip()
                or humanize_identifier(column["column_name"])
            )
            description_text = column["column_comment"] or str(
                ai_column.get("description", "")
            ).strip()
            row = [
                str(column["ordinal"]),
                escape_markdown_table_cell(column["column_name"]),
                escape_markdown_table_cell(logical_column_name),
                escape_markdown_table_cell(column["data_type"].upper()),
                escape_markdown_table_cell(column["length_precision"]),
                "Y" if column["is_primary_key"] else "N",
                escape_markdown_table_cell(column["foreign_key_reference"]),
                "Y" if column["is_not_null"] else "N",
                escape_markdown_table_cell(column["default"]),
                escape_markdown_table_cell(description_text),
            ]
            lines.append("| " + " | ".join(row) + " |")

        lines.append("")

    if notes:
        lines.extend(["## Notes / Open Questions", ""])
        for note in notes:
            lines.append(f"- {note}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def escape_markdown_table_cell(value: Any) -> str:
    text = str(value or "")
    text = text.replace("|", "\\|").replace("\n", "<br>")
    return text


def render_mermaid_erd(schema_model: dict[str, Any]) -> str:
    entity_names = {
        table["table_name"]: build_mermaid_identifier(table["table_name"])
        for table in schema_model["tables"]
    }
    lines = ["erDiagram"]

    for table in schema_model["tables"]:
        entity_name = entity_names[table["table_name"]]
        lines.append(f"    {entity_name} {{")
        for column in table["columns"]:
            markers: list[str] = []
            if column["is_primary_key"]:
                markers.append("PK")
            if column["foreign_key_reference"]:
                markers.append("FK")
            marker_text = " ".join(markers)
            if marker_text:
                marker_text = f" {marker_text}"
            lines.append(
                f"        {sanitize_mermaid_type(column['data_type'])} {column['column_name']}{marker_text}"
            )
        lines.append("    }")

    for relationship in schema_model["relationships"]:
        from_name = entity_names.get(
            relationship["from_table"], build_mermaid_identifier(relationship["from_table"])
        )
        to_name = entity_names.get(
            relationship["to_table"], build_mermaid_identifier(relationship["to_table"])
        )
        label = f"{relationship['from_column']} -> {relationship['to_column']}"
        lines.append(f'    {to_name} ||--o{{ {from_name} : "{label}"')

    return "\n".join(lines)


def sanitize_mermaid_type(data_type: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", str(data_type).upper()) or "TYPE"


def safe_filename(name: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]+", "_", name).strip()
    return cleaned or "database_schema"


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
      font-size: 9pt;
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate Markdown database schema documentation from a MySQL schema using Gemini."
    )
    parser.add_argument(
        "--config",
        default="DBconfig.json",
        help="Path to the JSON DB config file. Defaults to DBconfig.json",
    )
    args = parser.parse_args(argv)

    config_path = Path(args.config).resolve()

    try:
        log(f"Loading config: {config_path}")
        config = load_config(config_path)
        api_key = resolve_gemini_api_key(config)

        log(f"Loading prompt: {config.prompt_path}")
        prompt_text = config.prompt_path.read_text(encoding="utf-8")

        log(
            f"Reading MySQL schema from {config.host}:{config.port}/{config.database}"
        )
        schema_model = load_mysql_schema(config)

        client, genai_types, genai_errors = build_gemini_client(api_key)
        generation_config = build_generation_config(genai_types)
        throttler = Gemini429Throttler()

        request_text = build_enrichment_request(prompt_text, schema_model)
        log(f"Generating schema documentation with Gemini model {config.model}")
        response = generate_content_with_rate_limit_retry(
            client=client,
            genai_errors=genai_errors,
            throttler=throttler,
            model_name=config.model,
            contents=request_text,
            generation_config=generation_config,
            label="database schema enrichment",
        )

        ai_data = extract_json_response(extract_response_text(response))
        markdown_text = build_markdown_document(schema_model, ai_data)

        base_name = safe_filename(f"{config.database}_schema")
        markdown_path = write_markdown(config.output_dir, base_name, markdown_text)
        log(f"Markdown written: {markdown_path}")

        title = str(ai_data.get("document_title", "")).strip() or f"{config.database} Schema Definition"
        if prompt_for_pdf_export():
            pdf_path = write_pdf(markdown_path, markdown_text, title)
            log(f"PDF written: {pdf_path}")
        else:
            log("PDF export skipped")

        return 0

    except (ConfigError, GeminiError, PdfError, DatabaseSchemaError) as exc:
        print(f"[db-docs] ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
