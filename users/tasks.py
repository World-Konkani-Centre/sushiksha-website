from celery import shared_task
from celery.utils.log import get_task_logger

from users.utils import send_reward_mail, send_reward_slack

logger = get_task_logger(__name__)


@shared_task
def send_email(array):
    logger.info("sending the BADGE " + array[4] + " GIVEN BY -- " + array[2] + " TO " + array[5] + " at " + array[1])
    send_reward_mail(array)
    send_reward_slack(array)
    return "DONE\n"


