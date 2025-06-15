import time
from fastapi import Request

async def monitor_middleware(request: Request, call_next):
    # Start timing
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 3)

    # Initialize if not already present
    if not hasattr(request.app.state, "request_count"):
        request.app.state.request_count = 0
    if not hasattr(request.app.state, "last_latency"):
        request.app.state.last_latency = 0.0
    if not hasattr(request.app.state, "latency_history"):
        request.app.state.latency_history = []

    # Update metrics
    request.app.state.request_count += 1
    request.app.state.last_latency = duration
    request.app.state.latency_history.append(duration)
    request.app.state.latency_history = request.app.state.latency_history[-50:]  # keep last 50

    return response
