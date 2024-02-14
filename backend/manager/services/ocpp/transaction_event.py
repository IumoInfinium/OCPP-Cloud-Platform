from charge_point_node.models.transaction_event import TransactionEventEvent
from manager.models.tasks.transaction_event import TransactionEventTask
from ocpp.v201 import enums as OCPPEnums
from ocpp.v201 import datatypes as OCPPDatatypes


async def process_transaction_event(session, event: TransactionEventEvent) -> TransactionEventTask:

    # return AuthorizeTask(
    #     message_id=event.message_id,
    #     charge_point_id=event.charge_point_id,
    #     id_tag_info={"status":"Accepted"}
    # )
    # status can be : 
    
    id_token_info: OCPPDatatypes.IdTokenInfoType = None
    # id_token_info.status = OCPPEnums.AuthorizationStatusType.accepted
    
    updated_personal_message: OCPPDatatypes.MessageContentType = None
    # updated_personal_message.format =

    return TransactionEventTask(
        message_id = event.message_id,
        charge_point_id= event.charge_point_id,
        charging_priority=0, # ranges from -9 ... 9
        id_token_info= id_token_info,
        updated_personal_message= updated_personal_message,
        # message_id= event.message_id,
        # charge_point_id= event.charge_point_id,
        # id_token_info={"status": OCPPEnums.AuthorizationStatusType.accepted }
    )