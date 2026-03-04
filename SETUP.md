# Complete Environment Setup (Another Machine)

Step-by-step instructions to bring the Galvanize agents environment up on a new machine. No database or dump is required—all knowledge is in the repo; CrewAI/ChromaDB rebuilds indices on first run.

---

## Prerequisites

- **Python** 3.10, 3.11, or 3.12 (CrewAI requires 3.10+).
- **Git**.
- **(Optional)** [gcloud CLI](https://cloud.google.com/sdk/docs/install) if you use GCP Secret Manager for `GOOGLE_API_KEY`.

---

## Step 1: Clone the repo

```bash
git clone https://github.com/bennieking05/galvanize-agents.git
cd galvanize-agents
```

---

## Step 2: Create a virtual environment (recommended)

Using a venv avoids architecture and dependency conflicts (e.g. rpds/ChromaDB). Create and activate it on the **target machine**; do not copy `.venv` from another OS or architecture.

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

---

## Step 3: Install the project

```bash
pip install -e .
```

---

## Step 4: Configure secrets

1. Copy the example env file and create `.env`:
   ```bash
   cp .env.example .env
   ```

2. Set **`GOOGLE_API_KEY`** (Gemini API key). Choose one:

   - **From GCP Secret Manager** (project `genuine-park-487014-a7`, secret `galvanize-gemini-api-key`):
     ```bash
     echo "GOOGLE_API_KEY=$(gcloud secrets versions access latest --secret=galvanize-gemini-api-key --project=genuine-park-487014-a7)" >> .env
     ```
   - Or paste a key from [Google AI Studio](https://aistudio.google.com/apikey) into `.env`.

3. **(Optional)** Set **`SERPER_API_KEY`** in `.env` for Policy Monitor web search (get a key at [serper.dev](https://serper.dev)).

---

## Step 5: Verify

```bash
galvanize plan --period "next week" --segments developers
```

The first run builds CrewAI/ChromaDB knowledge indices from the `knowledge/` files in the repo. No extra data or dump is required.

---

## Optional: Override LLM model

Default model is `gemini-2.5-flash`. To use a different model (e.g. for region or API support), add to `.env`:

```
GALVANIZE_LLM_MODEL=gemini-2.5-flash
```

Change to a supported model name (e.g. `gemini-1.5-flash` or `gemini-2.0-flash-001` if still available in your context).

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| **"OPENAI_API_KEY is not set"** | Ensure `.env` has `GOOGLE_API_KEY`. The project uses a Google embedder (see `config.py` and crew files); no OpenAI key is needed. |
| **Architecture / rpds errors** | Use a **new venv** and `pip install -e .` on the target machine. Do not copy `.venv` from another OS or CPU architecture. |
| **"model ... is not found"** | Default is `gemini-2.5-flash`. If your key or region does not support it, set `GALVANIZE_LLM_MODEL` in `.env` to a supported model. |

---

## Data and "DB dump"

- **No database** — There is no PostgreSQL, MySQL, or other database. Nothing to dump or restore.
- **Knowledge base** — All content is under `knowledge/` in the repo:
  - `knowledge/segments/` — developers.md, investors.md, cdes.md, community_leaders.md
  - `knowledge/strategy_matrix.md`, `consumption_habits.md`, `market_context.md`, `implementation.md`
  Cloning the repo is sufficient; these files are versioned.
- **ChromaDB / CrewAI storage** — CrewAI builds embedding indices on first run from the markdown above and stores them in a platform-specific directory (e.g. `~/.local/share/CrewAI/` on Linux). That cache is **recreated automatically** when you run any crew on the new machine; no dump or copy is required.
- **Optional:** To keep CrewAI/ChromaDB cache inside the project directory, set before running:
  ```bash
  export CREWAI_STORAGE_DIR=./.crewai_storage
  ```
  Add `.crewai_storage/` to `.gitignore` if you use this.
