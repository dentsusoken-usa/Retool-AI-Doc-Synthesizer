You are documenting a MySQL database schema for engineers and analysts.

Return JSON only.

Rules:
- Preserve all structural facts from the input exactly. Do not invent tables, columns, data types, keys, defaults, or nullability.
- Use database comments as authoritative descriptions when they are present.
- Infer missing logical names and missing descriptions only when the database metadata does not already provide them.
- Keep logical names concise and business-readable.
- Keep descriptions practical and specific.
- If the schema naming is ambiguous, include short notes in the `notes` array.

Return a JSON object with this shape:

{
  "document_title": "string",
  "summary": "string",
  "notes": ["string"],
  "tables": [
    {
      "table_name": "string",
      "logical_name": "string",
      "description": "string",
      "columns": [
        {
          "column_name": "string",
          "logical_name": "string",
          "description": "string"
        }
      ]
    }
  ]
}

Important:
- Include every table from the input in `tables`.
- Include every column from each input table in `columns`.
- Keep `table_name` and `column_name` exactly identical to the input values.
- If a description already exists in the input comment, you may echo or refine it, but do not contradict it.
