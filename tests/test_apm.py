import pytest
import json
import os
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from apm.background_worker import _log_error
from apm.error_handler import global_exception_handler
from fastapi import Request
from starlette.exceptions import HTTPException

client = TestClient(app)


@pytest.fixture
async def sample_request():
    """Creates a properly structured mock FastAPI request object."""
    return Request(
        scope={
            "type": "http",
            "method": "GET",
            "path": "/test",
            "headers": [(b"user-agent", b"pytest")],
        }
    )


@pytest.mark.asyncio
async def test_error_handler_catches_exception(sample_request):
    """Ensure the global exception handler catches and processes exceptions correctly."""
    exc = HTTPException(status_code=500, detail="Test error")

    response = await global_exception_handler(sample_request, exc)

    assert response.status_code == 500
    assert json.loads(response.body.decode("utf-8")) == {
        "error": "Internal Server Error"
    }


@patch("apm.background_worker.requests.post")
def test_log_error_sends_webhook(mock_post):
    """Ensure errors are logged and a webhook is triggered."""
    mock_post.return_value.status_code = 202
    route = "/test-route"
    method = "GET"
    error_message = "Test Error"
    stack_trace = "Traceback: Example error"
    client_ip = "127.0.0.1"
    headers = {"User-Agent": "pytest"}

    log_file_path = "apm/logs/apm.log"

    if os.path.exists(log_file_path):
        os.remove(log_file_path)

    _log_error(route, method, error_message, stack_trace, client_ip, headers)

    assert os.path.exists(log_file_path)

    with open(log_file_path, "r") as log_file:
        log_data = json.loads(log_file.readlines()[-1])
        assert log_data["route"] == route
        assert log_data["method"] == method
        assert log_data["error"] == error_message

    mock_post.assert_called_once()


@patch("apm.background_worker.requests.post")
def test_log_error_handles_webhook_failure(mock_post):
    """Test webhook failure handling."""
    mock_post.side_effect = Exception("Webhook Failed")

    route = "/test-route"
    method = "POST"
    error_message = "Another Error"
    stack_trace = "Traceback: Example error"
    client_ip = "192.168.1.1"
    headers = {"User-Agent": "pytest"}

    _log_error(route, method, error_message, stack_trace, client_ip, headers)

    mock_post.assert_called_once()
