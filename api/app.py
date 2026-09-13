from fastapi import FastAPI, Query, HTTPException

from .models import (
    RecommendationRequest,
    RecommendationResponse,
    LoginRequest,
    LoginResponse,
)
from .spotify.spotify_service import SpotifyService
from .ai.claude_service import ClaudeService
from .comp.computing_service import ComputingService, RankingService


app = FastAPI(
    title="TuneAI",
    description="AI-powered music discovery",
)

spotify = SpotifyService()
claude = ClaudeService()
ranking = RankingService()

computing_service = ComputingService(
    spotify=spotify,
    claude=claude,
    ranking=ranking,
)


@app.get("/")
def root():
    return {
        "message": "TuneAI API is running"
    }

@app.get("/health")
def health():
    """
    Endpoint to check the health of the API.
    """

    return {
        "status": "ok"
    }

@app.get("/auth/login", response_model=LoginResponse)
def login():
    """
    Endpoint to initiate the Spotify authorization flow.
    """

    url = spotify.get_authorization_url()

    return LoginResponse(
        authorization_url=url
    )

@app.get("/auth/callback")
def callback(
    code: str,
    state: str,
):
    """
    Endpoint to handle the callback from the Spotify authorization flow.
    """
    try:
        spotify.handle_callback(
            authorization_code=code,
            state=state,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return {
        "message": "Successfully authenticated with Spotify!"
    }

@app.post("/recommendations", response_model=RecommendationResponse)
def recommendations(
    request: RecommendationRequest,
):
    """
    Endpoint to get Spotify recommendations based on a user request.
    """
    if not spotify.is_authenticated():
        raise HTTPException(
            status_code=401,
            detail="Spotify authentication required. Open /auth/login first."
        )

    try:
        results = computing_service.get_recommendations(
            request.request
        )

        return RecommendationResponse(
            recommendations=results
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )