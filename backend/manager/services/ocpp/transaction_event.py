from charge_point_node.models.transaction_event import TransactionEventEvent
from manager.models.tasks.transaction_event import TransactionEventTask
from ocpp.v201 import enums as OCPPEnums
from ocpp.v201 import datatypes as OCPPDatatypes
from ocpp.v201.call import TransactionEventPayload as CallTransactionEventPayload

from manager.services.transactions import update_transaction,create_transaction, get_transaction
from manager.views.transactions import UpdateTransactionView, CreateTransactionView
from manager.services.charge_points import get_charge_point

from loguru import logger
from typing import Dict

async def process_transaction_event(session, event: TransactionEventEvent) -> TransactionEventTask:
    
    
    logger.info("******************************")
    logger.info(f"{event}")
    

    payload: CallTransactionEventPayload = event.payload
    
    if(payload.event_type == OCPPEnums.TransactionEventType.started):    
        # transaction event started
        charge_point = await get_charge_point(session, event.charge_point_id)
        view = CreateTransactionView(
            city = charge_point.location.city,
            address= "temp",
            vehicle= event.payload.id_token['id_token'],
            meter_start= 0,
            charge_point= charge_point.id,
            account_id= "6fe555ea-2ed1-43bc-965e-254113401597"
        )
        
        transaction = await create_transaction(session=session, data=view)
        await session.flush()
        
        id_token_info: Dict= {}
        id_token_info['status'] = OCPPEnums.AuthorizationStatusType.accepted

        # updated_personal_message: OCPPDatatypes.MessageContentType = OCPPDatatypes.MessageContentType
        
        return TransactionEventTask(
            message_id = event.message_id,
            charge_point_id= event.charge_point_id,
            charging_priority = 0, # ranges from -9 ... 9
            id_token_info= id_token_info
        )
    
    elif(payload.event_type == OCPPEnums.TransactionEventType.updated):    
        # transaction event ongoing
        charge_point = await get_charge_point(session, event.charge_point_id)
        logger.info(f'{event.payload}')
        payload: CallTransactionEventPayload= event.payload
        meter_values = payload.meter_value[-1]["sampled_value"][-1]["value"]

        view = UpdateTransactionView(
            transaction_id = event.payload.transaction_info['transaction_id'],
            meter_stop= meter_values
        )

        # update transaction info
        # await update_transaction(session, event.payload.transaction_info['transaction_id'], view)
        # await session.flush()
        
        return TransactionEventTask(
            message_id = event.message_id,
            charge_point_id= event.charge_point_id,
            # charging_priority = 0, # ranges from -9 ... 9
            # id_token_info= id_token_info
        )
    else:
        # transaction event ended
        
        return TransactionEventTask(
            message_id = event.message_id,
            charge_point_id= event.charge_point_id,
            # charging_priority = 0, # ranges from -9 ... 9
            # id_token_info= id_token_info
        )
    
    