# 🧠 Repo Analyzer: Your Friendly Codebase Explorer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python 3.7+](https://img.shields.io/badge/Python-%3E=3.7-blue)
![Supported OS](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

---

## 🚀 What is Repo Analyzer?

Imagine if you could **summon a robot assistant** to **scan your entire codebase**, **skip the junk**, and **hand you a clean, structured summary** — ready for AI models or your own review.

**Repo Analyzer** does exactly that:

- It **clones or scans** any Git repository.
- **Filters out** binaries, media, and clutter.
- **Extracts code, imports, and metadata**.
- **Exports a detailed JSON snapshot** of your project.

Perfect for **prompt engineers, coding newcomers, or casual contributors** who want to **understand, document, or improve** any repo — **without getting lost**.

---

## 🧰 Tech Stack Overview

| Area             | Technologies / Tools                          |
|------------------|----------------------------------------------|
| **Language**     | Python 3.7+                                 |
| **Libraries**    | `gitpython`, `pathlib`, `logging`, `json`   |
| **Storage**      | Local JSON export                           |
| **CLI**          | Interactive command-line prompts            |
| **Output**       | Timestamped `.json` files in `.Repo-Analyzer-Output` |

---

## ✨ Key Features

- 🌀 **Clone or analyze** any Git repo (local or remote URL)
- 🧹 **Skips** binaries, media, archives, and common clutter
- 🕵️ **Extracts**:
  - File paths, sizes, extensions
  - Code content (text files only)
  - Import statements (Python)
  - Metadata (last modified time)
- 🗂️ **Organizes** by directory and file type
- 📦 **Exports** a timestamped JSON report
- 📝 **Beginner-friendly CLI prompts**
- 🔍 **Ideal for prepping repos for LLM analysis**

<details>
<summary>📁 Example Directory Structure</summary>

```plaintext
your-repo/
├── .Repo-Analyzer-Output/
│   └── analysis_YYYYMMDD_HHMMSS.json
├── src/
│   ├── main.py
│   └── utils.py
├── README.md
├── requirements.txt
└── ...
```
</details>

---

## 🧩 How It Works: Under the Hood

1. **Input**: You provide a **local repo path** (and optionally a **Git URL** to clone).
2. **Clone (optional)**: If URL is given, it clones the repo.
3. **Scan**: Recursively walks all files.
4. **Filter**: Skips excluded extensions & folders.
5. **Analyze**:
   - Reads text files
   - Extracts imports (Python)
   - Gathers metadata
6. **Export**: Saves a **timestamped JSON** report inside `.Repo-Analyzer-Output`.

---

## 🔄 Workflow Diagram

```mermaid
flowchart TD
    A[Start: Provide repo path / URL] --> B{Clone repo?}
    B -- Yes --> C[Clone repository]
    B -- No --> D[Use local repo]
    C --> E[Scan all files]
    D --> E
    E --> F{Exclude?}
    F -- Yes --> G[Skip file]
    F -- No --> H[Analyze file]
    H --> I[Extract content, imports, metadata]
    I --> J[Add to report]
    G --> J
    J --> K{More files?}
    K -- Yes --> E
    K -- No --> L[Export JSON report]
    L --> M[Done!]
```

---

## 🛠️ Prerequisites

| Tool            | Why Needed                                         | Download Link                                         |
|-----------------|----------------------------------------------------|-------------------------------------------------------|
| **Python 3.7+** | Runs the analyzer                                 | [python.org](https://www.python.org/downloads/)       |
| **Git**         | To clone remote repositories                       | [git-scm.com](https://git-scm.com/downloads)          |
| **pip**         | To install Python packages                         | Comes with Python                                     |
| **(Optional)** `conda` | Alternative environment manager            | [miniconda](https://docs.conda.io/en/latest/miniconda.html) |

_No API keys required!_

---

## ⚙️ Setup Options (Choose One)

### 🥇 Option 1: Virtual Environment (Recommended)

```bash
# Clone the repo (or download ZIP)
git clone https://github.com/yourname/repo-analyzer.git
cd repo-analyzer

# Create virtual environment
python -m venv repo_env

# Activate it
# Windows:
repo_env\Scripts\activate
# macOS/Linux:
source repo_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 🥈 Option 2: Conda Environment

```bash
conda create -n repo_env python=3.9
conda activate repo_env
pip install -r requirements.txt
```

### 🥉 Option 3: Docker (Advanced Users)

> ⚠️ **Note:** Docker adds complexity. Beginners may skip this.

```bash
# Build Docker image
docker build -t repo-analyzer .

# Run container
docker run -it --rm -v /path/to/your/repos:/repos repo-analyzer
```

---

## 🗺️ Visual Setup Guide

```mermaid
flowchart TD
    A[Clone/download repo] --> B[Choose setup method]
    B -->|venv| C[Create venv]
    B -->|conda| D[Create conda env]
    B -->|Docker| E[Build Docker image]
    C --> F[Activate env]
    D --> F
    E --> G[Run container]
    F --> H[Install dependencies]
    H --> I[Run Repo Analyzer]
    G --> I
    style C fill:#bbf
    style D fill:#bbf
    style E fill:#fa8
    style F fill:#bfb
    style G fill:#bfb
    style H fill:#ff9
    style I fill:#bfb
```

---

## ▶️ Running Repo Analyzer

After setup, run:

```bash
python Repo-Analyzer-main01.py
```

You'll be prompted:

- **Repository URL** (press Enter to skip if local)
- **Local repository path**

The tool will:

- Clone (if URL given)
- Analyze the repo
- Export a JSON report inside `.Repo-Analyzer-Output`

---

## 🔑 Configuration & API Keys

- **No API keys required!**
- Just provide a **repo URL** (optional) and **local path**.
- Output saved automatically in `.Repo-Analyzer-Output`.

---

## 📊 Project Status & Roadmap

- ✅ Clone and analyze Git repos
- ✅ Skip binaries/media
- ✅ Extract imports & metadata
- ✅ Export JSON reports
- ⏳ Improve language support (non-Python)
- ⏳ Add more visualizations
- 🔜 Web UI for easier use
- 🔜 Integration with LLMs for auto-docs
- ⚠️ Known: Large repos may take time

---

## 🤖 How AI Helped Build This

- AI pair programmers helped design filtering logic
- Assisted in writing docstrings and error handling
- Inspired this beginner-friendly README!

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 💬 Community & Support

- **New to coding?** You’re welcome here!
- Open issues or questions on GitHub
- Suggest features or improvements
- Share your experience to help others!

---

# 🧭 _Navigate any codebase with confidence!_
