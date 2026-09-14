# TuneAI 🎵

TuneAI is an AI-powered music discovery application that combines the **Spotify Web API** with **Anthropic Claude** to turn a natural-language music request into personalized music recommendations.

For example, a user can enter:

> "I want something slow but energetic, maybe R&B for a late-night drive."

TuneAI interprets the request, searches Spotify for relevant tracks and ranks the results based on search relevance and the user's existing Spotify listening data.

## Current Version

This version contains the **FastAPI backend** of TuneAI.

The original CLI MVP was used to validate the core recommendation flow. The FastAPI version exposes the same functionality through an API and prepares the application for a React frontend.

### Current flow

```text
User
  ↓
Spotify authentication
  ↓
Natural-language request
  ↓
Claude
  ↓
Structured music intent
  ↓
Spotify search
  ↓
Candidate tracks
  ↓
Local ranking
  ↓
15 recommendations
```

---

# What I've Built

## 1. Spotify authentication

TuneAI authenticates the user with Spotify using the **Authorization Code with PKCE** flow.

The FastAPI backend provides an authentication flow where:

1. `/auth/login` generates a Spotify authorization URL.
2. The user authorizes TuneAI through Spotify.
3. Spotify automatically redirects to `/auth/callback`.
4. FastAPI receives the authorization code and state.
5. TuneAI exchanges the code for Spotify access and refresh tokens.
6. The tokens are kept in memory and reused for recommendation requests.
7. Access tokens are automatically refreshed when they expire.

The application requests the following scopes:

* `user-read-private`
* `user-top-read`

The `user-top-read` scope allows TuneAI to access the user's top tracks and artists for lightweight personalization.

The current implementation is designed for a **single-user local application**. Authentication state is stored in memory and is lost when the FastAPI application restarts.

## 2. Natural-language music interpretation

Users can describe what they want using normal language rather than selecting predefined genres or moods.

Claude converts the request into structured information containing:

* mood
* energy
* genres
* musical characteristics
* Spotify search terms

For example:

```json
{
  "mood": [
    "sultry",
    "smooth",
    "confident"
  ],
  "energy": "medium",
  "genres": [
    "R&B",
    "neo-soul",
    "alternative R&B"
  ],
  "characteristics": [
    "slow tempo",
    "groovy bassline",
    "syncopated rhythm",
    "rich vocals",
    "punchy drums",
    "midtempo groove"
  ],
  "search_terms": [
    "slow groove R&B",
    "midtempo neo-soul",
    "energetic slow jam R&B"
  ]
}
```

Claude is responsible for **understanding the request**, not for selecting the final Spotify tracks.

## 3. Spotify candidate search

The generated search terms are used to search Spotify for candidate tracks.

TuneAI collects the results from each search and removes duplicate Spotify track IDs.

The result is a candidate pool that can then be ranked locally.

## 4. Local recommendation ranking

TuneAI uses a deterministic ranking system rather than asking Claude to rank Spotify tracks.

The current ranking considers:

* Spotify search relevance
* how highly a track appeared in search results
* whether the artist is already among the user's top artists
* whether the track is already among the user's top tracks
* artist diversity

Tracks the user already knows receive a penalty because the goal is **music discovery**, rather than simply returning familiar music.

The final output is limited to **15 recommendations**.

## 5. Recommendation diversity

The ranking layer also prevents the recommendation list from becoming repetitive.

Currently:

* duplicate track/artist combinations are removed
* an artist can contribute a maximum of two tracks

This keeps the final list more varied.

## 6. Simple API response

The FastAPI backend exposes a simplified recommendation response rather than returning the complete Spotify track objects.

Each recommendation contains:

```json
{
  "track": "Clouded",
  "artists": "Brent Faiyaz",
  "url": "https://open.spotify.com/track/..."
}
```

The Spotify URL allows the user to open the recommended track directly in Spotify.

---

# Design Choices

## Python first

The first version was intentionally implemented as a simple Python CLI.

The CLI was used to validate the core recommendation pipeline before adding additional infrastructure.

The FastAPI backend now exposes the existing services through an API without requiring the recommendation logic to be rewritten.

## Claude for intent, Spotify for music

Claude is used to interpret the user's natural-language request.

Spotify is responsible for finding the actual music.

This separation keeps the responsibilities clear:

```text
Claude
→ Understand the user's intent

Spotify
→ Find real tracks

TuneAI
→ Rank and present the results
```

Claude does **not** generate fictional tracks or artists.

## Deterministic local ranking

The recommendation ranking is implemented locally rather than asking the LLM to choose the final recommendations.

This was chosen because it makes the ranking:

* predictable
* explainable
* easier to debug
* cheaper
* easier to improve incrementally

