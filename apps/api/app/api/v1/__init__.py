"""API v1 routes."""
from fastapi import APIRouter

from app.api.v1 import accelerator, auth, career, job, resume, workflow

api_router = APIRouter()

# Each router already defines its own prefix — do NOT add prefix here again
api_router.include_router(auth.router)
api_router.include_router(resume.router)
api_router.include_router(job.router)
api_router.include_router(career.router)
api_router.include_router(accelerator.router)
api_router.include_router(workflow.router)
