from fastapi import FastAPI

from .api import tasks_api
from .db import async_engine

app = FastAPI()
app.mount("/", tasks_api)


@app.on_event("shutdown")
async def shutdown_db() -> None:
    await async_engine.dispose()
