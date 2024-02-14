from loguru import logger

from ocpp.v201.call import DataTransferPayload as CallDataTransferPayload
from ocpp.v201.enums import Action

from ocpp.v201.call_result import DataTransferPayload as CallResultDataTransferPayload

from charge_point_node.models.data_transfer import DataTransferEvent
from charge_point_node.router import Router
from core.queue.publisher import publish
from manager.models.tasks.data_transfer import DataTransferTask

router = Router()


@router.on(Action.DataTransfer)
async def on_data_transfer(
        message_id: str,
        charge_point_id: str,
        **kwargs
):
    logger.info(f"Start accept data transfer "
                f"(charge_point_id={charge_point_id}, "
                f"message_id={message_id},"
                f"payload={kwargs}).")
    event = DataTransferEvent(
        charge_point_id=charge_point_id,
        message_id=message_id,
        payload=CallDataTransferPayload(**kwargs)
        
    )
    logger.info(f";;;;;;;;;;;;;;;;;;;;;;;;;;{event};;;;;;;;;;;;;;;;;;;;;")
    await publish(event.json(), to=event.exchange, priority=event.priority)


@router.out(Action.DataTransfer)
async def respond_data_transfer(task: DataTransferTask) -> CallResultDataTransferPayload:
    logger.info(f"Start respond data transfer task={task}).")
    return CallResultDataTransferPayload(status=task.status)
