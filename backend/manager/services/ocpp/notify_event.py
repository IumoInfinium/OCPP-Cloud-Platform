from charge_point_node.models.notify_event import NotifyEventEvent
from manager.models.tasks.notify_event import NotifyEventTask

async def process_notify_event(session, event: NotifyEventEvent) -> NotifyEventTask:
    """
    NOTIFY EVENT logic here
    """
    return NotifyEventTask(
        message_id= event.message_id,
        charge_point_id= event.charge_point_id,
    )