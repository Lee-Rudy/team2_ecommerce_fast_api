from fastapi import FastAPI

from app.routers.Category import router as category_router

app = FastAPI(
    title="Team2 E-commerce API",
    version="0.1.0",
)

# --- Inclusion des routers ---
app.include_router(category_router)


def build_status() -> dict[str, str]:
    """Retourne le status de l'API."""
    return {"status": "ok"}


@app.get("/")
def root():
    """Endpoint racine pour vérifier que l'API fonctionne."""
    return build_status()
