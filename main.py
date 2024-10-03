import uvicorn
from fastapi import FastAPI


from slowapi import _rate_limit_exceeded_handler, Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.endpoints.tasks import tasks_router


app = FastAPI()
"""limiter = Limiter(key_func=get_remote_address, application_limits=['2/minute'])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)"""

app.include_router(tasks_router)

if __name__ == '__main__':
    uvicorn.run(app='main:app')