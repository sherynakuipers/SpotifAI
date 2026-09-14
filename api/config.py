import os

from dotenv import load_dotenv

load_dotenv("api/.env.local")

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]