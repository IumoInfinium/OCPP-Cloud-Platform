from ocpp.v201.enums import Action
from ocpp.v201.call import BootNotificationPayload

from charge_point_node.models.base import BaseEvent


class BootNotificationEvent(BaseEvent):
    action: Action = Action.BootNotification
    payload: BootNotificationPayload
