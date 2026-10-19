"""Liveness probe ([HEALTH-PROBES]): a public route, without data."""

from fastapi import APIRouter
from pydantic import BaseModel

HEALTH_STATUS_OK = "ok"

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str


# [PERMISSIONS]: public route, without data, used as the liveness probe ([HEALTH-PROBES]).
@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(status=HEALTH_STATUS_OK)
