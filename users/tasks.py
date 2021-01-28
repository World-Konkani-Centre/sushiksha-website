import csv
import datetime
import os

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from djangoProject.settings import FILE_PATH_FIELD_DIRECTORY
from users.models import BadgeCategory, Teams, Reward, AnalyticsReport
from users.utils import send_reward_mail, send_reward_slack
from django.contrib.auth.models import User

logger = get_task_logger(__name__)


@shared_task
def send_email(array):
    logger.info("sending the BADGE " + array[4] + " GIVEN BY -- " + array[2] + " TO " + array[5] + " at " + array[1])
    send_reward_mail(array)
    send_reward_slack(array)
    return "DONE\n"


@shared_task
def get_team_file_weekly():
    date = timezone.now()
    date_7 = date - datetime.timedelta(days=7)
    date_7 = date_7.date()
    filename = 'Sushiksha-Admin-Team-Points-Weekly' + str(datetime.date.today().isocalendar()[1]) + '.csv'
    filepath = os.path.join(FILE_PATH_FIELD_DIRECTORY, filename)
    if not os.path.exists(FILE_PATH_FIELD_DIRECTORY):
        os.makedirs(FILE_PATH_FIELD_DIRECTORY)
    with open(filepath, 'w+') as response:
        writer = csv.writer(response)
        headers = ['Team Name', 'Total Points']
        badge_category_start = 2
        category_points = []
        categories = BadgeCategory.objects.all().order_by('name')
        for category in categories:
            headers.append(category.name)
            category_points.append(0)
        headers.append('Points This Week')
        writer.writerow(headers)

        teams = Teams.objects.all().order_by('name')

        for team in teams:
            members = team.members.all()
            points = 0
            for i in range(0, len(category_points)):
                category_points[i] = 0
            for member in members:
                badges_received = Reward.objects.filter(user=member.user, timestamp__lte=date, timestamp__gt=date_7)
                for _badge in badges_received:
                    index = headers.index(_badge.badges.category.name)
                    category_points[index - badge_category_start] = category_points[
                                                                        index - badge_category_start] + _badge.badges.points
                    points = points + _badge.badges.points
            row_of_team = [team.name, team.points] + category_points + [points]
            writer.writerow(row_of_team)
    AnalyticsReport.objects.create(title='Team-Weekly-Report' + str(datetime.date.today().isocalendar()[1]) + '.csv',
                                   file=filepath)
    return True


@shared_task
def get_team_file_monthly():
    date = timezone.now()
    date_30 = date - datetime.timedelta(days=30)
    date_30 = date_30.date()
    filename = 'Sushiksha-Admin-Team-Points-Monthly' + str(datetime.date.today().month) + '.csv'
    filepath = os.path.join(FILE_PATH_FIELD_DIRECTORY, filename)
    if not os.path.exists(FILE_PATH_FIELD_DIRECTORY):
        os.makedirs(FILE_PATH_FIELD_DIRECTORY)
    with open(filepath, 'w+') as response:
        writer = csv.writer(response)
        headers = ['Team Name', 'Total Points']
        badge_category_start = 2
        category_points = []
        categories = BadgeCategory.objects.all().order_by('name')
        for category in categories:
            headers.append(category.name)
            category_points.append(0)
        headers.append('Points This Month')
        writer.writerow(headers)

        teams = Teams.objects.all().order_by('name')

        for team in teams:
            members = team.members.all()
            points = 0
            for i in range(0, len(category_points)):
                category_points[i] = 0
            for member in members:
                badges_received = Reward.objects.filter(user=member.user, timestamp__lte=date, timestamp__gt=date_30)
                for _badge in badges_received:
                    index = headers.index(_badge.badges.category.name)
                    category_points[index - badge_category_start] = category_points[
                                                                        index - badge_category_start] + _badge.badges.points
                    points = points + _badge.badges.points
            row_of_team = [team.name, team.points] + category_points + [points]
            writer.writerow(row_of_team)
        AnalyticsReport.objects.create(title='Team-Monthly-Report' + str(datetime.date.today().month) + '.csv',
                                       timestamp=timezone.now(), file=filepath)
    return True


