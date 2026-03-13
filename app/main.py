from fastapi import FastAPI

from app.routers.category import router as category_router
from app.routers.route_auth import router as auth_router
from app.routers.route_product import router as product_router
from app.routers.route_stock_movement import router as stock_movement_router
from app.routers.User import router as user_router

app = FastAPI(
    title="Team2 E-commerce API",
    version="0.1.0",
)

app.include_router(category_router)
app.include_router(product_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(stock_movement_router)


def build_status() -> dict[str, str]:
    """Generate API status response.

    Returns:
        Dict containing the API status.
    """
    return {"status": "ok"}


@app.get("/")
def root():
    """Root endpoint returning API health status.

    Returns:
        Dict with status information.
    """
    return build_status()
