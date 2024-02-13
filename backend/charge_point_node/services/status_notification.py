from loguru import logger

from ocpp.v201.call import StatusNotificationPayload as CallStatusNotification
from ocpp.v201.call_result import StatusNotificationPayload as CallResultStatusNotificationPayload
from ocpp.v201.enums import Action

from charge_point_node.models.status_notification import StatusNotificationEvent
from charge_point_node.router import Router
from core.queue.publisher import publish
from manager.models.tasks.status_notification import StatusNotificationTask

router = Router()

@router.on(Action.StatusNotification)
async def on_status_notification(
    message_id : str,
    charge_point_id : str,
    **kwargs,
):
    logger.info(f"Send status notification to queue"
                f"(charge_point_id={charge_point_id}, "
                f"message_id={message_id},"
                f"payload={kwargs}).")
    
    try:
        event = StatusNotificationEvent(
            charge_point_id= charge_point_id,
            message_id= message_id,
            payload = CallStatusNotification(**kwargs)
        )
        
        logger.info(f"====> {event}")
    except Exception as e:
        logger.info(f"{e}")
    
    await publish(event.json(), to = event.exchange, priority = event.priority)
    

@router.out(Action.StatusNotification)
async def on_status_notification(
    task: StatusNotificationTask    
) -> CallResultStatusNotificationPayload:
    logger.info(f"Received status notification response ... ={task}).")
    return CallResultStatusNotificationPayload()