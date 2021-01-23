import re
from django.core.mail import send_mail
from django.template import loader
import slack
from djangoProject.settings import SLACK_TOKEN


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
                    "text": "Congratulation " + name + " 🎉"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Badge Given by : " + awarded_by + " *\n*Badge Given : " + badge + " *\n " + description
                },
                "accessory": {
                    "type": "image",
                    "image_url": image,
                    "alt_text": "badge image"
                }
            },
            {
                "type": "divider"
            }
        ]
    }
    client_obj = slack.WebClient(token=SLACK_TOKEN)
    client_obj.chat_postMessage(**message)
    print("slack message sent")