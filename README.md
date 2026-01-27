# CluelessCodersToolbox

[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE.md)
![Python tools](https://img.shields.io/badge/Python-tools-blue)
![Supported OS](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

CluelessCodersToolbox is a beginner-friendly toolbox of small, focused scripts I use for everyday tasks. Each tool is intentionally simple, documented, and kept independent so you can run one tool without learning the whole repo.

## Design goals

- Simple for beginners: minimal setup, clear instructions
- Tool isolation: each tool has its own `requirements.txt`
- Strict dependency pins for predictable installs

## Repository layout

```text
CluelessCodersToolbox/
├── tools/                         # All runnable tools (each has its own README)
│   ├── Audio-File-Tools/
│   ├── Document-Format-Converters/
│   ├── File-and-Folder-Structure/
│   ├── OpenAI-JSON-to-Markdown/
│   ├── OpenRouter-Models/
│   └── Repo-Analyzer/
├── docs/                          # Writing guidelines and notes
├── templates/                     # Starter files (ex: gitignore)
├── LICENSE.md
└── README.md
```

## Local-only folders

- Any folder or file that starts with `__` is treated as local-only and ignored by git.
- Use this for personal archives, scratch data, or outputs you don't want published.

## Quick start (per tool)

1. Pick a tool in `tools/`.
2. Follow that tool's `README.md`.
3. Install dependencies for that tool only.

Example:

```bash
cd tools/Document-Format-Converters
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python PDF-to-Images/pdf_to_images.py
```

## Notes on dependencies

- Tools are independent on purpose.
- Dependencies are pinned in each `requirements.txt` to reduce surprise breakages.
- Some tools use only the standard library and have no requirements file.

## License

MIT. See `LICENSE.md`.
