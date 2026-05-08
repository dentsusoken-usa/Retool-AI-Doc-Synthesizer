# Project Instructions for Codex

This project generates documentation from Retool exported JSON files.

Important folders:
- sourcecode/: Retool exported JSON files
- prompts/: prompt templates
- output/: generated documentation
- config.json: local config file, may contain API keys or paths

Rules:
- Do not commit API keys or secrets.
- Do not print API keys in output.
- Prefer Python scripts.
- Existing main script: generate_retool_docs.py
- Raw/simple script: generate_retool_docs_raw.py
- Generated docs should go into output/.
- When modifying scripts, preserve existing behavior unless asked.
- Add clear comments and error handling.
- Use requirements.txt for dependencies.