import uvicorn
from fastapi import FastAPI


from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


from app.api.endpoints.tasks import tasks_router, limiter


app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(tasks_router)

if __name__ == '__main__':
    uvicorn.run(app='main:app')