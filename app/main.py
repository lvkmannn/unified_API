from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routes import rates
from app.utils.rate_limiter import is_rate_limited
from app.core.logging_config import logger

app = FastAPI()

@app.middleware("http")
async def rate_limiter_middleware(request: Request, call_next):
    client_ip = request.client.host
    max_requests = 10
    window_seconds = 60

    logger.info(f"Incoming request: {request.method} {request.url} from {client_ip}")

    if is_rate_limited(client_ip, max_requests, window_seconds):
        logger.warning(f"Rate limit exceeded for client: {client_ip}")
        return JSONResponse(
            status_code=429,
            content={
                "error": "Too many requests",
                "message": "Please try again later.",
                "retry_after": window_seconds,  # Optional: Include time to retry
            },
        )

    return await call_next(request)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Unified API!"}

app.include_router(rates.router, prefix="/api/v1")