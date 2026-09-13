from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    request: str


class RecommendationResponse(BaseModel):
    recommendations: list