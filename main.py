from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI
from app.api.routes import query
import asyncio

from app.utils.logger import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)

app = FastAPI()
app.include_router(query.router)


async def run_server():
    config = uvicorn.Config(app,
                            host="0.0.0.0",
                            log_level="info",
                            log_config=LOGGING_CONFIG,
                            port=8001,
                            )
    server = uvicorn.Server(config)
    await server.serve()




if __name__ == "__main__":
    asyncio.run(run_server())
