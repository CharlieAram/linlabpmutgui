"""Configuration management API endpoints."""
from fastapi import APIRouter, HTTPException
from backend.api.models.config import (
    DeviceConfig,
    ConfigSaveRequest,
    ConfigLoadRequest,
    ConfigListResponse,
    ConfigListItem
)
from backend.api.models.device import ApiResponse
from backend.services.config_service import ConfigService


router = APIRouter(prefix="/api/config", tags=["config"])

# Config service instance
config_service = ConfigService()


@router.post("/save", response_model=ApiResponse)
async def save_config(request: ConfigSaveRequest):
    """Save current configuration to file."""
    try:
        # Convert Pydantic model to dict
        config_dict = request.config.model_dump(mode='json')
        
        success = config_service.save_config(request.filename, config_dict)
        
        if success:
            return ApiResponse(
                success=True,
                message=f"Configuration saved to {request.filename}",
                data={"filename": request.filename}
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to save configuration")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Save error: {str(e)}")


@router.post("/load", response_model=DeviceConfig)
async def load_config(request: ConfigLoadRequest):
    """Load configuration from file."""
    try:
        config_dict = config_service.load_config(request.filename)
        
        if config_dict is None:
            raise HTTPException(status_code=404, detail="Configuration file not found")
        
        # Convert dict to Pydantic model
        config = DeviceConfig(**config_dict)
        return config
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Load error: {str(e)}")


@router.get("/list", response_model=ConfigListResponse)
async def list_configs():
    """List all saved configurations."""
    try:
        configs = config_service.list_configs()
        return ConfigListResponse(
            configs=[ConfigListItem(**config) for config in configs]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"List error: {str(e)}")


@router.delete("/{filename}", response_model=ApiResponse)
async def delete_config(filename: str):
    """Delete a configuration file."""
    try:
        success = config_service.delete_config(filename)
        
        if success:
            return ApiResponse(
                success=True,
                message=f"Configuration {filename} deleted",
                data={"filename": filename}
            )
        else:
            raise HTTPException(status_code=404, detail="Configuration file not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete error: {str(e)}")


@router.get("/export/{filename}")
async def export_config(filename: str):
    """Export configuration as downloadable JSON."""
    try:
        config_dict = config_service.load_config(filename)
        
        if config_dict is None:
            raise HTTPException(status_code=404, detail="Configuration file not found")
        
        return config_dict
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")