It also allows the AI component and recommendation logic to remain separate.

## Lightweight personalization

TuneAI uses the user's Spotify top tracks and top artists to make recommendations more relevant.

However, the current implementation deliberately keeps personalization simple rather than attempting to build a complex user profile.

The goal is to balance **familiarity with discovery**.

## No custom machine-learning model

TuneAI does not train its own recommendation model, which aligns with Spotify's rules.

The current approach combines:

* LLM-based intent extraction
* Spotify search
* deterministic local ranking

This is intentional for the MVP and keeps the system understandable within the scope of the assessment.

---

# Project Structure

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

**`api/app.py`**

Exposes the TuneAI functionality through FastAPI endpoints and handles Spotify authentication callbacks.

**`api/models.py`**

Contains the Pydantic request and response models used by the API.

**`api/ai/claude_service.py`**

Handles communication with the Anthropic API and converts natural-language requests into structured music intent.

**`api/spotify/spotify_service.py`**

Handles Spotify PKCE authentication, token refresh and Spotify Web API requests.

**`api/comp/computing_service.py`**

Coordinates the recommendation workflow by connecting Claude, Spotify and the ranking service.

**`api/comp/ranking_service.py`**

Contains the local recommendation ranking and diversity logic.

**`api/config.py`**

Loads environment variables and application configuration.

---

# API Endpoints

| Method | Endpoint           | Purpose                        |
| ------ | ------------------ | ------------------------------ |
| `GET`  | `/`                | API information                |
| `GET`  | `/health`          | Health check                   |
| `GET`  | `/auth/login`      | Start Spotify authentication   |
| `GET`  | `/auth/callback`   | Handle Spotify OAuth callback  |
| `POST` | `/recommendations` | Generate music recommendations |

FastAPI also provides interactive API documentation (Swagger) at `/docs`.

---

# Requirements

You need:

* Python 3.10+
* A Spotify account with an active Premium subscription
* A Spotify Developer application
* An Anthropic API key

The Anthropic Claude subscription and Anthropic API access are separate. The application requires an **Anthropic API key** with API access.

---

# Configuration

Create a `.env.local` file in the project root:

```env
ANTHROPIC_API_KEY=your_api_key_here
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

Do not commit `.env.local` to Git.

A `.env.example` file is included as a template.

---

# Spotify Setup

Create an application in the Spotify Developer Dashboard.

Configure the redirect URI to:

```text
http://127.0.0.1:8000/auth/callback
```

The redirect URI configured in Spotify must exactly match the value used by TuneAI.

TuneAI uses the **Authorization Code with PKCE** flow.

To authenticate:

1. Open `/auth/login`.
2. Open the returned Spotify authorization URL.
3. Authorize the application.
4. Spotify automatically redirects to `/auth/callback`.
5. TuneAI stores the resulting access and refresh tokens in memory.

No manual callback URL copying is required.

---

# Installation

Clone the repository and enter the project directory:

```bash
git clone <HTTPS or SSH repository URL>
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

# Running TuneAI

Start the FastAPI server:

```bash
uvicorn api.app:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### Authentication

Open:

```text
http://127.0.0.1:8000/auth/login
```

Authorize TuneAI with Spotify.

After authentication, recommendations can be requested through:

```text
POST /recommendations
```

Example request:

```json
{
  "request": "Slow but energetic R&B for a late-night drive."
}
```

Example response:

```json
{
  "recommendations": [
    {
      "track": "Slow Jamz",
      "artists": "Twista, Kanye West, Jamie Foxx",
      "url": "https://open.spotify.com/track/..."
    },
    {
      "track": "Clouded",
      "artists": "Brent Faiyaz",
      "url": "https://open.spotify.com/track/..."
    }
  ]
}
```

---

# Time Tracking

Time spent on each development branch is tracked below.

Update the individual branch times as development progresses and keep the total accumulated time up to date.

```text
Time spent CLI MVP: 3:11:36,44
Time spent FastAPI: 2:24:22,73
Time spent React frontend: ...
Time spent future branch: ...

Time spent total: 5:35:59,17
```

---

# Next Steps

The project is being developed incrementally.

Planned branches:

```text
CLI MVP
  ↓
FastAPI backend
  ↓
React frontend
```

The next stage will add a React frontend that consumes the existing FastAPI backend.

The recommendation logic and core services can remain unchanged.

---

# Technologies

* **Python** — core application
* **FastAPI** — backend API
* **Anthropic Claude** — natural-language music intent interpretation
* **Spotify Web API** — authentication, user taste data and music search
* **Requests** — HTTP communication
* **Pydantic** — API request and response validation
* **python-dotenv** — environment configuration
* **Uvicorn** — FastAPI development server