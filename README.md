 # AI Curriculum Generator

A lightweight Streamlit application that produces a beginner-friendly curriculum for a given topic by combining web research (Google Custom Search) with Google Generative AI (Gemini). This repository is structured for publishing on GitHub.

## Features
- Generate a structured curriculum in Markdown for any topic.
- Combine web research (Google Custom Search) with Gemini to draft content.

## Prerequisites
- Python 3.10+ (3.12 recommended)
- A working Python virtual environment
- API credentials for Google Custom Search and Gemini

## Configuration
Create a `.env` file at the project root (or export the variables in your shell) with the following keys:

```env
GOOGLE_API_KEY=your_google_api_key
SEARCH_ENGINE_ID=your_search_engine_cx
GEMINI_API_KEY=your_gemini_api_key
```

## Install (recommended for GitHub projects)
Create and activate a local virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```


## Run
With the virtual environment active and env vars configured:

```bash
streamlit run app.py
```

Open the URL printed by Streamlit, enter a topic, and click **Generate Curriculum**.

## Troubleshooting
- Import errors: confirm the virtual environment is active and dependencies installed.
- Google Custom Search: ensure `GOOGLE_API_KEY` and `SEARCH_ENGINE_ID` are valid and have quota.
- Gemini API: ensure `GEMINI_API_KEY` is valid and your account has access to the used model.

## Files
- `app.py` — main Streamlit application
- `requirements.txt` — minimal pinned dependencies used by `app.py`

