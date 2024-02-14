from ocpp.v201.enums import RegistrationStatusType
from loguru import logger

from charge_point_node.models.data_transfer import DataTransferEvent
# from core.utils import get_utc_as_string
from manager.models.tasks.data_transfer import DataTransferTask


async def process_data_transfer(
        session, 
        event: DataTransferEvent
    )->DataTransferTask:
        logger.info(f"IAM INNNNNNNN !!!!!!!!!1")

        return DataTransferTask(
                message_id=event.message_id,
                charge_point_id=event.charge_point_id,
                # payload={"status":RegistrationStatusType.accepted},
                status=RegistrationStatusType.accepted
        )