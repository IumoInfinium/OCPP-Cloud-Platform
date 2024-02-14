from ocpp.v201.enums import Action
from ocpp.v201.call import TransactionEventPayload

from charge_point_node.models.base import BaseEvent


class TransactionEventEvent(BaseEvent):
    action: Action = Action.TransactionEvent
    payload: TransactionEventPayload