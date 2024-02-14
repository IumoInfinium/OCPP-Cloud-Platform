import asyncio

import arrow
import websockets
import json
from uuid import uuid4
import dataclasses
from loguru import logger

from ocpp.charge_point import snake_to_camel_case, camel_to_snake_case


from ocpp.v201.call import (
    # AuthorizePayload as CallAuthorizePayload,
    BootNotificationPayload as CallBootNotificationPayload
)


from ocpp.v20.call_result import (
    BootNotificationPayload as CallResultBootNotificationPayload,
    # HeartbeatPayload as CallResultHeartbeatPayload,
    # AuthorizePayload as CallResultAuthorizePayload,
)

# from ocpp.v16.enums import Action
from ocpp.v201.enums import Action
from manager.services.charge_points import get_charge_point

from charge_point_node.tests import init_data, charge_point_id, url, clean_tables
from core.database import get_contextual_session
from manager.services.transactions import get_transaction

id_tag: str | None = None
transaction_id: int | None = None
localAuthList = {}




async def test_boot_notification(websocket):
    async with get_contextual_session() as session:
        charge_point = await get_charge_point(session, charge_point_id)
        status = charge_point.status

    boot_notification_payload = dataclasses.asdict(
        CallBootNotificationPayload(
            reason="PowerUp",
            charging_station={
            "model":"SupreCharge001",
            "vendor_name" :"Lakebrains"
            }
        )
    )

    logger.info(boot_notification_payload)
    message_id = str(uuid4())
    temp = json.dumps([
        2,
        message_id,
        Action.BootNotification.value,
        snake_to_camel_case({k: v for k, v in boot_notification_payload.items() if not v is None})
    ])

    logger.info(f"BOOT PAYLOAD ===> {temp}")
    response = await websocket.recv()
    data = json.loads(response)
    logger.info(f"BOOT RESPONSE ===> {data}")
    assert data[0] == 3
    assert data[1] == message_id
    CallResultBootNotificationPayload(**camel_to_snake_case(data[2]))
    async with get_contextual_session() as session:
        charge_point = await get_charge_point(session, charge_point_id)
        assert status == charge_point.status


async def test_cahrging():
    account, loaction, charge_point = await init_data(charge_point_id)

    async with websockets.connect(url) as websocket:
        await test_boot_notification(websocket)
    print("\n\n ------ SUCCESS ------\n\n")


if __name__ =="__main__":
    asyncio.get_event_loop().run_until_complete(test_cahrging())