# Niramaya Health AI

An educational symptom-checker prototype by **Krunal Kaklotar**. It explores two approaches to the same interface: classifying symptom tokens with logistic regression and generating text with pretrained language models.

> Use synthetic inputs only. The project is intended for software demonstrations, not medical decisions or handling patient data.

[Browse the frontend](frontend/) · [Read the Flask inference routes](backend/routes/ask_AI_API.py) · [Inspect the example predictions](backend/model_LR/prediction_comparison_results.csv)

## How it works

| Path | Implementation |
| --- | --- |
| Logistic regression | Flask maps recognized symptom tokens to a binary feature vector and loads a serialized classifier with Joblib. Both routes use the same classifier. LRv2 adds a precaution lookup when available. |
| BioGPT | The Flask backend loads Microsoft's pretrained BioGPT through Hugging Face Transformers and generates text locally. |
| Gemini | Flask sends the submitted question to Google's Gemini API and returns the generated text. |
| Web interface | Static HTML, CSS, and JavaScript call the Flask routes. Account, family profile, and chat history routes use PostgreSQL. |

## What the evaluation shows

The checked-in [comparison CSV](backend/model_LR/prediction_comparison_results.csv) labels **24 of 41 rows correct** (58.5%). This is a count of recorded example outcomes. The repository does not provide a reproducible training pipeline, documented train/test split, or a clinical validation study. The comparison does not evaluate BioGPT or Gemini.

## Preview the interface

From the repository root, serve the static pages with Python:

```bash
python -m http.server 8000 --bind 127.0.0.1 --directory frontend
```

Open [the home page](http://127.0.0.1:8000/home.html) or [the model overview](http://127.0.0.1:8000/our_model.html). The pages can be browsed without starting Flask. Interactive features depend on the API at port 5000.

## Run the Flask API locally

Use Python 3.11 for the pinned dependencies. BioGPT downloads model files on first startup. The classifier is serialized with Joblib and needs scikit-learn. The original scikit-learn version used to serialize it is undocumented, so compatibility may require matching the training environment.

```bash
cd backend
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt scikit-learn sacremoses
python -m flask --app app run --host 127.0.0.1 --port 5000
```

| Endpoint | JSON body |
| --- | --- |
| `POST /asklrv1` | `{"symptoms":"skin_rash blackheads"}` |
| `POST /asklrv2` | `{"symptoms":"skin_rash blackheads"}` |
| `POST /askbiogpt` | `{"question":"What is a symptom?"}` |
| `POST /askgemini` | `{"question":"What is a symptom?"}` |

Set `GEMINI_API_KEY` before starting Flask to enable Gemini. Set `GEMINI_MODEL` to a model available to your key if the legacy default is unavailable. Only send synthetic questions to external services.

The account and chat flows require the PostgreSQL tables expected by the route modules. A database schema or migration is not included. Password-reset email additionally requires `NIRAMAYA_SMTP_USER` and `NIRAMAYA_SMTP_PASSWORD`.

## Next engineering steps

1. Add the training script, dataset provenance, dependency versions, and a repeatable evaluation on held-out examples.
2. Add a local database schema and environment-based configuration for the account and chat features.
3. Add route tests for invalid payloads, unknown symptom tokens, and unavailable model services.

[Krunal Kaklotar on LinkedIn](https://www.linkedin.com/in/krunal-kaklotar/)
