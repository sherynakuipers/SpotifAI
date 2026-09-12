class RankingService:

    def rank_tracks(self, tracks: dict, top_tracks: list, top_artists: list) -> list:
        top_track_ids = {
            track["id"]
            for track in top_tracks
        }

        top_artist_ids = {
            artist["id"]
            for artist in top_artists
        }

        scored_tracks = []

        for track_data in tracks.values():
            track = track_data["track"]
            search_matches = track_data["search_matches"]

            score = 0

            artist_ids = {
                artist["id"]
                for artist in track["artists"]
            }

            # The track matched multiple search terms.
            score += search_matches * 10

            # The artist is already part of the user's taste.
            if artist_ids & top_artist_ids:
                score += 30

            # Avoid recommending a track the user already knows.
            if track["id"] in top_track_ids:
                score -= 20

            scored_tracks.append({
                "track": track,
                "score": score,
            })

        scored_tracks.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return scored_tracks