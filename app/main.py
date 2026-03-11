from fastapi import FastAPI


# test pour le pipelin ci
app = FastAPI(
    title="Team2 E-commerce API",
    version="0.1.0",
)


def build_status() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root():
    return build_status()
