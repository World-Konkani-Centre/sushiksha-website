from celery import shared_task
from celery.utils.log import get_task_logger

from users.utils import send_reward_mail, send_reward_slack

logger = get_task_logger(__name__)


@shared_task
def send_email(array):
    send_reward_mail(array)
    return True


@shared_task
def send_in_slack(array):
    send_reward_slack(array)
    return True
