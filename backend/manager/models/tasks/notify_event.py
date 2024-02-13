from typing import Dict

from ocpp.v201.enums import Action
from manager.models.tasks.base import BaseTask

class NotifyEventTask(BaseTask):

    action : Action = Action.NotifyEvent
    # pass custom_data here