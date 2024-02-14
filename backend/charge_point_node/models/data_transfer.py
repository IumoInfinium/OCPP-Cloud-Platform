from ocpp.v201.enums import Action
from ocpp.v201.call import DataTransferPayload

from charge_point_node.models.base import BaseEvent


class DataTransferEvent(BaseEvent):
    action: Action = Action.DataTransfer
    payload: DataTransferPayload
