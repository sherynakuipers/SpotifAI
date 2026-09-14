class RankingService:
    """
    Ranks tracks based on the user's music taste and the artists they like.
    """

    def rank_tracks(self, tracks: dict, top_tracks: list, top_artists: list) -> list:
        # Track IDs the user already listens to
        top_track_ids = {
            track["id"]
            for track in top_tracks
        }

        # Artist IDs the user already listens to
        top_artist_ids = {
            artist["id"]
            for artist in top_artists
        }

        scored_tracks = []

        for track_data in tracks.values():

            track = track_data["track"]
            search_score = track_data["search_score"]

            artist_ids = {
                artist["id"]
                for artist in track["artists"]
            }

            # Start with the Spotify search relevance score
            score = search_score

            # Small personalization boost: if the user likes the artist, give them a bonus
            if artist_ids & top_artist_ids:
                score += 8

            # Penalize tracks the user already knows
            if track["id"] in top_track_ids:
                score -= 25

            scored_tracks.append({
                "track": track,
                "score": score,
            })

        # Highest score first
        scored_tracks.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        # Build the final recommendation list.
        recommendations = []

        seen_tracks = set()
        artist_counts = {}

        for item in scored_tracks:

            track = item["track"]

            track_name = track["name"].strip().lower()

            artist_names = tuple(
                artist["name"].strip().lower()
                for artist in track["artists"]
            )

            track_key = (
                track_name,
                artist_names,
            )

            # Skip duplicate track/artist combinations
            if track_key in seen_tracks:
                continue

            seen_tracks.add(track_key)

            # Keep artist diversity
            for artist in track["artists"]:
                artist_id = artist["id"]

                if artist_counts.get(artist_id, 0) >= 2:
                    break
            else:
                recommendations.append(item)

                for artist in track["artists"]:
                    artist_id = artist["id"]

                    artist_counts[artist_id] = (
                        artist_counts.get(artist_id, 0) + 1
                    )

        return recommendations