# AI Sentiment Analysis REST API (Software Engineering Assignment)

A Python Flask REST API that uses a Hugging Face sentiment-analysis model to classify text as **POSITIVE** or **NEGATIVE**. The frontend is made using Streamlit. Results are saved in SQLite. JWT tokens protect the API.

## Features
- POST `/login`: get a JWT token using credentials from `.env`
- POST `/analyze`: analyze sentiment (JWT required); store in SQLite
- GET `/history`: list saved predictions (JWT required)
- GET `/`: confirm server is running
- Streamlit buttons: **Analyze Sentiment** and **Show Saved Predictions (Table)**

## Setup (Windows PowerShell)

Requires Python 3.10+ and an internet connection for the first download of the Hugging Face model.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` to set your own secret key and username/password. Generate a key with:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Start Flask in terminal 1:

```powershell
python app.py
```

Start Streamlit in terminal 2 (same environment):

```powershell
streamlit run frontend.py
```

Open the local address printed by Streamlit (usually http://localhost:8501), login with the username/password from `.env`, test a positive and a negative sentence, then click **Show Saved Predictions (Table)**.

## Example API requests

POST `/login` JSON:
```json
{"username":"student","password":"your-local-password"}
```
Response: `{"token":"..."}`

POST `/analyze` with HTTP header `Authorization: Bearer YOUR_TOKEN`:
```json
{"text":"This movie was amazing!"}
```
Response example (model scores vary):
```json
{"text":"This movie was amazing!","sentiment":"POSITIVE","score":0.9999}
```

GET `/history` with the same Authorization header returns saved rows.

## Demonstration checklist
1. Explain frontend -> Flask -> Hugging Face model -> SQLite.
2. Show `.env.example` and `.gitignore` (do not reveal your real `.env` values).
3. Show Flask server running and Streamlit login.
4. Analyze positive and negative text.
5. Click **Show Saved Predictions (Table)** to prove database storage.
6. Explain `POST` vs `GET`, secret keys and JWT authorization.
7. Show GitHub repository and submit its URL with your screen recording in Google Classroom.

## Security
Never commit `.env` or real credentials. Local demo only; do not expose Flask debug mode publicly. Passwords in this small educational application are local demonstration credentials, not a production user authentication system.
