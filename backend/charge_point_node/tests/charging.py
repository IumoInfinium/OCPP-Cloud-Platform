import asyncio

import arrow
import websockets
import json
from uuid import uuid4
import dataclasses
from loguru import logger

from ocpp.charge_point import snake_to_camel_case, camel_to_snake_case

from ocpp.v201.call import (
    AuthorizePayload as CallAuthorizePayload,
    BootNotificationPayload as CallBootNotificationPayload,
    StatusNotificationPayload as CallStatusNotificationPayload,
    NotifyEventPayload as CallNotifyEventPayload,
)

from ocpp.v20.call_result import (
    BootNotificationPayload as CallResultBootNotificationPayload,
    HeartbeatPayload as CallResultHeartbeatPayload,
    AuthorizePayload as CallResultAuthorizePayload,
    StatusNotificationPayload as CallResultStatusNotificationPayload,
    NotifyEventPayload as CallResultNotifyEventPayload,
)

from core.utils import get_utc_as_string
from ocpp.v201.enums import Action, ConnectorStatusType
from ocpp.v201 import enums as  OCPPEnums
from manager.services.charge_points import get_charge_point

from charge_point_node.tests import init_data, charge_point_id, url, clean_tables
from core.database import get_contextual_session
from manager.services.transactions import get_transaction

id_tag: str | None = None
transaction_id: int | None = None
heartbeat_interval = 5
heartbeat_start = False

