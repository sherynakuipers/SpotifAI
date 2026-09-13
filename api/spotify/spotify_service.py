import os
import base64
import hashlib
import time
import requests

from urllib.parse import urlencode

from api.config import SPOTIFY_CLIENT_ID


class SpotifyService:
    """
    Spotify API wrapper: handles Spotify PKCE authentication, token refresh,
    and authenticated Spotify API requests.
    """

    AUTH_URL = "https://accounts.spotify.com/authorize"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    REDIRECT_URI = "http://127.0.0.1:8000/auth/callback"
    BASE_URL = "https://api.spotify.com/v1"

    SCOPES = "user-read-private user-top-read"

    def __init__(self):
        self.client_id = SPOTIFY_CLIENT_ID

        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None

        # Temporary PKCE authentication state.
        self._code_verifier = None
        self._authorization_state = None

    # === Authentication ===

    def is_authenticated(self) -> bool:
            return self.access_token is not None

    def get_authorization_url(self) -> str:
        self._code_verifier = self._generate_code_verifier()
        code_challenge = self._generate_code_challenge(self._code_verifier)
        self._authorization_state = self._generate_state()

        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.REDIRECT_URI,
            "scope": self.SCOPES,
            "code_challenge_method": "S256",
            "code_challenge": code_challenge,
            "state": self._authorization_state,
        }

        return f"{self.AUTH_URL}?{urlencode(params)}"

    def handle_callback(self, authorization_code: str, state: str) -> None:
        if state != self._authorization_state:
            raise RuntimeError(
                "Spotify authorization state mismatch."
            )

        if not self._code_verifier:
            raise RuntimeError(
                "Spotify PKCE code verifier is missing."
            )

        self._exchange_code_for_token(
            authorization_code=authorization_code,
            code_verifier=self._code_verifier,
        )

        # PKCE values are one-time authentication state.
        self._code_verifier = None
        self._authorization_state = None

    def _generate_code_verifier(self) -> str:
        code_verifier = base64.urlsafe_b64encode(
            os.urandom(64)  # Matches Spotify's 43-128 character reqirement for PKCE implementation
        ).decode("utf-8").rstrip("=")

        return code_verifier

    def _generate_code_challenge(self, code_verifier: str) -> str:
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(
                code_verifier.encode("utf-8")
            ).digest()
        ).decode("utf-8").rstrip("=")   # Strip trailing '=' characters, according to Spotify's PKCE implementation

        return code_challenge

    def _generate_state(self) -> str:
        return base64.urlsafe_b64encode(
            os.urandom(30)
        ).decode("utf-8").rstrip("=")   # Strip trailing '=' characters, according to Spotify's PKCE implementation

    def _exchange_code_for_token(self, authorization_code: str, code_verifier: str) -> None:
        response = requests.post(
            self.TOKEN_URL,
            data={
                "client_id": self.client_id,
                "grant_type": "authorization_code",
                "code": authorization_code,
                "redirect_uri": self.REDIRECT_URI,
                "code_verifier": code_verifier,
            },
        )

        response.raise_for_status()

        token_data = response.json()

        self.access_token = token_data["access_token"]
        self.refresh_token = token_data.get("refresh_token")
        self.token_expires_at = (
            time.time()
            + token_data.get("expires_in", 3600)
        )

    def _refresh_access_token(self) -> None:
        if not self.refresh_token:
            raise RuntimeError(
                "Spotify session has expired. Please log in again."
            )

        response = requests.post(
            self.TOKEN_URL,
            data={
                "client_id": self.client_id,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            },
        )

        response.raise_for_status()

        token_data = response.json()

        self.access_token = token_data["access_token"]

        # Spotify may return a new refresh token.
        if token_data.get("refresh_token"):
            self.refresh_token = token_data["refresh_token"]

        self.token_expires_at = (
            time.time()
            + token_data.get("expires_in", 3600)
        )

    def _ensure_valid_token(self) -> None:
        if not self.access_token:
            raise RuntimeError(
                "Spotify authentication required."
            )

        # Refresh one minute before expiration.
        if self.token_expires_at and time.time() >= self.token_expires_at - 60:
            self._refresh_access_token()

    # === API calls ===

    def get_top_tracks(self, limit: int = 20) -> list:
        self._ensure_valid_token()

        response = requests.get(
            f"{self.BASE_URL}/me/top/tracks",
            headers={
                "Authorization": f"Bearer {self.access_token}",
            },
            params={
                "limit": limit,
            },
        )

        response.raise_for_status()

        return response.json()["items"]

    def get_top_artists(self, limit: int = 20) -> list:
        self._ensure_valid_token()

        response = requests.get(
            f"{self.BASE_URL}/me/top/artists",
            headers={
                "Authorization": f"Bearer {self.access_token}",
            },
            params={
                "limit": limit,
            },
        )

        response.raise_for_status()

        return response.json()["items"]

    def search_tracks(self, query: str, limit: int = 10) -> list:
        self._ensure_valid_token()

        response = requests.get(
            f"{self.BASE_URL}/search",
            headers={
                "Authorization": f"Bearer {self.access_token}",
            },
            params={
                "q": query,
                "type": "track",
                "limit": limit,
            },
        )

        response.raise_for_status()

        return response.json()["tracks"]["items"]