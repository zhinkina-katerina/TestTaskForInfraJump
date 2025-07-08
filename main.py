from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes import query
import asyncio

from app.errors import (sqlalchemy_exception_handler,
                        generic_exception_handler,
                        http_exception_handler)
from app.utils.logger import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)

app = FastAPI()
app.include_router(query.router)

app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
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
