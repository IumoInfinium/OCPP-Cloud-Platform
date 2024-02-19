from typing import Tuple

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import delete
from loguru import logger

from core.database import get_contextual_session
from core.queue.publisher import publish
from manager.models import AuthData, Account, ChargePoint
from ocpp.v201.datatypes import SetVariableDataType,GetVariableDataType
from manager.models.tasks.connections import DisconnectTask
# from manager.models.tasks.configuring_charging_station import SetVariableData 
from manager.services.accounts import get_account
from manager.services.charge_points import (
    get_charge_point,
    get_statuses_counts, create_charge_point, build_charge_points_query, remove_charge_point
)
from manager.utils import acquire_lock, params_extractor, paginate
from manager.views.charge_points import StatusCount, PaginatedChargePointsView, CreateChargPointView
from ocpp.v201.enums import GenericDeviceModelStatusType
from ocpp.v201.enums import ReportBaseType

charge_points_router = APIRouter(
    tags=["charge_points"]
)


@charge_points_router.post(
    "/charge_points/{charge_point_id}",
    status_code=status.HTTP_200_OK
)
async def authenticate(charge_point_id: str, data: AuthData | None = None):
    logger.info(f"Start authenticate charge point (id={charge_point_id})")
    async with get_contextual_session() as session:
        charge_point = await get_charge_point(session, charge_point_id)
        if not charge_point:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)


@charge_points_router.get(
    "/{account_id}/charge_points",
    status_code=status.HTTP_200_OK
)
async def list_charge_points(
        search: str = "",
        account: Account = Depends(get_account),
        params: Tuple = Depends(params_extractor)
) -> PaginatedChargePointsView:
    async with get_contextual_session() as session:
        items, pagination = await paginate(
            session,
            lambda: build_charge_points_query(account, search),
            *params
        )
        return PaginatedChargePointsView(items=[item[0] for item in items], pagination=pagination)


@charge_points_router.post(
    "/{account_id}/charge_points",
    status_code=status.HTTP_201_CREATED,
)
async def add_charge_point(
        data: CreateChargPointView,
        account: Account = Depends(get_account)
):
    async with get_contextual_session() as session:
        await create_charge_point(session, data)
        await session.commit()


@charge_points_router.get(
    "/{account_id}/charge_points/counters",
    status_code=status.HTTP_200_OK,
    response_model=StatusCount
)
async def get_counters(account: Account = Depends(get_account)):
    async with get_contextual_session() as session:
        return await get_statuses_counts(session, account.id)


@charge_points_router.patch(
    "/{account_id}/charge_points/{charge_point_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def disconnect(charge_point_id: str):
    await acquire_lock(charge_point_id)
    task = DisconnectTask(charge_point_id=charge_point_id)
    await publish(task.json(), to=task.exchange)


@charge_points_router.delete(
    "/{account_id}/charge_points/{charge_point_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_charge_point(
        charge_point_id: str,
        account: Account = Depends(get_account),
):
        async with get_contextual_session() as session:
            await remove_charge_point(session, charge_point_id)
            await session.commit()
            


@charge_points_router.post(
    "/{account_id}/chage_points/{charge_point_id}/variable",
    status_code=status.HTTP_200_OK,
    response_model=None
)
async def set_variable(data:SetVariableDataType):
    attribute_value = data.attribute_value
    component = data.component.name
    varibale_type = data.variable.name 
    return {"attribute_value":attribute_value,
            "component":component,
            "varibale":varibale_type
    }


@charge_points_router.get(
    "/{account_id}/chage_points/{charge_point_id}/variables",
    status_code=status.HTTP_200_OK
)
async def get_variable():
    return {"attribute_value":"string",
            "component":"Fan",
            "varibale":"RPM"
    }

# from manager.models.tasks.configuring_charging_station import BaseReport

@charge_points_router.post(
    "/{account_id}/chage_points/{charge_point_id}/baseReport",
    status_code=status.HTTP_200_OK
)
async def get_base_report(requestId: int, data:ReportBaseType):
    id = requestId
    return {"status":GenericDeviceModelStatusType.accepted,"ID":id,"report":data}


# from manager.models.tasks.configuring_charging_station import BaseReport
from ocpp.v201.enums import ResetType,ResetStatusType
from typing import Optional
# from ocpp.v201.enums import ReportBaseType
@charge_points_router.post(
    "/{account_id}/chage_points/{charge_point_id}/reset",
    status_code=status.HTTP_200_OK
)
async def reset(data:ResetType, evseId: Optional[int]=None):
    return {"status":ResetStatusType.accepted,"statusInfo":{"type":data,"evseId":evseId}}




# @charge_points_router.get(
#         "/{account_id}/charge_points/{charge_point_id}")
# async def reset_charge_point(
#     charge_point_id: str,
#     reset_type: str,
#     account : Account = Depends(get_account),
# ):
#     async with get_contextual_session() as session:
#         logger.info(f"RESET request starting ... Type : {reset_type}")
#         await acquire_lock(charge_point_id)
#         task = ResetTask(charge_point_id= charge_point_id, type=reset_type)
        
#         await publish(task.json(), to= task.exchange)
    