#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from generate_DB_docs import (
    ConfigError,
    DatabaseSchemaError,
    AppConfig,
    load_config,
    load_schema_model,
)


def log(message: str) -> None:
    print(f"[db-extract] {message}")


def safe_filename(name: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in name)
    cleaned = cleaned.strip("._")
    return cleaned or "db_schema_extract"


def build_ai_ready_payload(
    config: AppConfig, config_path: Path, schema_model: dict[str, Any]
) -> dict[str, Any]:
    relationships = schema_model.get("relationships", [])
    tables = schema_model.get("tables", [])

    outbound_by_table: dict[str, list[dict[str, Any]]] = {}
    inbound_by_table: dict[str, list[dict[str, Any]]] = {}
    for relationship in relationships:
        if not isinstance(relationship, dict):
            continue
        from_table = str(relationship.get("from_table", "")).strip()
        to_table = str(relationship.get("to_table", "")).strip()
        if from_table:
            outbound_by_table.setdefault(from_table, []).append(relationship)
        if to_table:
            inbound_by_table.setdefault(to_table, []).append(relationship)

    table_entries: list[dict[str, Any]] = []
    for table in tables:
        if not isinstance(table, dict):
            continue
        table_name = str(table.get("table_name", "")).strip()
        columns = table.get("columns", [])
        normalized_columns: list[dict[str, Any]] = []
        primary_key_columns: list[str] = []
        foreign_key_columns: list[dict[str, Any]] = []

        for column in columns:
            if not isinstance(column, dict):
                continue
            column_name = str(column.get("column_name", "")).strip()
            is_primary_key = bool(column.get("is_primary_key", False))
            foreign_key_reference = str(column.get("foreign_key_reference", "") or "").strip()
            if is_primary_key and column_name:
                primary_key_columns.append(column_name)
            if foreign_key_reference and column_name:
                foreign_key_columns.append(
                    {
                        "column_name": column_name,
                        "reference": foreign_key_reference,
                    }
                )

            normalized_columns.append(
                {
                    "ordinal": column.get("ordinal"),
                    "column_name": column_name,
                    "data_type": column.get("data_type", ""),
                    "column_type": column.get("column_type", ""),
                    "length_precision": column.get("length_precision", ""),
                    "is_primary_key": is_primary_key,
                    "foreign_key_reference": foreign_key_reference,
                    "is_not_null": bool(column.get("is_not_null", False)),
                    "default": column.get("default", ""),
                    "column_comment": column.get("column_comment", ""),
                    "extra": column.get("extra", ""),
                }
            )

        outbound_relationships = outbound_by_table.get(table_name, [])
        inbound_relationships = inbound_by_table.get(table_name, [])
        table_entries.append(
            {
                "table_name": table_name,
                "table_comment": table.get("table_comment", ""),
                "column_count": len(normalized_columns),
                "primary_key_columns": primary_key_columns,
                "foreign_key_columns": foreign_key_columns,
                "outbound_relationship_count": len(outbound_relationships),
                "inbound_relationship_count": len(inbound_relationships),
                "outbound_relationships": outbound_relationships,
                "inbound_relationships": inbound_relationships,
                "columns": normalized_columns,
            }
        )

    return {
        "schema_export_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "config_path": str(config_path),
            "mode": config.mode,
            "database": config.database,
            "host": config.host if config.mode == "mysql" else None,
            "port": config.port if config.mode == "mysql" else None,
            "include_tables": config.include_tables or [],
            "exclude_tables": config.exclude_tables or [],
            "mock_schema_path": str(config.mock_schema_path) if config.mock_schema_path else None,
        },
        "summary": {
            "table_count": len(table_entries),
            "relationship_count": len(
                [item for item in relationships if isinstance(item, dict)]
            ),
        },
        "relationships": [
            item for item in relationships if isinstance(item, dict)
        ],
        "tables": table_entries,
    }


def write_json_output(output_dir: Path, database_name: str, payload: dict[str, Any]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{safe_filename(database_name)}_schema_extract.json"
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract database schema information into a single AI-friendly JSON file."
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

        if config.mode == "mock":
            log(
                f"Loading mock schema from {config.mock_schema_path} for database {config.database}"
            )
        else:
            log(f"Reading MySQL schema from {config.host}:{config.port}/{config.database}")

        schema_model = load_schema_model(config)
        payload = build_ai_ready_payload(config, config_path, schema_model)
        output_path = write_json_output(config.output_dir, config.database, payload)
        log(f"Schema extract written: {output_path}")
        return 0

    except (ConfigError, DatabaseSchemaError) as exc:
        print(f"[db-extract] ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
