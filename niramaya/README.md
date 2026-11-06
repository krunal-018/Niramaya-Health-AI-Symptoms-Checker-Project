# Niramaya Health AI

An educational biomedical evidence workspace by Krunal Kaklotar. Ask free-text questions and follow-ups, retrieve PubMed-indexed papers through Europe PMC, and collect sources and questions in downloadable visit notes.

## Run locally

From this directory, install the requirements in a fresh virtual environment. Set a fresh Gemini API key in your environment to enable chat. Research and Visit Prep can run without it.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app run --port 5000
```

Open http://127.0.0.1:5000. Stop any previous Flask instance on port 5000 first. Chat accepts a question and a separate literature topic. Use English search terms for PubMed coverage. The answer language selector controls model output. Set optional `GEMINI_MODEL` to override the configured default.

## Deploy

Connect the repository and rebuild branch in Render using the root Blueprint. Enter the key in Render's secret configuration. Select the Free plan and review your Gemini project's quotas and billing settings before enabling public chat. Free web services can sleep when idle.

The app forwards research topics to Europe PMC and sends chat questions, limited follow-up context, and retrieved abstracts to Gemini. It does not persist chats or notes. Avoid submitting private medical information. Retrieved sources and generated statements should be reviewed together. The app is for general educational use. It has not undergone clinical validation.
