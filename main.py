from fastapi import FastAPI
from apm.error_handler import global_exception_handler
from api.routes import router
import logging

app = FastAPI()

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(router)

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
