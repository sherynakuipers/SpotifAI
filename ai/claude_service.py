import anthropic
import json

from config import ANTHROPIC_API_KEY


class ClaudeService:

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=ANTHROPIC_API_KEY
        )

    def ask(self, user_request: str) -> str:
        prompt = f"""
            You are a music discovery assistant.

            Interpret the user's music request and extract the characteristics that would help a music discovery system find suitable music.

            Focus on:

            * mood
            * energy
            * genre or genres
            * musical characteristics
            * useful Spotify search terms

            Do not recommend specific songs or artists yet.

            Return ONLY valid JSON using exactly this structure:

            {{
                "mood": ["string"],
                "energy": "low | medium | high",
                "genres": ["string"],
                "characteristics": ["string"],
                "search_terms": ["string"]
            }}

            Example:

            User request:
            "I want something for a late-night drive through the city. Something atmospheric and a little melancholic, but still with enough energy to keep me awake."

            Expected output:
            {{
                "mood": ["atmospheric", "melancholic", "nocturnal"],
                "energy": "medium",
                "genres": ["electronic", "synthwave", "dream pop"],
                "characteristics": ["cinematic", "spacious", "dark", "melodic", "steady rhythm"],
                "search_terms": ["atmospheric electronic", "melancholic synthwave", "nocturnal dream pop"]
            }}

            Now interpret this user's request:

            User request:
            {user_request}
        """

        try:
            response = self.client.messages.create(
                model="claude-sonnet-5",
                max_tokens=300,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            return json.loads(response.content[0].text)
        except Exception as e:
            raise "Claude service error" + str(e)