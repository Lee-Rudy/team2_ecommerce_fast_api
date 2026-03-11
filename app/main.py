from fastapi import FastAPI
from app.routers.Category import router as category_router

app = FastAPI(
    title="Team2 E-commerce API",
    version="0.1.0",
)

# Inclure les routers
app.include_router(category_router)

@app.get("/")
def root():
    return {"status": "ok"}
