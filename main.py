from ai.claude_service import ClaudeService
from spotify.spotify_service import SpotifyService
from spotify.ranking_service import RankingService


def main():
    spotify = SpotifyService()
    claude = ClaudeService()
    ranking = RankingService()

    print("🎵 TuneAI\n")

    # === Spotify authentication ===
    print("Connecting to Spotify...")
    spotify.authenticate()
    print("✓ Successfully authenticated with Spotify!")

    # === Retrieving user music taste from Spotify ===
    print("\nLoading your music taste...")
    top_tracks = spotify.get_top_tracks()
    top_artists = spotify.get_top_artists()
    print("✓ Done!")

    # === Asking Claude for music intent ===
    user_request = input(
        "\nWhat are you in the mood for?\n> "
    ).strip()

    print("\nInterpreting your request...")
    music_intent = claude.ask(
        user_request
    )
    print("✓ Done!")

    # === Searching Spotify for tracks ===
    print("\nSearching Spotify...")

    tracks = {}

    for search_term in music_intent["search_terms"]:
        results = spotify.search_tracks(search_term)

        for track in results:
            track_id = track["id"]

            if track_id not in tracks:
                tracks[track_id] = {
                    "track": track,
                    "search_matches": 0,
                }

            tracks[track_id]["search_matches"] += 1

    print(f"✓ Found {len(tracks)} unique tracks.")

    # === Ranking Spotify tracks with Claude intent ===
    print("\nRanking recommendations...")

    ranked_tracks = ranking.rank_tracks(
        tracks=tracks,
        top_tracks=top_tracks,
        top_artists=top_artists,
    )

    print("✓ Done!")

    # === Displaying recommendations ===
    print("\n🎵 Your recommendations:\n")

    for item in ranked_tracks[:15]:
        track = item["track"]
        artists = ", ".join(
            artist["name"]
            for artist in track["artists"]
        )

        print(f"- {track['name']} — {artists} ")


if __name__ == "__main__":
    main()