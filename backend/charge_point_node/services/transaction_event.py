from loguru import logger

from ocpp.v201.call import TransactionEventPayload as CallTransactionPayload
from ocpp.v201.call_result import TransactionEventPayload as CallResultTransactionPayload
from ocpp.v201.enums import Action

from charge_point_node.models.transaction_event import TransactionEventEvent
from charge_point_node.router import Router
from core.queue.publisher import publish
from manager.models.tasks.transaction_event import TransactionEventTask

router = Router()


@router.on(Action.TransactionEvent)
async def request_transaction_event(
        message_id: str,
        charge_point_id: str,
        **kwargs
):
    logger.info(f"Start accept transaction action "
                f"(charge_point_id={charge_point_id}, "
                f"message_id={message_id},"
                f"payload={kwargs}).")
    event = TransactionEventEvent(
        charge_point_id=charge_point_id,
        message_id=message_id,
        payload=CallTransactionPayload(**kwargs)
    )
    await publish(event.json(), to=event.exchange, priority=event.priority)
    

@router.out(Action.TransactionEvent)
async def respond_authorize(task : TransactionEventTask) -> CallResultTransactionPayload:
    logger.info(f"Start respond transaction task={task}).")
    return CallResultTransactionPayload(
        total_cost= task.total_cost,
        charging_priority=task.charging_priority,
        updated_personal_message= task.updated_personal_message,
        custom_data= task.custom_data,
        id_token_info=task.id_token_info,
    )

