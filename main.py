from ai.claude_service import ClaudeService
from spotify.spotify_service import SpotifyService


def main():
    spotify = SpotifyService()
    claude = ClaudeService()

    print("🎵 TuneAI\n\n")

    # === Spotify authentication ===
    print("Connecting to Spotify...")

    spotify.authenticate()

    print("✓ Successfully authenticated with Spotify!")

    # === Claude service ===
    user_request = input(
        "\nWhat are you in the mood for?\n> "
    ).strip()

    music_intent = claude.ask(user_request)

    print("\nClaude's interpretation:")
    print(music_intent)


    # === Spotify API ===
    print("\nSearching Spotify...")

    tracks = []

    for search_term in music_intent["search_terms"]:
        results = spotify.search_tracks(search_term)

        tracks.extend(results)

    print(f"✓ Found {len(tracks)} tracks.")

    for track in tracks:
        artists = ", ".join(
            artist["name"] for artist in track["artists"]
        )

        print(f"- {track['name']} — {artists}")


if __name__ == "__main__":
    main()