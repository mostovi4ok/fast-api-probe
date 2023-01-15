from fastapi import FastAPI

from .db import async_engine
from .api import tasks_api


app = FastAPI()
app.mount("/", tasks_api)


@app.on_event("shutdown")
async def shutdown_db() -> None:
    await async_engine.dispose()
