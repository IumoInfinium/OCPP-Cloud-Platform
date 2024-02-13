import asyncio

import arrow
import websockets
import json
from uuid import uuid4
import dataclasses
from loguru import logger

from ocpp.charge_point import snake_to_camel_case, camel_to_snake_case
# from ocpp.v16.call import (
#     AuthorizePayload as CallAuthorizePayload,
#     BootNotificationPayload as CallBootNotificationPayload,
#     StartTransactionPayload as CallStartTransactionPayload,
#     StopTransactionPayload as CallStopTransactionPayload,
#     MeterValuesPayload as CallMeterValuesPayload
# )


from ocpp.v201.call import (
    AuthorizePayload as CallAuthorizePayload
)
# from ocpp.v16.call_result import (
#     BootNotificationPayload as CallResultBootNotificationPayload,
#     HeartbeatPayload as CallResultHeartbeatPayload,
#     AuthorizePayload as CallResultAuthorizePayload,
#     StartTransactionPayload as CallResultStartTransactionPayload,
#     StopTransactionPayload as CallResultStopTransactionPayload,
# )
from ocpp.v20.call_result import (
    BootNotificationPayload as CallResultBootNotifcationPayload,
    HeartbeatPayload as CallResultHeartbeatPayload,
    AuthorizePayload as CallResultAuthorizePayload,
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
# localAuthList = {'12345678':'Accepted'}


# async def local_auth(websocket, account, location, charge_point):
#     RFID='12345678999'
# ### something is present in local authentication
#     if len(localAuthList) != 0 and RFID in localAuthList.keys():
#         # for key, value in localAuthList.items():
#         assert localAuthList[RFID] == "Accepted"
#         logger.info(f"STAT CHARGING WITHOUT SENDING AUTH REQ TO SERVER")
#         await test_start_transaction(websocket, account, location, charge_point, RFID)
#         await test_stop_transaction(websocket, account, location, charge_point)
#     else:
#         if len(localAuthList) == 0:
#             RFID = str(uuid4()).split("-")[0]
#         logger.info(f"NOT FOUND IN LOCAL AUTH LIST")
#         await test_authorize(websocket, account, location, charge_point, RFID)
#     # else:
#     #     await test_authorize(websocket, account, location, charge_point, RFID)
        

async def test_authorize(websocket, account, location, charge_point, RFID):

    id_=RFID

    authorize_payload = dataclasses.asdict(CallAuthorizePayload(
        id_token= {
            "idToken" : "A1B2C3D4",
            "type" : "ISO15693"
        }
    ))

    message_id = str(uuid4())
    temp=json.dumps([
        2,
        message_id,
        Action.Authorize.value,
        snake_to_camel_case({k: v for k, v in authorize_payload.items() if not v is None})
    ])
    logger.info(f"PALYLOAD====>{temp}")
    await websocket.send(json.dumps([
        2,
        message_id,
        Action.Authorize,
        snake_to_camel_case({k: v for k, v in authorize_payload.items() if not v is None})
    ]))
    await asyncio.sleep(1)
    response = await websocket.recv()
    data = json.loads(response)
    logger.info(f"DATA===>{data}")
    assert data[0] == 3
    assert data[1] == message_id
    if data[2]["idTagInfo"]['status'] == "Accepted":
        logger.info(f"Auth list before ==> {localAuthList}")
        localAuthList[id_] = "Accepted"
        logger.info(f"Auth list after ==> {localAuthList}")

    
    CallResultAuthorizePayload(**camel_to_snake_case(data[2]))

# async def test_start_transaction(websocket, account, location, charge_point, RFID):
#     global transaction_id
#     global id_tag

#     # id_tag = str(uuid4()).split("-")[0]
#     id_tag = RFID
#     meter_start = 1000

#     start_transaction_payload = dataclasses.asdict(CallStartTransactionPayload(
#         connector_id=1,
#         id_tag=id_tag,
#         meter_start=meter_start,
#         timestamp=arrow.get().isoformat()
#     ))

#     message_id = str(uuid4())
#     temp = json.dumps([
#         2,
#         message_id,
#         Action.StartTransaction.value,
#         snake_to_camel_case({k: v for k, v in start_transaction_payload.items() if not v is None})
#     ])
#     logger.info(f"START PALYLOAD====>{temp}")
#     await websocket.send(json.dumps([
#         2,
#         message_id,
#         Action.StartTransaction.value,
#         snake_to_camel_case({k: v for k, v in start_transaction_payload.items() if not v is None})
#     ]))
#     await asyncio.sleep(1)
#     response = await websocket.recv()
#     data = json.loads(response)
#     logger.info(f"START RESPONSE====>{data}")
#     assert data[0] == 3
#     assert data[1] == message_id
#     payload = CallResultStartTransactionPayload(**camel_to_snake_case(data[2]))
#     transaction_id = payload.transaction_id

#     async with get_contextual_session() as session:
#         transaction = await get_transaction(session, payload.transaction_id)
#         assert transaction.account_id == account.id
#         assert transaction.city == location.city
#         assert transaction.address == location.address1
#         assert transaction.charge_point == charge_point.id
#         assert transaction.meter_start == meter_start
#         assert not transaction.meter_stop

# async def test_meter_values(websocket):
#     meter_values_payload = dataclasses.asdict(CallMeterValuesPayload(
#         connector_id=1,
#         transaction_id=123,
#         meter_value=[
#             {
#                 "timestamp": arrow.get().isoformat(),
#                 "sampled_value": [
#                     {"value": "4567.45"}
#                 ]
#             }
#         ]
#     ))
#     message_id = str(uuid4())
#     await websocket.send(json.dumps([
#         2,
#         message_id,
#         Action.MeterValues.value,
#         snake_to_camel_case({k: v for k, v in meter_values_payload.items() if not v is None})
#     ]))
#     await asyncio.sleep(1)
#     response = await websocket.recv()
#     data = json.loads(response)
#     assert data[0] == 3
#     assert data[1] == message_id
#     assert not data[2]

# async def test_stop_transaction(websocket, account, location, charge_point):

#     meter_stop = 1200
#     stop_transaction_payload = dataclasses.asdict(CallStopTransactionPayload(
#         meter_stop=meter_stop,
#         id_tag=id_tag,
#         timestamp=arrow.get().isoformat(),
#         transaction_id=transaction_id
#     ))

#     message_id = str(uuid4())
    
#     temp =json.dumps([
#         2,
#         message_id,
#         Action.StopTransaction.value,
#         snake_to_camel_case({k: v for k, v in stop_transaction_payload.items() if not v is None})
#     ])
#     logger.info(f"STOP PALYLOAD====>{temp}")
#     await websocket.send(json.dumps([
#         2,
#         message_id,
#         Action.StopTransaction.value,
#         snake_to_camel_case({k: v for k, v in stop_transaction_payload.items() if not v is None})
#     ]))
#     await asyncio.sleep(1)
#     response = await websocket.recv()
#     data = json.loads(response)
#     logger.info(f"STOP RESPONSE====>{data}")
#     assert data[0] == 3
#     assert data[1] == message_id
#     CallResultStopTransactionPayload(**camel_to_snake_case(data[2]))

#     async with get_contextual_session() as session:
#         transaction = await get_transaction(session, transaction_id)
#         assert transaction.account_id == account.id
#         assert transaction.city == location.city
#         assert transaction.address == location.address1
#         assert transaction.charge_point == charge_point.id
#         assert transaction.meter_stop == meter_stop
#         assert transaction.meter_stop >= transaction.meter_start

async def test_heartbeat(websocket):

    message_id = str(uuid4())
    await websocket.send(json.dumps([
        2,
        message_id,
        Action.Heartbeat.value,
        {}
    ]))
    await asyncio.sleep(1)
    response = await websocket.recv()
    data = json.loads(response)
    assert data[0] == 3
    assert data[1] == message_id
    CallResultHeartbeatPayload(**camel_to_snake_case(data[2]))
    
async def test_boot_notification(websocket):
    async with get_contextual_session() as session:
        charge_point = await get_charge_point(session, charge_point_id)
        status = charge_point.status

    boot_notification_payload = dataclasses.asdict(CallBootNotificationPayload(
        charge_point_model="test_model",
        charge_point_vendor="test_vendor",
    ))

    message_id = str(uuid4())
    await websocket.send(json.dumps([
        2,
        message_id,
        Action.BootNotification.value,
        snake_to_camel_case({k: v for k, v in boot_notification_payload.items() if not v is None})
    ]))

    response = await websocket.recv()
    data = json.loads(response)
    assert data[0] == 3
    assert data[1] == message_id
    CallResultBootNotificationPayload(**camel_to_snake_case(data[2]))
    async with get_contextual_session() as session:
        charge_point = await get_charge_point(session, charge_point_id)
        assert status == charge_point.status



async def test_charging():
    account, location, charge_point = await init_data(charge_point_id)

    async with websockets.connect(url) as websocket:
        # await local_auth(websocket, account, location, charge_point)
        await test_authorize(websocket, account, location, charge_point)
        await asyncio.sleep(1)
        # await test_boot_notification(websocket)
        # await asyncio.sleep(1)
        # await test_start_transaction(websocket, account, location, charge_point)
        # await asyncio.sleep(5)
        # await test_meter_values(websocket)
        # await asyncio.sleep(1)
        # await test_heartbeat(websocket)
        # await asyncio.sleep(1)
        # await test_stop_transaction(websocket, account, location, charge_point)
        # await asyncio.sleep(5)

    # await clean_tables(account, location, charge_point)

    print("\n\n --- SUCCESS ---")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(test_charging())