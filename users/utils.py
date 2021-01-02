import re
from django.core.mail import send_mail


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
    # print("it works")
    email = array[0]
    timestamp = array[1]
    awarded_by = array[2]
    description = array[3]
    badge = array[4]
    subject = f'A {badge} Badge from {awarded_by}'
    comment = f'{description}'
    send_mail(subject, comment, None, [email])
    # print("End")
