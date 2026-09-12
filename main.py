from ai.claude_service import ClaudeService
from spotify.spotify_service import SpotifyService


def main():
    try:
        spotify_service = SpotifyService()
        spotify_service.authenticate()
        print("Successfully authenticated with Spotify!")
    except Exception as e:
        print(e)

    # claude = ClaudeService()

    # response = claude.ask(
    #     "Describe Giveon's (artist) music in three words."  # For testing purposes only
    # )

    # print(response)


if __name__ == "__main__":
    main()