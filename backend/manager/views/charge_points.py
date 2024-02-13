from __future__ import annotations

from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel
# from ocpp.v16.enums import ChargePointStatus
from ocpp.v201.enums import ConnectorStatusType

from manager.views import PaginationView
from manager.views.locations import SimpleLocation


class ConnectorView(BaseModel):
    # status: ChargePointStatus
    status : ConnectorStatusType


class ChargePointUpdateStatusView(BaseModel):
    # status: ChargePointStatus
    status: ConnectorStatusType
    connectors: Dict | None = None


class StatusCount(BaseModel):
    available: int = 0
    offline: int = 0
    reserved: int = 0
    charging: int = 0


class CreateChargPointView(BaseModel):
    location_id: str
    id: str
    manufacturer: str
    serial_number: str
    model: str
    password: str | None = None
    comment: str | None = None


class SimpleChargePoint(BaseModel):
    id: str
    # status: ChargePointStatus
    status: ConnectorStatusType
    model: str
    updated_at: datetime | None = None
    location: SimpleLocation

    class Config:
        orm_mode = True


class PaginatedChargePointsView(BaseModel):
    items: List[SimpleChargePoint]
    pagination: PaginationView
