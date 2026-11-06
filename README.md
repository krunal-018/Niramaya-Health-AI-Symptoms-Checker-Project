# Niramaya Health AI

**A conversational health information and biomedical research workspace** by Krunal Kaklotar.

### [Open the live app ↗](https://niramaya-health-ai-bbzc.onrender.com/)

Ask a health question in plain language, explore published research, or prepare notes for a healthcare conversation. Niramaya is an educational project and has not undergone clinical validation.

## Features

| Feature | What you can do |
| --- | --- |
| **Direct Chat** | Ask a question without entering a research topic. The assistant can ask follow-up questions about details such as symptom duration and measured temperature, then use your recent replies to tailor general information. |
| **Research-backed Chat** | Enter a question and literature search terms. The app retrieves biomedical abstracts and shows the papers alongside the generated answer so you can inspect the evidence. |
| **Research Explorer** | Search PubMed-indexed literature through Europe PMC, read abstracts, and open the original PubMed records. |
| **Visit Prep** | Add questions and source links from the workspace, edit your notes, and download them as a text file. |
| **Answer language** | Choose English or German for AI answers. The interface is in English. |

**Try it:** In Direct Chat, use the fictional example “I have a fever. What information should I tell a clinician?” In Research Explorer, try `exercise AND sleep quality`.

## Technology stack

| Layer | Technologies |
| --- | --- |
| Frontend | HTML, CSS, and vanilla JavaScript |
| Backend | Python and Flask |
| AI | Google Gemini API. Default model: `gemini-3.5-flash-lite` |
| Research | Europe PMC REST API and PubMed record links |
| Hosting | Render web service with Gunicorn and a [deployment Blueprint](render.yaml) |

Flask serves the website and API from the same origin. Direct Chat calls Gemini, while Research-backed Chat retrieves abstracts from Europe PMC first. Visit notes are edited and exported in the browser. The deployed app does not use a database.

## Run locally

From the repository root, run these commands in Windows PowerShell with Python 3.11:

```powershell
cd niramaya
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app run --host 127.0.0.1 --port 5000
```

Open [the local homepage](http://127.0.0.1:5000/). To enable chat, set `GEMINI_API_KEY` in the same PowerShell session before starting Flask. Optionally set `GEMINI_MODEL` to override the default. Research Explorer and Visit Prep work without a Gemini key.

## Deployment

The live app deploys from `main` on Render using `niramaya/` as the service root and `/healthz` as the health check. Configure `GEMINI_API_KEY` in Render's environment settings. Keep credentials out of Git.

## Repository layout

- [`niramaya/app.py`](niramaya/app.py) — Flask routes, Gemini integration, and literature retrieval.
- [`niramaya/static/`](niramaya/static/) — Interface, styling, and browser interactions.
- [`render.yaml`](render.yaml) — Hosting configuration.
- [`backend/`](backend/) and [`frontend/`](frontend/) — Earlier prototype, including the original BioGPT and logistic regression experiments.

## Privacy and scope

Chat sends your question and limited recent conversation context to Gemini. Literature search terms go to Europe PMC. Keep names, medical records, and other identifying details out of the app. Visit notes stay in the current page until you download them. Review generated information and its sources before relying on it.

[Live homepage](https://niramaya-health-ai-bbzc.onrender.com/) · [Krunal Kaklotar on LinkedIn](https://www.linkedin.com/in/krunal-kaklotar/)
