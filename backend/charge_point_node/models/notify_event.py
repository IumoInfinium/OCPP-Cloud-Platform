from ocpp.v201.enums import Action
from ocpp.v201.call import NotifyEventPayload

from charge_point_node.models.base import BaseEvent

class NotifyEventEvent(BaseEvent):
    action : Action = Action.NotifyEvent
    payload: NotifyEventPayload