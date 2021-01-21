from celery import shared_task
from users.utils import send_reward_mail, send_reward_slack


@shared_task
def send_email(array):
    send_reward_mail(array)
    send_reward_slack(array)
    return True
