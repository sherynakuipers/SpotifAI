from fastapi import FastAPI

from .models import RecommendationRequest, RecommendationResponse
from .comp.computing_service import ComputingService


app = FastAPI(
    title="TuneAI API",
    description="AI-powered music discovery API",
    version="0.1.0",
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

@app.post("/recommendations", response_model=RecommendationResponse)
def recommendations(
    request: RecommendationRequest,
):
    """
    Endpoint to get Spotify recommendations based on a user request.
    """
    computing_service = ComputingService()

    results = computing_service.get_recommendations(
        request.request
    )

    return RecommendationResponse(
        recommendations=results
    )