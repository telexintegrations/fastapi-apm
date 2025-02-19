from fastapi import FastAPI
from apm.error_handler import global_exception_handler

app = FastAPI()

app.add_exception_handler(Exception, global_exception_handler)

@app.get("/test-error")
async def trigger_error():
    raise ValueError("Simulating error")