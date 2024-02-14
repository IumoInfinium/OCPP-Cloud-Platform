from typing import Dict

from ocpp.v201.enums import Action
from manager.models.tasks.base import BaseTask
from ocpp.v201 import enums as OCPPEnums
from ocpp.v201 import datatypes as OCPPDatatypes


class TransactionEventTask(BaseTask):
    action: Action.TransactionEvent
    total_cost: float | None
    charging_priority: int | None
    id_token_info: Dict | None
    updated_personal_message: OCPPDatatypes.MessageContentType | None
    custom_data: None