import os
import threading
import logging
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

TELEX_WEBHOOK_URL = os.getenv("TELEX_WEBHOOK_URL")

if not TELEX_WEBHOOK_URL:
    raise ValueError("TELEX_WEBHOOK_URL environment variable is not set!")


def log_error_async(
    route: str,
    method: str,
    error_message: str,
    stack_trace: str,
    client_ip: str,
    headers: dict,
):
    """Background job to log errors asynchronously."""
    thread = threading.Thread(
        target=_log_error,
        args=(route, method, error_message, stack_trace, client_ip, headers),
    )
    thread.daemon = True
    thread.start()


def _log_error(
    route: str,
    method: str,
    error_message: str,
    stack_trace: str,
    client_ip: str,
    headers: dict,
):
    """Writes error details to a log file asynchronously and sends it to Telex."""

    timestamp = datetime.now().isoformat()

    telex_message = (
        f"🔔 *Error at {route} ({method})*\n"
        f"❌ *Message:* {error_message}\n"
        f"🌍 *Client IP:* {client_ip}\n"
        f"🕒 *Time:* {timestamp}\n"
        f"📄 *Stack Trace (Last 3 Lines):*\n" + "\n".join(stack_trace.splitlines()[-3:])
    )

    with open("apm/logs/apm.log", "a") as log_file:
        log_entry = {
            "timestamp": timestamp,
            "route": route,
            "method": method,
            "client_ip": client_ip,
            "headers": headers,
            "error": error_message,
            "stack_trace": stack_trace.splitlines()[-3:],
        }
        log_file.write(json.dumps(log_entry) + "\n")

    logger.error(f"Logged error: {error_message}")

    try:
        response = requests.post(
            TELEX_WEBHOOK_URL,
            headers={"Content-Type": "application/json"},
            json={
                "event_name": "error_handler",
                "status": "error",
                "username": "FastAPI APM",
                "message": telex_message,
            },
        )

        if response.status_code == 202:
            logger.info("Successfully sent error to Telex")
        else:
            logger.warning(f"Failed to send error to Telex: {response.text}")

    except Exception as e:
        logger.error(f"Error sending log to Telex: {e}")
