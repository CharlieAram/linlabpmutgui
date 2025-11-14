"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routers import device, channels, beamforming, patterns, config


# Create FastAPI app
app = FastAPI(
    title="TX7332 PMUT Control API",
    description="REST API for controlling TX7332 PMUT device",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(device.router)
app.include_router(channels.router)
app.include_router(beamforming.router)
app.include_router(patterns.router)
app.include_router(config.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "TX7332 PMUT Control API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

