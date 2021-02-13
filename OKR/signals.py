from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Entry
from .utils import send_okr_message


@receiver(post_save, sender=Entry)
def send_mail(sender, instance, created, **kwargs):
    print("hell")
    if created:
        print("hurrya")
        name = instance.user.profile.name
        date_time = instance.date_time
        key_result = instance.key_result
        time_spent = instance.time_spent
        objective = instance.key_result.objective
        update = instance.update
        image = 'https://sushiksha.konkanischolarship.com' + str(instance.user.profile.image.url)
        array = [name, date_time, key_result, time_spent, objective, update, image]
        send_okr_message(array)
        # comment during production to avoid unnecessary errors
        # uncomment above line only if you have celery, rabbitmq setup and know the implementation
        return True