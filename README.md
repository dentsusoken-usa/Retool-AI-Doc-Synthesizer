# RetoolDocwithGemini

Generate documentation for a Retool app export with the Gemini API.

This repo currently includes two command-line scripts:

- `generate_retool_docs.py`
  - Parses and normalizes a Retool export before sending structured context to Gemini.
  - Best when you want Gemini to work from extracted queries, JavaScript logic, widgets, and dependencies instead of the raw export blob.
- `generate_retool_docs_raw.py`
  - Sends the raw source file content directly to Gemini with no Retool parsing, no chunk preprocessing, and no batch logic.
  - Best when you want the model to read the original file as-is.

Both scripts:

- read configuration from `config.json`
- generate Markdown output
- optionally export PDF after Markdown is created
- support `429` retry/throttling for Gemini rate limits

## Repo Layout

- `config.json`: runtime configuration
- `requirements.txt`: Python dependencies
- `prompts/retool_doc_prompt.md`: editable Gemini prompt
- `sourcecode/`: sample Retool export JSON files
- `output/`: generated Markdown and PDF files
- `generate_retool_docs.py`: parsed/structured documentation flow
- `generate_retool_docs_raw.py`: raw-file documentation flow

## Requirements

- Python 3.10+
- A Gemini API key

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Configuration

The scripts use `config.json` with these fields:

```json
{
  "input_path": "sourcecode/YourRetoolExport.json",
  "prompt_path": "prompts/retool_doc_prompt.md",
  "output_dir": "output",
  "model": "gemini-2.5-flash-lite",
  "gemini_api_key": ""
}
```

Field notes:

- `input_path`: one source file to document
- `prompt_path`: the prompt file sent to Gemini
- `output_dir`: where Markdown/PDF files are written
- `model`: Gemini model name
- `gemini_api_key`: optional; if blank, the scripts fall back to the `GEMINI_API_KEY` environment variable

Prefer using an environment variable instead of storing a real key in `config.json`:

```powershell
$env:GEMINI_API_KEY="your_actual_key"
```

## Usage

### 1. Parsed Retool mode

Use this when you want the script to decode the Retool export and send structured app information to Gemini.

```powershell
python generate_retool_docs.py --config config.json
```

What it does:

- loads the Retool export JSON
- decodes the serialized `appState`
- extracts structured context such as SQL queries, JavaScript logic, widgets, and dependencies
- asks Gemini to generate documentation from that structured context

### 2. Raw file mode

Use this when you do not want any Retool-specific parsing and want Gemini to interpret the source file directly.

```powershell
python generate_retool_docs_raw.py --config config.json
```

What it does:

- reads the source file as raw text
- sends that raw file directly to Gemini in one generation request
- writes the resulting Markdown

## Prompt Customization

Edit `prompts/retool_doc_prompt.md` to change:

- the tone of the documentation
- the level of technical detail
- the section structure
- whether Gemini should include summaries, appendices, risks, or open questions

## Output

Both scripts write Markdown to the configured `output_dir` using the source filename as the document name.

Example outputs:

- `output/Royalty Calculation.md`
- `output/Royalty Calculation.pdf`

After Markdown generation, the script asks:

```text
Export PDF? [y/N]:
```

If you answer `y`, the script converts the Markdown to PDF.

## Choosing a Script

Use `generate_retool_docs.py` when:

- you want cleaner, more structured context
- you want Gemini to work from extracted Retool entities instead of raw serialized data

Use `generate_retool_docs_raw.py` when:

- you want the simplest possible flow
- you want no Retool parsing at all
- you want Gemini to interpret the file directly

## Rate Limits

Gemini free-tier quotas can cause `429 RESOURCE_EXHAUSTED` errors.

The scripts already include automatic retry/throttling for `429` responses, but long runs can still pause while waiting for quota to reset.

If you hit repeated quota problems:

- wait for the retry window and rerun
- reduce the number of requests
- switch models
- enable billing for higher quotas

## Notes

- These scripts are single-file oriented. They expect one input file per run.
- The parsed script is more Retool-aware.
- The raw script is simpler, but if the raw file is too large for a single Gemini request, Gemini may still reject it.
