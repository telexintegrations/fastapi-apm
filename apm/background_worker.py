import threading
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

def log_error_async(route: str, error_message: str, stack_trace: str):
    """Background job to log errors asynchronously."""
    thread = threading.Thread(
        target=_log_error, args=(route, error_message, stack_trace)
    )
    thread.daemon = True
    thread.start()
    
def _log_error(route: str, error_message: str, stack_trace: str):
    """Writes error details to a log file asynchronously."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "route": route,
        "error": error_message,
        "stack_trace": stack_trace
    }
    
    with open("apm/logs/apm.log", "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")
    
    logger.error(f"Logged error for {route}: {error_message}")