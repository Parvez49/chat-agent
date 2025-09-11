from fastapi import FastAPI

from app.api.v1.routes.chat_routes import router
from app.core.config import settings

common_kwargs = dict(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    contact=settings.CONTACT,
)
if settings.ENV == 'local':
    app = FastAPI(
        **common_kwargs,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        debug=True,
    )
else:
    app = FastAPI(
        **common_kwargs,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

# Register routes
app.include_router(router, prefix="/api/v1", tags=['chat'])


@app.get("/test/")
def test_app():
    return {"message": "Hellow, World!"}
