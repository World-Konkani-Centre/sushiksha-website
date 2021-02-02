from django.shortcuts import render

from archive.forms import UrlRequestForm


def timer(request):
    if request.POST:
        form = UrlRequestForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['URL']
            return render(request, 'templates/timer/timer.html', context={'url': url, 'form':form})
        return render(request, 'templates/timer/timer.html', context={'url': 'https://cuckoo.team/'})
    else:
        form = UrlRequestForm()
        return render(request, 'templates/timer/timer.html', context={'url': 'https://cuckoo.team/', 'form':form})



"""
## UNOptimized


@login_required
def get_user_file(request):
    date = timezone.now()
    date_7 = date - datetime.timedelta(days=7)
    date_7 = date_7.date()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Sushiksha-User-Points' + str(
        datetime.date.today()) + '.csv'
    writer = csv.writer(response)
    headers = ["WEEK "]
    badge_category_start = 1
    category_points = []
    categories = BadgeCategory.objects.all().order_by('name')
    for category in categories:
        headers.append(category.name)
        category_points.append(0)
    headers.append('Points this week')
    writer.writerow(headers)

    user = User.objects.filter(id=request.user.id).first()
    # week 1
    points = 0
    badges_received = Reward.objects.filter(user=user, timestamp__lte=date, timestamp__gt=date_7)
    for i in range(0, len(category_points)):
        category_points[i] = 0
    for _badge in badges_received:
        index = headers.index(_badge.badges.category.name)
        category_points[index - badge_category_start] = category_points[
                                                            index - badge_category_start] + _badge.badges.points
        points = points + _badge.badges.points
    row_of_user = ["Week 1 " + str(date.date()) + ' -- ' + str(date_7)] + category_points + [points]
    writer.writerow(row_of_user)

    # week 2
    date = date_7
    date_7 = date - datetime.timedelta(days=7)
    points = 0
    badges_received = Reward.objects.filter(user=user, timestamp__lte=date, timestamp__gt=date_7)
    for i in range(0, len(category_points)):
        category_points[i] = 0
    for _badge in badges_received:
        index = headers.index(_badge.badges.category.name)
        category_points[index - badge_category_start] = category_points[
                                                            index - badge_category_start] + _badge.badges.points
        points = points + _badge.badges.points
    row_of_user = ["Week 2 " + str(date) + ' -- ' + str(date_7)] + category_points + [points]
    writer.writerow(row_of_user)

    # week 3
    date = date_7
    date_7 = date - datetime.timedelta(days=7)
    points = 0
    badges_received = Reward.objects.filter(user=user, timestamp__lte=date, timestamp__gt=date_7)
    for i in range(0, len(category_points)):
        category_points[i] = 0
    for _badge in badges_received:
        index = headers.index(_badge.badges.category.name)
        category_points[index - badge_category_start] = category_points[
                                                            index - badge_category_start] + _badge.badges.points
        points = points + _badge.badges.points
    row_of_user = ["Week 3 " + str(date) + ' -- ' + str(date_7)] + category_points + [points]
    writer.writerow(row_of_user)

    # week 4
    date = date_7
    date_7 = date - datetime.timedelta(days=7)
    points = 0
    badges_received = Reward.objects.filter(user=user, timestamp__lte=date, timestamp__gt=date_7)
    for i in range(0, len(category_points)):
        category_points[i] = 0
    for _badge in badges_received:
        index = headers.index(_badge.badges.category.name)
        category_points[index - badge_category_start] = category_points[
                                                            index - badge_category_start] + _badge.badges.points
        points = points + _badge.badges.points
    row_of_user = ["Week 4 " + str(date) + ' -- ' + str(date_7)] + category_points + [points]
    writer.writerow(row_of_user)

    return response

@login_required
def get_team_file(request):
    date = timezone.now()
    date_7 = date - datetime.timedelta(days=7)
    date_7 = date_7.date()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Sushiksha-Team-Points' + str(
        datetime.date.today()) + '.csv'
    writer = csv.writer(response)
    headers = ['Member Name']
    badge_category_start = 1
    category_points = []
    categories = BadgeCategory.objects.all().order_by('name')
    for category in categories:
        headers.append(category.name)
        category_points.append(0)
    headers.append('Points This Week')
    writer.writerow(headers)

    team = Teams.objects.filter(members__user__id=request.user.id).first()
    if team is not None:
        members = team.members.all().order_by('name')
    else:
        return redirect('logs')
    for member in members:
        points = 0
        for i in range(0, len(category_points)):
            category_points[i] = 0
        badges_received = Reward.objects.filter(user=member.user, timestamp__lte=date, timestamp__gt=date_7)
        for _badge in badges_received:
            index = headers.index(_badge.badges.category.name)
            category_points[index - badge_category_start] = category_points[
                                                                index - badge_category_start] + _badge.badges.points
            points = points + _badge.badges.points
        row_of_team = [member.name] + category_points + [points]
        writer.writerow(row_of_team)
    return response


@login_required
def get_user_file_large(request):
    if request.POST:
        form = RangeRequestForm(request.POST)
        if form.is_valid():
            beginning = form.cleaned_data['beginning']
            end = form.cleaned_data['end']
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=Sushiksha-All-Users-Points' + str(
                datetime.date.today()) + '.csv'
            writer = csv.writer(response)
            headers = ['Username', 'Name', 'Email', 'Batch', 'Total Points', 'Stars']
            badge_category_start = 6
            category_points = []
            categories = BadgeCategory.objects.all().order_by('name')
            for category in categories:
                headers.append(category.name)
                category_points.append(0)
            headers.append(
                'Points In Interval - ' + beginning.strftime("%d/%b/%Y %H:%M") + '---' + end.strftime("%d/%b/%Y %H:%M"))
            writer.writerow(headers)

            users = User.objects.all().order_by('username')

            for user in users:
                points = 0
                badges_received = Reward.objects.filter(user=user, timestamp__lte=end, timestamp__gte=beginning)
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
            return response
    else:
        form = RangeRequestForm()
        heading = "User Data"
        context = {
            'form': form,
            'heading': heading
        }
        return render(request, 'logs-users.html', context=context)

@login_required
def get_team_file_large(request):
    if request.POST:
        form = RangeRequestForm(request.POST)
        if form.is_valid():
            beginning = form.cleaned_data['beginning']
            end = form.cleaned_data['end']
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=Sushiksha-All-Teams-Points' + str(
                datetime.date.today()) + '.csv'
            writer = csv.writer(response)
            headers = ['Team Name', 'Total Points']
            badge_category_start = 2
            category_points = []
            categories = BadgeCategory.objects.all().order_by('name')
            for category in categories:
                headers.append(category.name)
                category_points.append(0)
            headers.append(
                'Points In Interval - ' + beginning.strftime("%d/%b/%Y %H:%M") + '---' + end.strftime("%d/%b/%Y %H:%M"))
            writer.writerow(headers)

            teams = Teams.objects.all().order_by('name')

            for team in teams:
                members = team.members.all()
                points = 0
                for i in range(0, len(category_points)):
                    category_points[i] = 0
                for member in members:
                    badges_received = Reward.objects.filter(user=member.user, timestamp__lte=end,
                                                            timestamp__gte=beginning)
                    for _badge in badges_received:
                        index = headers.index(_badge.badges.category.name)
                        category_points[index - badge_category_start] = category_points[
                                                                            index - badge_category_start] + _badge.badges.points
                        points = points + _badge.badges.points
                row_of_team = [team.name, team.points] + category_points + [points]
                writer.writerow(row_of_team)
            return response
    else:
        form = RangeRequestForm()
        heading = "Team Data"
        context = {
            'form': form,
            'heading': heading
        }
        return render(request, 'logs-users.html', context=context)


@login_required
def get_single_user_file_large(request):
    if request.POST:
        form = UserRangeRequestForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            beginning = form.cleaned_data['beginning']
            end = form.cleaned_data['end']
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=Sushiksha-'+str(user)+'-Points' + str(
                datetime.date.today()) + '.csv'
            writer = csv.writer(response)
            headers = ['WEEK']
            badge_category_start = 1
            category_points = []
            categories = BadgeCategory.objects.all().order_by('name')
            for category in categories:
                headers.append(category.name)
                category_points.append(0)
            headers.append('Points this week')
            writer.writerow(headers)

            delta = datetime.timedelta(days=7)
            week_counter = 1
            next = end - delta
            while next >= beginning:
                points = 0
                for i in range(0, len(category_points)):
                    category_points[i] = 0
                badges_received = Reward.objects.filter(user=user, timestamp__lte=end,
                                                        timestamp__gt=next)
                for _badge in badges_received:
                    index = headers.index(_badge.badges.category.name)
                    category_points[index - badge_category_start] = category_points[
                                                                        index - badge_category_start] + _badge.badges.points
                    points = points + _badge.badges.points
                row_of_team = ["Week " + str(week_counter) + '--' + str(end.date()) + ' -- ' + str(
                    next.date())] + category_points + [points]
                writer.writerow(row_of_team)
                end = next
                next -= delta
                week_counter += 1

            points = 0
            for i in range(0, len(category_points)):
                category_points[i] = 0
            badges_received = Reward.objects.filter(user=user, timestamp__lte=end,
                                                    timestamp__gt=beginning)
            for _badge in badges_received:
                index = headers.index(_badge.badges.category.name)
                category_points[index - badge_category_start] = category_points[
                                                                    index - badge_category_start] + _badge.badges.points
                points = points + _badge.badges.points
            row_of_team = ["Week " + str(week_counter) + '--' + str(end.date()) + ' -- ' + str(beginning.date())] + category_points + [
                points]
            writer.writerow(row_of_team)
            return response

    else:
        form = UserRangeRequestForm()
        heading = "Single User Data"
        context = {
            'form': form,
            'heading': heading
        }
        return render(request, 'logs-users.html', context=context)
"""