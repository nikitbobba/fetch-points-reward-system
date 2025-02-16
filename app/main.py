from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers import receipts

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Converting FastAPI's default 422 Unprocessable Entity response to a 400 Bad Request.
    This will allow a custom detail message
    """
    return JSONResponse(
        status_code=400,
        content={"detail": "The receipt is invalid.", "errors": exc.errors()},
    )


app.include_router(receipts.router)
