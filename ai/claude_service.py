import anthropic

from config import ANTHROPIC_API_KEY


class ClaudeService:

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=ANTHROPIC_API_KEY
        )

    def ask(self, prompt: str) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-5",
            max_tokens=500,  # Adjust this value based on the desired length of the response
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.content[0].text