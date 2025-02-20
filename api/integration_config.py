from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

integration_json = {
    "data": {
        "date": {"created_at": "2025-02-20", "updated_at": "2025-02-20"},
        "descriptions": {
            "app_name": "FastAPI APM",
            "app_description": "Modifier integration for global error handling in FastAPI applications.",
            "app_logo": "https://cdn-icons-png.flaticon.com/512/3475/3475848.png",
            "app_url": "https://fastapi-apm.onrender.com/",
            "background_color": "#f0f0f0",
        },
        "is_active": True,
        "integration_type": "modifier",
        "integration_category": "Performance Monitoring",
        "key_features": [
            "Captures all unhandled exceptions",
            "Logs errors asynchronously",
            "Prevents blocking API execution",
            "Modifies Telex messages with error details",
        ],
        "author": "Wasiu Bakare",
        "settings": [
            {
                "label": "Log Level",
                "type": "dropdown",
                "required": True,
                "default": "ERROR",
                "options": ["INFO", "WARNING", "ERROR", "CRITICAL"],
            }
        ],
        "target_url": "https://ping.telex.im/v1/webhooks/0195184b-daf9-7f90-8266-30fff9bf7591",
        "tick_url": "https://fastapi-apm.onrender.com/",
    }
}


@router.get("/integration-config")
async def get_integration_json():
    return JSONResponse(content=integration_json)
