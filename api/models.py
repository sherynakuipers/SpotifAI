from pydantic import BaseModel


class LoginRequest(BaseModel):
    code: str
    state: str

class LoginResponse(BaseModel):
    authorization_url: str


class RecommendationRequest(BaseModel):
    request: str


class RecommendationResponse(BaseModel):
    recommendations: list