async def test_authorize(websocket):

    authorize_payload = dataclasses.asdict(CallAuthorizePayload(
        id_token= {
            "id_token" : "A1B2C3D4",
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
    logger.info(f"AUTH PALYLOAD====>{temp}")
    await websocket.send(json.dumps([
        2,
        message_id,
        Action.Authorize,
        snake_to_camel_case({k: v for k, v in authorize_payload.items() if not v is None})
    ]))
    await asyncio.sleep(1)
    response = await websocket.recv()
    data = json.loads(response)
    logger.info(f"AUTH DATA===>{data}")
    assert data[0] == 3
    assert data[1] == message_id
    CallResultAuthorizePayload(**camel_to_snake_case(data[2]))


async def test_boot_notification(websocket):
    async with get_contextual_session() as session:
        charge_point = await get_charge_point(session, charge_point_id)
        status = charge_point.status

    message_id = str(uuid4())
    
    boot_notification_payload = dataclasses.asdict(CallBootNotificationPayload(
        reason = "PowerUp",
        charging_station={
            "model":"SupreCharge001",
            "vendor_name" :"Lakebrains"
        }
    ))

    temp = json.dumps([
            2,
            message_id,
            Action.BootNotification.value,
            snake_to_camel_case({k: v for k, v in boot_notification_payload.items() if not v is None})
    ])
    logger.info(f"BOOT PAYLOAD ===> {temp}")
    await websocket.send(json.dumps([
        2,
        message_id,
        Action.BootNotification.value,
        snake_to_camel_case({k: v for k, v in boot_notification_payload.items() if not v is None})
    ]))

    response = await websocket.recv()
    data = json.loads(response)
    logger.info(f"BOOT RESPONSE ===> {data}")
    assert data[0] == 3
    assert data[1] == message_id
    CallResultBootNotificationPayload(**camel_to_snake_case(data[2]))
    
    async with get_contextual_session() as session:
        charge_point = await get_charge_point(session, charge_point_id)
        assert status == charge_point.status

# async def test_start_transaction(websocket, account, location, charge_point):
#     global transaction_id
#     global id_tag

#     id_tag = str(uuid4()).split("-")[0]
#     meter_start = 1000

#     start_transaction_payload = dataclasses.asdict(CallStartTransactionPayload(
#         connector_id=1,
#         id_tag=id_tag,
#         meter_start=meter_start,
#         timestamp=arrow.get().isoformat()
#     ))

#     message_id = str(uuid4())
#     await websocket.send(json.dumps([
#         2,
#         message_id,
#         Action.StartTransaction.value,
#         snake_to_camel_case({k: v for k, v in start_transaction_payload.items() if not v is None})
#     ]))
#     await asyncio.sleep(1)
#     response = await websocket.recv()
#     data = json.loads(response)
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
#     await websocket.send(json.dumps([
#         2,
#         message_id,
#         Action.StopTransaction.value,
#         snake_to_camel_case({k: v for k, v in stop_transaction_payload.items() if not v is None})
#     ]))
#     await asyncio.sleep(1)
#     response = await websocket.recv()
#     data = json.loads(response)
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
    """
    HeartBeat Function
    """
    message_id = str(uuid4())
    await websocket.send(json.dumps([
        2,
        message_id,
        Action.Heartbeat,
        {}
    ]))
    logger.info("HeartBeat Sent >>>")
    await asyncio.sleep(1)
    response = await websocket.recv()
    data = json.loads(response)
    
    logger.info(f"Heartbeat Payload received -> {data}")
    assert data[0] == 3
    assert data[1] == message_id
    
    logger.info("HeartBeat Received <<<")
    CallResultHeartbeatPayload(**camel_to_snake_case(data[2]))

async def test_status_notification(websocket):
    """
    Send Status Notification to CSMS
    """
    
    status_notification_payload = dataclasses.asdict(CallStatusNotificationPayload(
        connector_id= 1,
        connector_status= ConnectorStatusType.available,
        evse_id=1,
        timestamp=get_utc_as_string()
    ))

    message_id = str(uuid4())
    temp=json.dumps([
        2,
        message_id,
        Action.StatusNotification,
        snake_to_camel_case({k: v for k, v in status_notification_payload.items() if not v is None})
    ])
    logger.info(f"STATUS NOTIFICATION PAYLOAD====>{temp}")
    await websocket.send(json.dumps([
        2,
        message_id,
        Action.StatusNotification,
        snake_to_camel_case({k: v for k, v in status_notification_payload.items() if not v is None})
    ]))
    await asyncio.sleep(1)
    response = await websocket.recv()
    data = json.loads(response)
    
    assert data[0] == 3
    assert data[1] == message_id
    logger.info(f"STATUS NOTIFICATION DATA===>{data}")
    CallResultStatusNotificationPayload(**camel_to_snake_case(data[2]))


async def test_notify_event(websocket):
    """
    Notify event to CSMS
    """
    
    event_id = 0
    notify_event_payload = dataclasses.asdict(CallNotifyEventPayload(
        generated_at= get_utc_as_string(),
        seq_no=0,
        event_data= [
            {
                "event_id" : event_id,
                "timestamp": get_utc_as_string(),
                "trigger": OCPPEnums.EventTriggerType.alerting,
                "actualValue": "0",
                "event_notification_type": OCPPEnums.EventNotificationType.hard_wired_notification,
                "component": {
                    "name": "AirCoolingSystem",
                },
                "variable": {
                    "name": "FanSpeed",
                }
            },
            {
                "eventId": event_id + 1,
                "timestamp": get_utc_as_string(),
                "trigger": OCPPEnums.EventTriggerType.alerting,
                "actualValue": "F-0.1.0",
                "event_notification_type": OCPPEnums.EventNotificationType.hard_wired_notification,
                "component": {
                    "name": "AirCoolingSystem"
                },
                "variable": {
                    "name": "Problem"
                }
            }
        ]
    ))

    message_id = str(uuid4())
    temp=json.dumps([
        2,
        message_id,
        Action.NotifyEvent,
        snake_to_camel_case({k: v for k, v in notify_event_payload.items() if not v is None})
    ])
    logger.info(f"PAYLOAD====>{temp}")
    await websocket.send(json.dumps([
        2,
        message_id,
        Action.NotifyEvent,
        snake_to_camel_case({k: v for k, v in notify_event_payload.items() if not v is None})
    ]))
    await asyncio.sleep(1)
    response = await websocket.recv()
    data = json.loads(response)
    
    logger.info(f"DATA===>{data}")
    assert data[0] == 3
    assert data[1] == message_id
    CallResultStatusNotificationPayload(**camel_to_snake_case(data[2]))

async def test_charging():
    account, location, charge_point = await init_data(charge_point_id)

    async with websockets.connect(url) as websocket:
        # logger.info(websocket)
        await test_authorize(websocket)
        await asyncio.sleep(1)
        
        await test_boot_notification(websocket)
        await asyncio.sleep(1)
        
        # Sends a heartbeat to CSMS, one-time
        # add logic to resend it again on after n seconds.
        await test_heartbeat(websocket)
        await asyncio.sleep(1)
        
        # # Sends a status notification to CSMS
        await test_status_notification(websocket)
        await asyncio.sleep(1)
        
        # Sends a notify event to CSMS
        await test_notify_event(websocket)
        await asyncio.sleep(1)
        
        # await test_start_transaction(websocket, account, location, charge_point)
        # await asyncio.sleep(5)
        # await test_meter_values(websocket)
        # await asyncio.sleep(1)
        # await test_stop_transaction(websocket, account, location, charge_point)
        # await asyncio.sleep(5)


    await clean_tables(account, location, charge_point)

    print("\n\n --- SUCCESS ---")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(test_charging())
