from typing import Union
from fastapi import FastAPI
from database import create_database

from routes.authentication import router as auth_router
from routes.version import router as version_router
from routes.upload import router as upload_router
from routes.files import router as files_router 
from routes.query import router as query_router
from routes.delete import router as delete_router

create_database()

app = FastAPI()

app.include_router(version_router, prefix="/api/v1", tags=["version"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(upload_router, prefix="/api/v1", tags=["upload"])
app.include_router(files_router, prefix="/api/v1", tags=["files"])
app.include_router(query_router, prefix="/api/v1", tags=["query"])
app.include_router(delete_router, prefix="/api/v1", tags=["delete"])