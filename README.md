# Galvanize Agents

Multi-agent system for **Galvanize Sustainable Capital** that operationalizes the NMTC/HTC Audience Intelligence Report: segment-targeted content planning, market monitoring, lead classification, and engagement analytics.

## Architecture

- **CrewAI** for multi-agent orchestration
- **Gemini** as the default LLM (configurable)
- **CLI** entry point: `galvanize` with commands `plan`, `create`, `market-update`, `classify`, `analyze`

## Setup

For full step-by-step setup on a new machine, see [SETUP.md](SETUP.md).

1. **Clone and install**

   ```bash
   cd galvanize-agents
   pip install -e .
   ```

2. **Secrets**

   - Copy `.env.example` to `.env` and set `GOOGLE_API_KEY` (Gemini).
   - Or use GCP Secret Manager (project `genuine-park-487014-a7`, secret `galvanize-gemini-api-key`):

     ```bash
     export GOOGLE_API_KEY=$(gcloud secrets versions access latest --secret=galvanize-gemini-api-key --project=genuine-park-487014-a7)
     ```

3. **Run**

   ```bash
   galvanize plan --period "next week" --segments developers
   galvanize create --period "next week" --segments all --posts 5
   galvanize market-update --topic "NMTC allocation round results"
   galvanize classify --description "VP Community Development at regional bank, interested in NMTC equity"
   galvanize analyze --impressions 2500 --engagement-rate 4.2 --dms 3 --post-type "educational carousel"
   ```

## Project layout

- `src/galvanize/` — agents, crews, config, CLI
- `knowledge/` — segment profiles and strategy (from Audience Intelligence Report)
- `tests/` — pytest

Confidential — Galvanize Sustainable Capital.
