from fastapi import APIRouter

router = APIRouter()


@router.get("/test-success")
async def test_success():
    """Simulates a successful API request."""
    return {"message": "API is running fine!"}


@router.get("/test-fail")
async def test_fail():
    """Simulates a failing API request."""
    raise Exception("Simulated Failure")
