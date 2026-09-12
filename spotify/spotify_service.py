import os
import base64
import hashlib
import requests
import webbrowser
from urllib.parse import parse_qs, urlencode, urlparse

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

from config import SPOTIFY_CLIENT_ID

class SpotifyService:

    AUTH_URL = "https://accounts.spotify.com/authorize"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    REDIRECT_URI = "http://127.0.0.1:8000/auth/callback"

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
        state = base64.urlsafe_b64encode(
            os.urandom(30)
        ).decode("utf-8")

        return state

    def _request_authorization(self, code_challenge: str, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.REDIRECT_URI,
            "scope": "user-read-private user-top-read",
            "code_challenge_method": "S256",
            "code_challenge": code_challenge,
            "state": state,
        }

        authorization_url = f"{self.AUTH_URL}?{urlencode(params)}"

        print("--> Opening authorization URL in browser...")
        webbrowser.open(authorization_url)

        return self._get_authorization_code(expected_state=state)

    def _get_authorization_code(self, expected_state: str) -> str:
        callback_url = input(
            "Paste the callback URL here:\n> "
        ).strip()

        params = parse_qs(urlparse(callback_url).query)

        if params.get("error"):
            raise RuntimeError(
                f"Spotify authorization failed: {params['error'][0]}"
            )

        state = params.get("state", [None])[0]

        if state != expected_state:
            raise RuntimeError("Spotify authorization state mismatch.")

        authorization_code = params.get("code", [None])[0]

        if not authorization_code:
            raise RuntimeError(
                "Spotify did not return an authorization code."
            )

        return authorization_code

    def _exchange_code_for_token(self, authorization_code: str, code_verifier: str,) -> None:
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

        # Testing purposes only
        if not response.ok:
            print(response.text)
            
        response.raise_for_status()

        self.access_token = response.json()["access_token"]