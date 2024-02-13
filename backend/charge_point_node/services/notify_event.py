from loguru import logger

from ocpp.v201.call_result import NotifyEventPayload as CallResultNotifyEventPayload
from ocpp.v201.call import NotifyEventPayload as CallNotifyEventPayload
from ocpp.v201.enums import Action

from charge_point_node.models.notify_event import NotifyEventEvent
from charge_point_node.router import Router
from core.queue.publisher import publish

from manager.models.tasks.notify_event import NotifyEventTask

router = Router()


@router.on(Action.Authorize)
async def request_authorize(
        message_id: str,
        charge_point_id: str,
        **kwargs
):
    logger.info(f"Start accept notify event action "
                f"(charge_point_id={charge_point_id}, "
                f"message_id={message_id},"
                f"payload={kwargs}).")
    event = NotifyEventEvent(
        charge_point_id=charge_point_id,
        message_id=message_id,
        payload=CallNotifyEventPayload(**kwargs)
    )
    await publish(event.json(), to=event.exchange, priority=event.priority)
    

@router.out(Action.Authorize)
async def respond_authorize(task : NotifyEventTask) -> CallResultNotifyEventPayload:
    logger.info(f"Start respond authorize task={task}).")
    return CallResultNotifyEventPayload()

