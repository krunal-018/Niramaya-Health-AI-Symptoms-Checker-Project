# Niramaya AI Scenario Studio

A portfolio demo with fictional scenarios, built-in sample responses, and optional live Gemini responses. Flask serves the interface and API on the same origin. The demo uses no database or local model download.

## Run on Windows

From the repository root:

```powershell
cd portfolio
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app run --port 5000
```

Open http://127.0.0.1:5000. Set a fresh `GEMINI_API_KEY` in the server environment before starting Flask to enable live mode. Set `GEMINI_MODEL` to override the default model if necessary.

## Deploy on Render

Connect this GitHub repository in Render and deploy the branch containing the demo. The root `render.yaml` defines a Free web service. For manual setup, use root directory `portfolio`, build command `pip install -r requirements.txt`, start command `gunicorn --workers 1 --threads 4 --bind 0.0.0.0:$PORT app:app`, and health check `/healthz`. Set optional Gemini configuration in Render's Environment settings. The Free service can sleep when idle, and live requests depend on provider quota.

The original research prototype is documented in the repository root. This separate entry point uses curated fictional prompts for a public portfolio audience.
