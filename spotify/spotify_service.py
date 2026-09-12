import os
import base64
import hashlib
import requests

from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

class SpotifyService:

    AUTH_URL = "https://accounts.spotify.com/authorize"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    REDIRECT_URI = "http://127.0.0.1:8000/callback"

    def __init__(self):
        self.client_id = SPOTIFY_CLIENT_ID
        self.access_token = None

    def authenticate(self):
        code_verifier = self._generate_code_verifier()
        code_challenge = self._generate_code_challenge(code_verifier)
        state = self._generate_state()

        authorization_code = self._request_authorization(
            code_challenge=code_challenge,
            state=state,
        )

        self._exchange_code_for_token(
            authorization_code=authorization_code,
            code_verifier=code_verifier,
        )

        return self.access_token

    def _generate_code_verifier(self) -> str:
        code_verifier = base64.urlsafe_b64encode(
            os.urandom(30)
        ).decode("utf-8")

        return code_verifier

    def _generate_code_challenge(self, code_verifier: str) -> str:
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(
                code_verifier.encode("utf-8")
            ).digest()
        ).decode("utf-8")

        return code_challenge

    def _generate_state(self) -> str:
        state = base64.urlsafe_b64encode(
            os.urandom(30)
        ).decode("utf-8")

        return state

    def _request_authorization(self, code_challenge: str, state: str) -> str:
        authorization_url = f"{self.AUTH_URL}?client_id={self.client_id}&response_type=code&redirect_uri={self.REDIRECT_URI}&scope=user-read-private user-read-email&code_challenge={code_challenge}&code_challenge_method=S256&state={state}"

        response = requests.get(authorization_url)
        response.raise_for_status()

        return response.url

    def _exchange_code_for_token(self, authorization_code: str, code_verifier: str) -> None:
        token_url = f"{self.TOKEN_URL}?client_id={self.client_id}&client_secret={SPOTIFY_CLIENT_SECRET}&code={authorization_code}&code_verifier={code_verifier}&redirect_uri={self.REDIRECT_URI}&grant_type=authorization_code"

        response = requests.post(token_url)
        response.raise_for_status()

        self.access_token = response.json()["access_token"]