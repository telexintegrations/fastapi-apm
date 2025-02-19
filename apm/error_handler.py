import logging
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global error handler that logs and modifies error responses."""
    error_trace = traceback.format_exc()
    log_entry = f"[ERROR] {request.url.path} - {exc}\n{error_trace}"
    
    with open("apm/logs/apm.log") as log_file:
        log_file.write(log_entry + "\n")
    
    logger.error(log_entry)
    
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "details": "Notification sent successfully"}
    )