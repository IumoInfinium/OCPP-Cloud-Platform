from ocpp.v201.enums import Action
from ocpp.v201.call import AuthorizePayload

from charge_point_node.models.base import BaseEvent

class AuthorizeEvent(BaseEvent):
    action : Action = Action.Authorize
    payload: AuthorizePayload