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
    title="TuneAI API",
    description="AI-powered music discovery API",
    version="0.1.0",
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
    login_request: LoginRequest,
):
    """
    Endpoint to handle the callback from the Spotify authorization flow.
    """

    spotify.handle_callback(
        code=login_request.code,
        state=login_request.state,
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
            detail="Spotify authentication required."
        )
    
    computing_service = ComputingService()

    results = computing_service.get_recommendations(
        request.request
    )

    return RecommendationResponse(
        recommendations=results
    )