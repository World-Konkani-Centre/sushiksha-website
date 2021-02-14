from celery import shared_task
from celery.utils.log import get_task_logger

from .utils import send_okr_message

logger = get_task_logger(__name__)


@shared_task
def okr_entry(array):
    print(array)
    send_okr_message(array)
    return "DONE\n"


