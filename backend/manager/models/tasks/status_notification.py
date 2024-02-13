from ocpp.v201.enums import Action

from manager.models.tasks.base import BaseTask


class StatusNotificationTask(BaseTask):
    action: Action = Action.StatusNotification
    # pass custom_data here