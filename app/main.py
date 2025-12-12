from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, user, subscriptions, tokens, generate, gallery, stats

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for Cortex AI - AI Image Generation Platform",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["Authentication"])
app.include_router(user.router, prefix=f"{settings.API_PREFIX}/user", tags=["User"])
app.include_router(subscriptions.router, prefix=f"{settings.API_PREFIX}/subscriptions", tags=["Subscriptions"])
app.include_router(tokens.router, prefix=f"{settings.API_PREFIX}/tokens", tags=["Tokens"])
app.include_router(generate.router, prefix=f"{settings.API_PREFIX}/generate", tags=["Generate"])
app.include_router(gallery.router, prefix=f"{settings.API_PREFIX}/gallery", tags=["Gallery"])
app.include_router(stats.router, prefix=f"{settings.API_PREFIX}/stats", tags=["Statistics"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Cortex AI API",
        "version": settings.APP_VERSION,
        "docs": f"{settings.API_PREFIX}/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
