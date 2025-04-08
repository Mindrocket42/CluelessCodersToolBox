# 🧠 **Repo Analyzer: Instantly Understand Any Codebase**

[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
![Python 3.7+](https://img.shields.io/badge/Python-%3E=3.7-blue)
![Windows](https://img.shields.io/badge/Windows-supported-lightgrey)
![Linux](https://img.shields.io/badge/Linux-supported-lightgrey)
![macOS](https://img.shields.io/badge/macOS-supported-lightgrey)

---

## 🌟 What is Repo Analyzer? *Why should you care?*

Ever felt **lost in a giant codebase**? Or wanted a **quick, clean summary** of a project *without* digging through endless files?

**Repo Analyzer** is your **friendly robot assistant** that:

- **Clones or scans** any Git repository (local or remote)
- **Skips the junk**: binaries, media, clutter, and noise
- **Extracts code, imports, and metadata**
- **Exports a beginner-friendly JSON snapshot** of the entire repo

Perfect for **prompt engineers, coding newcomers, or casual contributors** who want to **understand, document, or improve** any repo — **without getting overwhelmed**.

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

---

## 🧩 How It Works: Under the Hood

**In simple steps:**

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
    E --> F{Excluded?}
    F -- Yes --> G[Skip file]
    F -- No --> H[Analyze file]
    H --> I[Extract content, imports, metadata]
    I --> J[Add to report]
    G --> J
    J --> K{More files?}
    K -- Yes --> E
    K -- No --> L[Export JSON report]
    L --> M[Done!]

style A fill:#cceeff,stroke:#333333,color:#111111
style B fill:#fffacd,stroke:#333333,color:#111111
style C fill:#cceeff,stroke:#333333,color:#111111
style D fill:#cceeff,stroke:#333333,color:#111111
style E fill:#cceeff,stroke:#333333,color:#111111
style F fill:#fffacd,stroke:#333333,color:#111111
style G fill:#ffddcc,stroke:#333333,color:#111111
style H fill:#cceeff,stroke:#333333,color:#111111
style I fill:#bbf7d0,stroke:#333333,color:#111111
style J fill:#bbf7d0,stroke:#333333,color:#111111
style K fill:#fffacd,stroke:#333333,color:#111111
style L fill:#bbf7d0,stroke:#333333,color:#111111
style M fill:#eeeeee,stroke:#333333,color:#111111
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

### 🥇 Option 1: Virtual Environment (Recommended for Beginners)

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

### 🥉 Option 3: Docker (Optional, Not Recommended for Beginners)

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

style A fill:#cceeff,stroke:#333333,color:#111111
style B fill:#fffacd,stroke:#333333,color:#111111
style C fill:#cceeff,stroke:#333333,color:#111111
style D fill:#cceeff,stroke:#333333,color:#111111
style E fill:#ffddcc,stroke:#333333,color:#111111
style F fill:#bbf7d0,stroke:#333333,color:#111111
style G fill:#bbf7d0,stroke:#333333,color:#111111
style H fill:#cceeff,stroke:#333333,color:#111111
style I fill:#bbf7d0,stroke:#333333,color:#111111
```

---

## ▶️ Running Repo Analyzer

After setup, run:

```bash
python Repo-Analyzer-main01.py
```

You'll be prompted to:

- Enter a **repository URL** (press Enter to skip if analyzing local repo)
- Enter the **local repository path**

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
