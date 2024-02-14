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
    # BootNotificationPayload as CallBootNotificationPayload,
    DataTransferPayload as CallDataTransferPayload
)


from ocpp.v201.call_result import (
    DataTransferPayload as CallResultDataTransferPayload,
    # BootNotificationPayload as CallResultBootNotificationPayload,
    # HeartbeatPayload as CallResultHeartbeatPayload,
    # AuthorizePayload as CallResultAuthorizePayload,
)


from ocpp.v201.enums import Action
# from manager.services.charge_points import get_charge_point

from charge_point_node.tests import init_data, charge_point_id, url, clean_tables
# from core.database import get_contextual_session
# from manager.services.transactions import get_transaction



async def test_data_transfer(websocket):
    
    vendor_id = str(uuid4()).split('-')[0]
    message_id = str(uuid4())

    data_transfer_payload = dataclasses.asdict(CallDataTransferPayload(
        vendor_id=vendor_id,
        # message_id=str(uuid4())
    ))

    logger.info(f"DATA TRANSFER ======> {data_transfer_payload}")
    
    pay = {"vendorId":"12345"}
    temp=json.dumps([
        2,
        message_id,
        Action.DataTransfer.value,
        pay
        # snake_to_camel_case({k: v for k,v in data_transfer_payload.items() if not v in None})
    ])
    logger.info(f"DATA TRANSFER PAYLOAD ====>{temp}")
    await websocket.send(json.dumps([
        2,
        message_id,
        Action.DataTransfer.value,
        pay
        # snake_to_camel_case({k: v for k,v in data_transfer_payload.items() if not v in None})
    ]))
    await asyncio.sleep(1)
    response = await websocket.recv()
    data = json.loads(response)
    logger.info(f"DATA TRANSFER RESPONSE===>{data}")
    # assert data[0] == 3
    assert data[1] == message_id
    CallResultDataTransferPayload(**camel_to_snake_case(data[2]))


async def test_cahrging():
    account, loaction, charge_point = await init_data(charge_point_id)

    async with websockets.connect(url) as websocket:
        await test_data_transfer(websocket)
    print("\n\n ------ SUCCESS ------\n\n")


if __name__ =="__main__":
    asyncio.get_event_loop().run_until_complete(test_cahrging())