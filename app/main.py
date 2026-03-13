from fastapi import FastAPI
from app.routers.Category import router as category_router
from app.routers.User import router as user_router

app = FastAPI(
    title="Team2 E-commerce API",
    version="0.1.0",
)

# Inclure les routers
app.include_router(category_router)
app.include_router(user_router)


def build_status() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/")
def root():
    return build_status()
