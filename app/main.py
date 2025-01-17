from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routes import rates
from app.utils.rate_limiter import is_rate_limited
import time

app = FastAPI()

@app.middleware("http")
async def rate_limiter_middleware(request: Request, call_next):
    client_ip = request.client.host
    max_requests = 10
    window_seconds = 60

    if is_rate_limited(client_ip, max_requests, window_seconds):
        return JSONResponse(
            status_code=429,
            content={
                "error": "Too many requests",
                "message": "Please try again later.",
                "retry_after": window_seconds,  # Optional: Include time to retry
            },
        )

    return await call_next(request)

@app.middleware("http")
async def log_requests(request: Request, call_next):

    # Start timing the request processing
    start_time = time.time()

    # Process the request
    response = await call_next(request)

    # Log the response and processing time
    process_time = time.time() - start_time

    return response

@app.get("/")
def read_root():
    return {"message": "Welcome to the Unified API!"}

app.include_router(rates.router, prefix="/api/v1")