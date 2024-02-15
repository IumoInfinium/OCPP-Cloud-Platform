from charge_point_node.models.transaction_event import TransactionEventEvent
from manager.models.tasks.transaction_event import TransactionEventTask
from ocpp.v201 import enums as OCPPEnums
from ocpp.v201 import datatypes as OCPPDatatypes
from ocpp.v201.call import TransactionEventPayload

from loguru import logger
from typing import Dict

async def process_transaction_event(session, event: TransactionEventEvent) -> TransactionEventTask:
    
    
    logger.info("******************************")
    logger.info(f"{event}")
    

    payload: TransactionEventPayload = event.payload
    
    if(payload.event_type == OCPPEnums.TransactionEventType.started):    
        # transaction event started
        
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
        return TransactionEventTask(
            message_id = event.message_id,
            charge_point_id= event.charge_point_id,
            # charging_priority = 0, # ranges from -9 ... 9
            # id_token_info= id_token_info
        )
    else:
        # transaction event endee
        return TransactionEventTask(
            message_id = event.message_id,
            charge_point_id= event.charge_point_id,
            # charging_priority = 0, # ranges from -9 ... 9
            # id_token_info= id_token_info
        )
    
    