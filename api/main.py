import os
import logging
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers.file_upload_router import router as file_upload_router

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI app instance
app = FastAPI(
    title='GIO LANGCHAING GPT',
    version='1.0.0',
    description='Conversation AI with Langchaing technology'
)

# CORS middleware settings
origins = ["*"]  # Consider restricting this in a production environment

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["Root"], include_in_schema=False)
def read_root() -> RedirectResponse:
    return RedirectResponse(url="/docs/")


# Including the routers without JWT authentication
app.include_router(
    file_upload_router,
    tags=["Protected"]
)
