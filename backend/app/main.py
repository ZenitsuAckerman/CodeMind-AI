import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.core.logging import setup_logging
from app.api.v1.api import api_router
from app.api import health

# Configure logging at startup
setup_logging(debug=settings.DEBUG)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        description="CodeMind AI - Engineering Knowledge Workspace API",
    )

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict this in production!
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router, tags=["health"])
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/", tags=["root"])
    async def root():
        """Root endpoint returning basic application metadata."""
        return {
            "name": settings.PROJECT_NAME,
            "status": "running"
        }

    return app

app = create_app()
