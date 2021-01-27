from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.tasks import send_email
from .models import Profile, Pomodoro, Reward,Teams, House,Badge


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Pomodoro.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Reward)
def send_mail(sender, instance, created, **kwargs):
    if created:
        email = instance.user.email
        name = instance.user.profile.name
        badge = instance.badges.title
        description = instance.description
        awarded_by = instance.awarded_by
        timestamp = instance.timestamp
        image = 'https://sushiksha.konkanischolarship.com' + str(instance.badges.logo.url)
        array = [email, timestamp, awarded_by, description, badge, name, image]
        profile = Profile.objects.get(user=instance.user)
        _badge = Badge.objects.get(title=badge)
        profile.points = profile.points + _badge.points
        profile.save()
        team = Teams.objects.filter(members__user=instance.user).first()
        if team is not None:
            team.points = team.points + _badge.points
            team.save()
        house = House.objects.filter(teams__members__user=instance.user).first()
        if house is not None:
            house.points = house.points + _badge.points
            house.save()
        # send_email.delay(array)
        # do not uncomment
        # uncomment above line only if you have celery, rabbitmq setup and know the implementation
        return True
