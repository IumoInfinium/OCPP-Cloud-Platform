from charge_point_node.models.authorize import AuthorizeEvent
from manager.models.tasks.authorize import AuthorizeTask
from ocpp.v201 import enums as OCPPEnums


async def process_authorize(session, event: AuthorizeEvent) -> AuthorizeTask:

    # return AuthorizeTask(
    #     message_id=event.message_id,
    #     charge_point_id=event.charge_point_id,
    #     id_tag_info={"status":"Accepted"}
    # )
    # status can be : 
    return AuthorizeTask(
        message_id= event.message_id,
        charge_point_id= event.charge_point_id,
        id_token_info={"status": OCPPEnums.AuthorizationStatusType.accepted }
    )