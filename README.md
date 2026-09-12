# TuneAI 🎵

TuneAI is an AI-powered music discovery application combining the **Spotify Web API** and **Anthropic Claude**.

The user describes what they are in the mood for, Claude converts the request into structured music intent, Spotify provides candidate tracks and TuneAI ranks the results locally.

## Current version

This branch contains the **CLI MVP**.

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
* 15 final recommendations per request

## Design choices

* **Python CLI first** — validate the core recommendation flow before adding a web stack.
* **Claude for intent, Spotify for music** — Claude interprets the request; Spotify provides the actual tracks.
* **Local deterministic ranking** — predictable, explainable and easy to iterate on.
* **Lightweight personalization** — use existing Spotify taste without building a complex user profile.
* **No custom ML model** — uses LLM-based intent extraction, Spotify search and local ranking.

## Project structure

```text
tuneai/
├── main.py
├── config.py
├── .env.example
├── requirements.txt
│
├── ai/
│   ├── __init__.py
│   └── claude_service.py
│
└── spotify/
    ├── __init__.py
    ├── ranking_service.py
    └── spotify_service.py
```

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

The CLI uses PKCE and a manual callback step. After authorizing Spotify, paste the callback URL into the CLI when prompted.

## Installation

```bash
git clone <HTTPS or SSH repository URL>
cd tuneai

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

```bash
python main.py
```

The application will authenticate with Spotify, interpret the user's request with Claude, search Spotify, rank the candidates and display 15 recommendations.

## Time Tracking

```text
Time spent CLI MVP: 3:11:36,44
Time spent FastAPI: ...
Time spent React frontend: ...
Time spent future branch: ...

Time spent total: 3:11:36,44
```

## Next steps

```text
CLI MVP
   ↓
FastAPI backend
   ↓
React frontend
```

## Technologies

* **Python** — application
* **Anthropic Claude** — music intent interpretation
* **Spotify Web API** — authentication and music search
* **Requests** — HTTP requests
* **python-dotenv** — environment configuration
