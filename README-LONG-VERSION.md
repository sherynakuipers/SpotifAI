# TuneAI 🎵

TuneAI is an AI-powered music discovery application that combines the **Spotify Web API** with **Anthropic Claude** to turn a natural-language music request into personalized music recommendations.

For example, a user can enter:

> "I want something slow but energetic, maybe R&B for a late-night drive."

TuneAI interprets the request, searches Spotify for relevant tracks, and ranks the results based on search relevance and the user's existing Spotify listening data.

## Current version

This version contains the **CLI MVP** of TuneAI.

The goal of this version was to validate the core recommendation flow before introducing a web API or frontend.

### Current flow

```text
User request
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

## What I've Built

### 1. Spotify authentication

TuneAI authenticates the user with Spotify using the **Authorization Code with PKCE** flow.

The CLI opens Spotify's authorization page in the browser. After authorization, the user pastes the callback URL back into the application.

The application requests the following scopes:

* `user-read-private`
* `user-top-read`

The `user-top-read` scope allows TuneAI to access the user's top tracks and artists for lightweight personalization.

### 2. Natural-language music interpretation

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

### 3. Spotify candidate search

The generated search terms are used to search Spotify for candidate tracks.

TuneAI collects the results from each search and removes duplicate Spotify track IDs.

The result is a candidate pool that can then be ranked locally.

### 4. Local recommendation ranking

TuneAI uses a deterministic ranking system rather than asking Claude to rank Spotify tracks.

The current ranking considers:

* Spotify search relevance
* how highly a track appeared in search results
* whether the artist is already among the user's top artists
* whether the track is already among the user's top tracks
* artist diversity

Tracks the user already knows receive a penalty because the goal is **music discovery**, rather than simply returning familiar music.

The final output is limited to **15 recommendations**.

### 5. Recommendation diversity

The ranking layer also prevents the recommendation list from becoming repetitive.

Currently:

* duplicate track/artist combinations are removed
* an artist can contribute a maximum of two tracks

This keeps the final list more varied.

---

# Design Choices

## Python first

The first version is intentionally implemented as a simple Python CLI.

The goal of this branch is to validate the core recommendation pipeline before adding additional infrastructure.

A web API and frontend can be added later without changing the core services significantly.

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
tuneai/
├── main.py
├── config.py
├── .env.local
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
│   └── spotify_service.py
```

### Responsibilities

**`main.py`**

Coordinates the complete CLI workflow.

**`ai/claude_service.py`**

Handles communication with the Anthropic API and converts natural-language requests into structured music intent.

**`spotify/spotify_service.py`**

Handles Spotify authentication and Spotify Web API requests.

**`spotify/ranking_service.py`**

Contains the local recommendation ranking and diversity logic.

**`config.py`**

Loads environment variables and application configuration.

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

The current CLI implementation uses PKCE and a manual callback step rather than running a local callback server.

After Spotify authorization, the browser will redirect to the callback URL. Copy the complete callback URL and paste it into the CLI when prompted.

---

# Installation

Clone the repository and enter the project directory:

```bash
git clone <HTTPS or SSH repository URL>
cd tuneai
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

Run:

```bash
python main.py
```

The application will:

1. Authenticate with Spotify.
2. Load the user's top tracks and artists.
3. Ask what they are in the mood for.
4. Send the request to Claude for interpretation.
5. Search Spotify using the generated search terms.
6. Rank the candidate tracks.
7. Display 15 recommendations.

Example:

```text
🎵 TuneAI

Connecting to Spotify...
✓ Successfully authenticated with Spotify!

Loading your music taste...
✓ Done!

What are you in the mood for?
> Slow but energetic RnB.

Interpreting your request...
✓ Done!

Searching Spotify...
✓ Found 29 unique tracks.

Ranking recommendations...
✓ Done!

🎵 Your recommendations:

- Slow Jamz — Twista, Kanye West, Jamie Foxx
- Clouded — Brent Faiyaz
- ...
```

---

# Time Tracking

Time spent on each development branch is tracked below.

Update the individual branch times as development progresses and keep the total accumulated time up to date.

```text
Time spent CLI MVP: 3:11:36,44
Time spent FastAPI: ...
Time spent React frontend: ...
Time spent future branch: ...

Time spent total: 3:11:36,44
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

The next stage will expose the existing TuneAI functionality through a FastAPI backend.

The React frontend can then consume the API without requiring the recommendation logic to be rewritten.

---

# Technologies

* **Python** — core application
* **Anthropic Claude** — natural-language music intent interpretation
* **Spotify Web API** — authentication, user taste data, and music search
* **Requests** — HTTP communication
* **python-dotenv** — environment configuration