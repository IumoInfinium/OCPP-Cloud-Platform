# from typing import Dict

# from ocpp.v16.enums import Action

# from manager.models.tasks.base import BaseTask


# class AuthorizeTask(BaseTask):
#     id_tag_info: Dict
#     action: Action = Action.Authorize



from typing import Dict

from ocpp.v201.enums import Action
from manager.models.tasks.base import BaseTask

class AuthorizeTask(BaseTask):
    # , { "idTokenInfo": {"status": "Accepted" }}
    id_token_info: Dict
    action : Action = Action.Authorize