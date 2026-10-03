from fastapi import FastAPI

app = FastAPI(title="Mars Explorer Lab (proyecto de práctica)")


@app.get("/health")
def health():
    """Comprobación mínima de que la API está viva."""
    return {"status": "ok"}
