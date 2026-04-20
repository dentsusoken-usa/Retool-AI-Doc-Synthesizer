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
from urllib.parse import unquote


DEFAULT_MODEL = "gemini-2.5-flash-lite"
DEFAULT_OUTPUT_DIR = "output"
RETRY_DELAY_PATTERN = re.compile(r"Please retry in ([0-9.]+)s", re.IGNORECASE)
MAX_429_RETRIES = 6
DEFAULT_429_DELAY_SECONDS = 30.0


class ConfigError(RuntimeError):
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


def log(message: str) -> None:
    print(f"[retool-docs-raw] {message}")


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
        raise ConfigError(f"Source file was not found: {input_path}")
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


def read_source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def detect_code_fence_language(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "json"
    if suffix == ".py":
        return "python"
    if suffix in {".js", ".mjs", ".cjs"}:
        return "javascript"
    if suffix in {".ts", ".tsx"}:
        return "typescript"
    if suffix in {".md", ".markdown"}:
        return "markdown"
    if suffix == ".sql":
        return "sql"
    if suffix in {".yaml", ".yml"}:
        return "yaml"
    return "text"


def build_raw_request(prompt_text: str, input_path: Path, source_text: str) -> str:
    language = detect_code_fence_language(input_path)
    return f"""
{prompt_text.strip()}

You are receiving the raw source file directly with no preprocessing, no parsing, and no chunking.
Read the file as-is and generate the documentation from the raw content alone.
If parts of the file are noisy, serialized, or hard to interpret, say so explicitly instead of inventing structure.
Return Markdown only.

Source file path: {input_path}
Source file name: {input_path.name}

Raw file content:
```{language}
{source_text}
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


def clean_markdown_response(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            return "\n".join(lines[1:-1]).strip()
    return stripped


def human_title_from_path(input_path: Path) -> str:
    decoded_name = unquote(input_path.name)
    return Path(decoded_name).stem


def safe_filename(name: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]+", "_", name).strip()
    return cleaned or "retool_documentation"


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
        description="Generate Markdown documentation from a raw source file using Gemini."
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

        log(f"Loading raw source file: {config.input_path}")
        source_text = read_source_text(config.input_path)

        client, genai_types, genai_errors = build_gemini_client(api_key)
        generation_config = build_generation_config(genai_types)
        throttler = Gemini429Throttler()

        title = human_title_from_path(config.input_path)
        request_text = build_raw_request(prompt_text, config.input_path, source_text)

        log(f"Generating Markdown with Gemini model {config.model}")
        response = generate_content_with_rate_limit_retry(
            client=client,
            genai_errors=genai_errors,
            throttler=throttler,
            model_name=config.model,
            contents=request_text,
            generation_config=generation_config,
            label="raw file documentation generation",
        )
        markdown_text = clean_markdown_response(extract_response_text(response))

        base_name = safe_filename(title)
        markdown_path = write_markdown(config.output_dir, base_name, markdown_text)
        log(f"Markdown written: {markdown_path}")

        if prompt_for_pdf_export():
            pdf_path = write_pdf(markdown_path, markdown_text, title)
            log(f"PDF written: {pdf_path}")
        else:
            log("PDF export skipped")

        return 0

    except (ConfigError, GeminiError, PdfError) as exc:
        print(f"[retool-docs-raw] ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
