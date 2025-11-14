"""Entry point for running the backend server."""
import uvicorn
from backend.api.main import app


if __name__ == "__main__":
    print("Starting TX7332 PMUT Control API Server...")
    print("API Documentation: http://localhost:8000/docs")
    print("API Base URL: http://localhost:8000/api")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes during development
        log_level="info"
    )

