import traceback
from fastapi import Request
from fastapi.responses import JSONResponse
from apm.background_worker import log_error_async

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global error handler that logs and modifies error responses."""
    error_trace = traceback.format_exc()
    log_error_async(request.url.path, str(exc), error_trace)
    
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "details": "Notification sent successfully"}
    )