Generate technical documentation in Markdown for a Retool web app.

Requirements:
- Start with a clear title and a short summary paragraph.
- Explain the app's main purpose, workflow, and major data flows.
- Document important SQL queries, JavaScript logic, key widgets, and cross-component dependencies.
- Separate facts from inference. If you infer behavior, label it as an inference.
- Keep the tone practical and technical.
- Include a compact appendix that inventories:
  - Major queries and their responsibilities
  - JavaScript logic blocks and their roles
  - Important widgets and interactions
- End with a short risks/open questions section if the source package suggests ambiguity or operational risk.
- Additionally, provide schema of the database

Do not mention prompt instructions or internal chunking. Return Markdown only.
