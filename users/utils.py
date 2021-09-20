import datetime
import re

import numpy as np
import slack
from django.core.mail import send_mail
from django.db.models import Sum
from django.db.models.functions import Lower
from django.template import loader
from django.utils import timezone

from djangoProject.settings import SLACK_TOKEN
from .models import BadgeCategory, Reward, Teams, House, UPGRADE_POINTS


def collect_titles(badges):
    titles = []
    for badge in badges:
        titles.append(badge.badges.title)
    return set(titles)


def collect_badges(user):
    badge = user.reward_set.all()
    titles = collect_titles(badges=badge)

    rewards = []
    count = []
    for title in titles:
        rewards.append(user.reward_set.filter(badges__title=title).first())
        count.append(user.reward_set.filter(badges__title=title).count())

    return rewards, count


def get_house_points(house):
    points = 0
    for team in house.teams.all():
        for member in team.members.all():
            points += member.get_point()
    return points


def get_house_data(houses):
    for house in houses:
        house.points = get_house_points(house)
        house.save()


def get_team_points(teams):
    points = 0
    for member in teams.members.all():
        points += member.get_point()
    return points


def get_team_data(teams):
    for team in teams:
        team.points = get_team_points(team)
        team.save()


def email_check(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    else:
        return None


def send_reward_mail(array):
    email = array[0]
    timestamp = array[1]
    awarded_by = array[2]
    description = array[3]
    badge = array[4]
    name = array[5]
    logo = array[6]
    html_message = loader.render_to_string(
        'email/message.html',
        {
            'image': logo,
            'name': name,
            'badge': badge,
            'awarded': awarded_by,
            'reason': description,
        })

    subject = f'A {badge} Badge from {awarded_by}'

    comment = f'''
Dear {name},
Congratulations.
You have been awarded with {badge} by {awarded_by} for {description}. Please visit your profile page on 
Sushiksha Website to see the badge. Badges are an amazing way to express your feelings to fellow sophists.

Congrats once again,

Best Wishes,
Convener
Sushiksha
Alumni Mentoring Programme
World Konkani Centre
    '''
    send_mail(subject, comment, None, [email], html_message=html_message)
    print("email sent")


def send_reward_slack(array):
    timestamp = array[1]
    awarded_by = array[2]
    description = array[3]
    badge = array[4]
    name = array[5]
    image = array[6]
    slack_id = array[7]
    message = {
        'channel': '#sushiksha-badges',
        "blocks": [
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Congratulations " + name + " 🎉"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*From:* " + awarded_by + "\n*Badge Given:* " + badge + "\n*Message:*\n" + description
                },
                "accessory": {
                    "type": "image",
                    "image_url": image,
                    "alt_text": badge
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f":wkc-badge1: <https://sushiksha.konkanischolarship.com/user/rewards/|Sushiksha Badges> | <@{slack_id}>"
                    }
                ]
            },
        ]
    }
    client_obj = slack.WebClient(token=SLACK_TOKEN)
    client_obj.chat_postMessage(**message)
    print("slack message sent")


def format_result(result, headers):
    output = []
    array = np.array(result)[::-1]
    for i in range(len(headers)):
        output.append(array[:, i].tolist())
    return output


def user_chart_data(user):
    result = []
    headers = []
    category_points = []
    categories = BadgeCategory.objects.all().order_by(Lower('name'))
    for category in categories:
        headers.append(category.name)
        category_points.append(0)
    end = timezone.now()
    delta = datetime.timedelta(days=7)
    for week in range(1, 5):
        points = 0
        for i in range(0, len(category_points)):
            category_points[i] = 0
        badges_received = Reward.objects.filter(user=user, timestamp__lte=end,
                                                timestamp__gt=(end - delta)).values('badges__category__name').annotate(
            Sum('badges__points'))
        for category in badges_received:
            index = headers.index(category['badges__category__name'])
            category_points[index] += category['badges__points__sum']
            points += category['badges__points__sum']
        result.append(category_points + [points])
        end -= delta
    result = format_result(result, headers)
    return headers, result


def get_category_points_data(user, categories):
    query_category = Reward.objects.filter(user=user).values('badges__category__name').annotate(
        Sum('badges__points'))
    result = [0] * len(categories)
    for q in query_category:
        result[categories.index(q['badges__category__name'])] = q['badges__points__sum']
    return result


def update_profile_points(profile, _badge):
    profile.points = profile.points + _badge.points
    if profile.total_points == 0:
        profile.total_points = max(0, profile.points)
    else:
        profile.total_points += _badge.points
    categories = list(BadgeCategory.objects.all().order_by(Lower('name')).values_list('name', flat=True))
    points = get_category_points_data(profile.user, categories)
    if profile.rank == "Senator" and points >= UPGRADE_POINTS[1]:
        profile.rank = "Caesar"
    elif profile.rank == "Sophist" and points >= UPGRADE_POINTS[0]:
        profile.rank = "Senator"
    if profile.rank == "Caesar" and profile.total_points >= 1000:
        profile.suShells += profile.total_points / 1000
        profile.total_points = profile.total_points % 1000
    profile.save()