@shared_task
def get_user_file_weekly():
    date = timezone.now()
    date_7 = date - datetime.timedelta(days=7)
    date_7 = date_7.date()
    filename = 'Sushiksha-Admin-Member-Points-Weekly' + str(datetime.date.today().isocalendar()[1]) + '.csv'
    filepath = os.path.join(FILE_PATH_FIELD_DIRECTORY, filename)
    if not os.path.exists(FILE_PATH_FIELD_DIRECTORY):
        os.makedirs(FILE_PATH_FIELD_DIRECTORY)
    with open(filepath, 'w+') as response:
        writer = csv.writer(response)
        headers = ['Username', 'Name', 'Email', 'Batch', 'Total Points', 'Stars']
        badge_category_start = 6
        category_points = []
        categories = BadgeCategory.objects.all().order_by('name')
        for category in categories:
            headers.append(category.name)
            category_points.append(0)
        headers.append('Points This Week')
        writer.writerow(headers)

        users = User.objects.all().order_by('profile__name')

        for user in users:
            points = 0
            badges_received = Reward.objects.filter(user=user, timestamp__lte=date, timestamp__gt=date_7)
            for i in range(0, len(category_points)):
                category_points[i] = 0
            for _badge in badges_received:
                index = headers.index(_badge.badges.category.name)
                category_points[index - badge_category_start] = category_points[
                                                                    index - badge_category_start] + _badge.badges.points
                points = points + _badge.badges.points
            row_of_user = [user.username, user.profile.name, user.email, user.profile.batch, user.profile.points,
                           user.profile.stars] + category_points + [points]
            writer.writerow(row_of_user)

        AnalyticsReport.objects.create(title='Member-Weekly-Report' + str(datetime.date.today().isocalendar()[1]) + '.csv',
                                       timestamp=timezone.now(), file=response)
        return True


@shared_task
def get_user_file_monthly():
    date = timezone.now()
    date_30 = date - datetime.timedelta(days=30)
    date_30 = date_30.date()
    filename = 'Sushiksha-Admin-Member-Points-Monthly' + str(datetime.date.today().month) + '.csv'
    filepath = os.path.join(FILE_PATH_FIELD_DIRECTORY, filename)
    if not os.path.exists(FILE_PATH_FIELD_DIRECTORY):
        os.makedirs(FILE_PATH_FIELD_DIRECTORY)
    with open(filepath, 'w+') as response:
        writer = csv.writer(response)
        headers = ['Username', 'Name', 'Email', 'Batch', 'Total Points', 'Stars']
        badge_category_start = 6
        category_points = []
        categories = BadgeCategory.objects.all().order_by('name')
        for category in categories:
            headers.append(category.name)
            category_points.append(0)
        headers.append('Points This Week')
        writer.writerow(headers)

        users = User.objects.all().order_by('profile__name')

        for user in users:
            points = 0
            badges_received = Reward.objects.filter(user=user, timestamp__lte=date, timestamp__gt=date_30)
            for i in range(0, len(category_points)):
                category_points[i] = 0
            for _badge in badges_received:
                index = headers.index(_badge.badges.category.name)
                category_points[index - badge_category_start] = category_points[
                                                                    index - badge_category_start] + _badge.badges.points
                points = points + _badge.badges.points
            row_of_user = [user.username, user.profile.name, user.email, user.profile.batch, user.profile.points,
                           user.profile.stars] + category_points + [points]
            writer.writerow(row_of_user)

        AnalyticsReport.objects.create(title='Member-Monthly-Report' + str(datetime.date.today().month)  + '.csv',
                                       timestamp=timezone.now(), file=response)
        return True
