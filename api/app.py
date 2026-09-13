from fastapi import FastAPI

app = FastAPI(
    title="TuneAI API",
    description="AI-powered music discovery API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "TuneAI API is running"
    }

@app.get("/health")
def health():
    # Endpoint to check if the API is running
    return {
        "status": "ok"
    }