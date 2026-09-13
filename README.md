# TuneAI 🎵

TuneAI is an AI-powered music discovery application combining the **Spotify Web API** and **Anthropic Claude**.

The user describes what they are in the mood for, Claude converts the request into structured music intent, Spotify provides candidate tracks and TuneAI ranks the results locally.

## Current version

This branch contains the **FastAPI backend**.

```text
User request
    ↓
Claude → music intent
    ↓
Spotify → candidate tracks
    ↓
TuneAI → local ranking
    ↓
15 recommendations
```

### What I've built

* Spotify authentication using **Authorization Code with PKCE**
* Natural-language music intent interpretation using Claude
* Spotify track search and candidate collection
* Deterministic local recommendation ranking
* Lightweight personalization using the user's top tracks and artists
* Duplicate removal and artist diversity
* FastAPI endpoints for authentication and recommendations
* 15 final recommendations per request

## Design choices

* **Python CLI first** — validate the core recommendation flow before adding a web stack.
* **FastAPI backend** — expose the existing recommendation logic through an API.
* **Claude for intent, Spotify for music** — Claude interprets the request; Spotify provides the actual tracks.
* **Local deterministic ranking** — predictable, explainable and easy to iterate on.
* **Lightweight personalization** — use existing Spotify taste without building a complex user profile.
* **No custom ML model** — uses LLM-based intent extraction, Spotify search and local ranking.

## Project structure

```text
SpotifAI/
├── .gitignore
├── README-LONG-VERSION.md
├── README.md
├── requirements.txt
│
└── api/
    ├── __init__.py
    │
    ├── ai/
    │   ├── __init__.py
    │   └── claude_service.py
    │
    ├── spotify/
    │   ├── __init__.py
    │   └── spotify_service.py
    │
    ├── comp/
    │   ├── __init__.py
    │   ├── computing_service.py
    │   └── ranking_service.py
    │
    ├── config.py
    ├── models.py
    └── app.py
```

### Responsibilities

* **`api/app.py`** — FastAPI endpoints and Spotify authentication callback
* **`api/models.py`** — Pydantic request and response models
* **`api/ai/claude_service.py`** — Claude integration and music intent extraction
* **`api/spotify/spotify_service.py`** — Spotify PKCE authentication, token refresh and API requests
* **`api/comp/computing_service.py`** — recommendation workflow orchestration
* **`api/comp/ranking_service.py`** — local ranking and recommendation diversity
* **`api/config.py`** — environment variables and application configuration

## Requirements

* Python 3.10+
* Spotify account with an active Premium subscription
* Spotify Developer application
* Anthropic API key

## Configuration

Create `.env.local` in the project root:

```env
ANTHROPIC_API_KEY=your_api_key_here
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

Do not commit `.env.local`.

Configure this redirect URI in the Spotify Developer Dashboard:

```text
http://127.0.0.1:8000/auth/callback
```

TuneAI uses Spotify's **Authorization Code with PKCE** flow. After authorizing Spotify, the user is automatically redirected back to the FastAPI callback.

## Installation

```bash
git clone <HTTPS or SSH repository URL>

python -m venv .venv
```

Activate the virtual environment:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Start the FastAPI server:

```bash
uvicorn api.app:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Start Spotify authentication:

```text
http://127.0.0.1:8000/auth/login
```

Then request recommendations through:

```text
POST /recommendations
```

Example:

```json
{
  "request": "Slow but energetic R&B for a late-night drive."
}
```

## API endpoints

| Method | Endpoint           | Purpose                       |
| ------ | ------------------ | ----------------------------- |
| `GET`  | `/`                | API information               |
| `GET`  | `/health`          | Health check                  |
| `GET`  | `/auth/login`      | Start Spotify authentication  |
| `GET`  | `/auth/callback`   | Handle Spotify OAuth callback |
| `POST` | `/recommendations` | Generate recommendations      |

## Time Tracking

```text
Time spent CLI MVP: 3:11:36,44
Time spent FastAPI: 2:24:22,73
Time spent React frontend: ...
Time spent future branch: ...

Time spent total: 5:35:59,17
```

## Next steps

```text
CLI MVP
   ↓
FastAPI backend
   ↓
React frontend
```

The next stage will add a React frontend consuming the existing FastAPI backend.

## Technologies

* **Python** — application
* **FastAPI** — backend API
* **Anthropic Claude** — music intent interpretation
* **Spotify Web API** — authentication and music search
* **Requests** — HTTP requests
* **Pydantic** — API validation
* **python-dotenv** — environment configuration
* **Uvicorn** — development server