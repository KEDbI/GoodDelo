import uvicorn
from fastapi import FastAPI

from app.api.endpoints.tasks import tasks_router

app = FastAPI()

app.include_router(tasks_router)

if __name__ == '__main__':
    uvicorn.run(app='main:app')