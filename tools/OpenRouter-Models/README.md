# OpenRouter Models Fetcher

[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](../../LICENSE.md)
![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)
![Supported OS](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

Fetches the public OpenRouter model catalog and saves it as a timestamped Markdown table.

## What it does

- Calls `https://openrouter.ai/api/v1/models`
- Formats results into a readable table
- Writes `openrouter-models_YYYYMMDD_HHMMSS.txt` in the same folder

## Setup

```bash
cd CluelessCodersToolbox/tools/OpenRouter-Models
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python get-openr-models.py
```

## Notes

- No API key required for the public models endpoint.
- Output files are ignored by git (see root `.gitignore`).

## License

MIT. See `../../LICENSE.md`.
