from ocpp.v201.enums import Action, RegistrationStatusType
from typing import Dict
from manager.models.tasks.base import BaseTask


class DataTransferTask(BaseTask):
    # payload: Dict
    status: RegistrationStatusType
    action: Action = Action.DataTransfer
