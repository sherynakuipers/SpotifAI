from ai.claude_service import ClaudeService
from spotify.spotify_service import SpotifyService


def main():
    spotify = SpotifyService()
    claude = ClaudeService()

    spotify.authenticate()
    print("✓ Successfully authenticated with Spotify!")

    user_request = input(
        "\nWhat are you in the mood for?\n> "
    ).strip()

    response = claude.ask(user_request)

    print("\nClaude:")
    print(response)


if __name__ == "__main__":
    main()