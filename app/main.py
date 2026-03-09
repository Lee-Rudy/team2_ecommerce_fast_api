from fastapi import FastAPI

app = FastAPI(
    title="Team2 E-commerce API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"status": "ok"}
