from api.ai.claude_service import ClaudeService
from api.spotify.spotify_service import SpotifyService
from .ranking_service import RankingService


class ComputingService:
    """
    Computing service: interacts with the Claude and Spotify APIs to interpret user requests and rank tracks.
    """

    def __init__(self):
        self.spotify = SpotifyService()
        self.claude = ClaudeService()
        self.ranking = RankingService()

    def get_recommendations(self, user_request: str):
        self.spotify.authenticate()

        top_tracks = self.spotify.get_top_tracks()
        top_artists = self.spotify.get_top_artists()

        music_intent = self.claude.ask(
            user_request
        )

        tracks = {}

        for search_term in music_intent["search_terms"]:
            results = self.spotify.search_tracks(search_term, limit=10)

            for position, track in enumerate(results):
                track_id = track["id"]

                if track_id not in tracks:
                    tracks[track_id] = {
                        "track": track,
                        "search_score": 0
                    }

                search_points = max(1, len(results) - position)
                tracks[track_id]["search_score"] += search_points

        ranked_tracks = self.ranking.rank_tracks(
            tracks=tracks,
            top_tracks=top_tracks,
            top_artists=top_artists,
        )

        return ranked_tracks[:15]