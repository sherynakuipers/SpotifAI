from ai.claude_service import ClaudeService


def main():
    claude = ClaudeService()

    response = claude.ask(
        "Describe Giveon's (artist) music in three words."  # For testing purposes only
    )

    print(response)


if __name__ == "__main__":
    main()