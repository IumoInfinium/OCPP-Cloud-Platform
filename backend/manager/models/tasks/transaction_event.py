from typing import Dict, Optional

from ocpp.v201.enums import Action
from manager.models.tasks.base import BaseTask
from ocpp.v201 import enums as OCPPEnums
from ocpp.v201 import datatypes as OCPPDatatypes


class TransactionEventTask(BaseTask):
    action: Action = Action.TransactionEvent
    total_cost: Optional[float]
    charging_priority: Optional[int]
    id_token_info: Optional[OCPPDatatypes.IdTokenInfoType]
    updated_personal_message: Optional[OCPPDatatypes.MessageContentType]
    custom_data: Optional[Dict]