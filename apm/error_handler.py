import traceback
from fastapi import Request
from fastapi.responses import JSONResponse
from apm.background_worker import log_error_async


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global error handler that logs and modifies error responses."""

    error_trace = traceback.format_exc()
    client_ip = request.client.host if request.client else "Unknown"

    log_error_async(
        route=request.url.path,
        method=request.method,
        error_message=str(exc),
        stack_trace=error_trace,
        client_ip=client_ip,
        headers=dict(request.headers),
    )

    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"},
    )
