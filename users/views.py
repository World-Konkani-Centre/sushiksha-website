import csv
import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum
from django.db.models.functions import Lower
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils import timezone
from djqscsv import render_to_csv_response

from .forms import UserUpdateForm, ProfileUpdateForm, RewardForm, UserRegisterForm, BadgeForm, RangeRequestForm, \
    UserRangeRequestForm, MultiBadgeForm
from .models import Badge, Profile, House, Teams, Reward, BadgeCategory, Mentions
from .utils import email_check, user_chart_data, get_category_points_data

color = ['window.chartColors.red', 'window.chartColors.purple',
         'window.chartColors.green',
         'window.chartColors.orange', 'window.chartColors.grey',
         'window.chartColors.yellow', 'window.chartColors.blue']


def register(request):
    if request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }
    return render(request, 'authorization/register.html', context)


def user_login(request):
    if request.POST:
        user_cred = request.POST['username']
        password = request.POST['password']
        if email_check(user_cred):
            username = User.objects.get(email=user_cred).username
            user = authenticate(request, username=username, password=password)
        else:
            user = authenticate(request, username=user_cred, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have logged into your account!!')
            return redirect('home')

        else:
            messages.error(request, 'Invalid Credential')
            return redirect(request.META['HTTP_REFERER'])
    else:
        return render(request, 'authorization/login.html', {'title': "Login"})


@login_required
def profile(request):
    user = get_object_or_404(User, id=request.user.id)
    categories, data = user_chart_data(user)
    result = get_category_points_data(user, categories)
    zipped_data = zip(categories, data, color)
    profile_details = {}
    badges = Reward.objects.filter(user=request.user).values('badges__title', 'badges__logo').annotate(
        Count('badges__title'))
    if request.POST:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Your Account has been Updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        query = Profile.objects.filter(user__id=request.user.id).first()
        profile_details = {
            'username': query.user.username,
            'batch': query.batch,
            'name': query.name,
            'phone': query.phone,
            'college': query.college,
            'degree': query.degree,
            'branch': query.branch,
            'profession': query.profession,
            'address': query.address,
            'guidance': query.guidance,
        }
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': "Profile",
        'badges': badges,
        'profile_details': profile_details,
        'data_query': zipped_data,
        'color': color,
        'query_category': zip(categories, result)
    }
    return render(request, 'profile/profile.html', context=context)


@login_required
def search(request):
    queryset = User.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(username__icontains=query) |
            Q(profile__batch__icontains=query) |
            Q(profile__name__icontains=query) |
            Q(profile__guidance__icontains=query) |
            Q(email__icontains=query)
        ).distinct()
    mentors = queryset.filter(profile__role=True).order_by(Lower('profile__name'))
    mentees = queryset.filter(profile__role=False).order_by(Lower('profile__name'))
    context = {
        'mentee': mentees,
        'mentors': mentors,
        'title': 'Members'
    }
    return render(request, 'member-list/search.html', context=context)


def user_list_view(request):
    mentors = Profile.objects.filter(role=True).order_by(Lower('name'))
    mentee = Profile.objects.filter(role=False).order_by(Lower('name'))
    context = {
        'mentors': mentors,
        'mentee': mentee,
        'title': "Members"
    }
    return render(request, 'member-list/trainers.html', context=context)


@login_required
def user_detail_view(request, pk):
    user = get_object_or_404(User, id=pk)
    badges = Reward.objects.filter(user=user).values('badges__title', 'badges__logo').annotate(Count('badges__title'))
    categories, data = user_chart_data(user)
    result = get_category_points_data(user, categories)
    zipped_data = zip(categories, data, color)
    context = {
        'title': f"{user.username}",
        'user': user,
        'badges': badges,
        'data_query': zipped_data,
        'color': color,
        'query_category': zip(categories, result)
    }

    return render(request, 'profile/profile-detail.html', context=context)


@login_required
def create_badge(request, id):
    user = get_object_or_404(User, id=id)
    form = RewardForm(request.POST or None)
    badges = Badge.objects.all().order_by(Lower('title'))
    if not request.user.profile.role:
        form.fields['badges'].queryset = Badge.objects.filter(featured=False).order_by(Lower('title'))
    else:
        form.fields['badges'].queryset = badges
    if request.POST:
        if form.is_valid():
            if user.id == request.user.id:
                messages.error(request, 'You cannot give a badge to yourself!')
            else:
                if form.instance.badges.featured:
                    if request.user.profile.role:
                        form.instance.user = user
                        if request.user.profile.name:
                            form.instance.awarded_by = request.user.profile.name
                        else:
                            form.instance.awarded_by = request.user.username
                        form.save()
                        messages.info(request, 'Your Badge submission is under review, it will be updated shortly')
                        return redirect(reverse('user-detail', kwargs={'pk': user.id}))
                    else:
                        messages.error(request, 'The badge that you have chosen can only be given by mentor')
                else:
                    form.instance.user = user
                    form.instance.awarded_by = request.user.username
                    form.save()
                    messages.info(request, 'Your Badge submission is under review, it will be updated shortly')
                    return redirect('trainers')

    context = {
        'heading': f'Give a badge to {user.username}',
        'form': form,
        'badges': badges
    }
    return render(request, 'badges/badge-create.html', context=context)


@login_required()
def badge(request):
    form = BadgeForm(request.POST or None)
    badges = Badge.objects.all().order_by(Lower('title'))
    if not request.user.profile.role:
        form.fields['badges'].queryset = Badge.objects.filter(featured=False).order_by(Lower('title'))
    else:
        form.fields['badges'].queryset = badges
    form.fields['user'].queryset = User.objects.all().order_by(Lower('username'))
    if request.POST:
        if form.is_valid():
            if form.instance.user.id == request.user.id:
                messages.error(request, 'You cannot give a badge to yourself!')
            else:
                row = form.save(commit=False)
                if request.user.profile.name:
                    row.awarded_by = request.user.profile.name
                else:
                    row.awarded_by = request.user.username
                row.save()
                messages.info(request, 'Your Badge submission is under review, it will be updated shortly')
                return redirect('trainers')
    context = {
        'form': form,
        'badges': badges
    }
    return render(request, 'badges/badge.html', context=context)


def multi_badge(request):
    if request.method == 'POST':
        form = MultiBadgeForm(request.POST)
        if form.is_valid():
            profiles = form.cleaned_data.get('profiles')
            badge = form.cleaned_data.get('badge')
            awarded = form.cleaned_data.get('awarded_by')
            describe = form.cleaned_data.get('description')
            
            for id in profiles:
                user = get_object_or_404(User, id=int(id))
                Reward.objects.create(user=user, description=describe, awarded_by=awarded, badges=get_object_or_404(Badge, id=int(badge)))
                messages.info(request, f'Badge awarded to {user.profile.name}')
            return redirect('trainers')

    else:
        form = MultiBadgeForm()
        context = {
            'form': form
        }
        return render(request, 'badges/multi-badge.html', context=context)



@login_required
def leader(request):
    data = Profile.objects.all()
    house = House.objects.all()
    team = Teams.objects.all()
    team = team.order_by('-points')
    house = house.order_by('-points')
    mentions = Mentions.objects.all().order_by('-id')[:6]
    context = {
        'data': data,
        'house': house,
        'teams': team,
        'title': 'Leaderboard',
        'mentions': mentions
    }
    return render(request, 'member-list/leader.html', context=context)


@login_required
def get_logs(request):
    if request.user.is_authenticated:
        return render(request, 'analytics/logs.html', context=None)


@login_required
def get_profile_file(request):
    if request.user.is_superuser:
        queryset = Profile.objects.all().values('user__username', 'name', 'batch', 'user__email'
                                                , 'phone', 'college', 'profession', 'linkedin',
                                                'github', 'okr', 'points', 'stars').order_by('name')
        return render_to_csv_response(queryset, filename='Sushiksha-Profiles' + str(datetime.date.today()),
                                      field_header_map={'user__username': 'Username', 'name': 'Name', 'batch': 'batch',
                                                        'user__email': 'email', 'phone': 'phone number',
                                                        'college': 'college',
                                                        'profession': 'profession', 'linkedin': 'linked in',
                                                        'github': 'github',
                                                        'okr': 'OKR', 'points': 'Total Points', 'stars': 'Stars'})


@login_required
def get_user_file(request):
    date = timezone.now()
    date_7 = date - datetime.timedelta(days=7)
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
    badges_received = Reward.objects.filter(user=user, timestamp__lte=date, timestamp__gt=date_7).values(
        'badges__category__name').annotate(Sum('badges__points'))
    for i in range(0, len(category_points)):
        category_points[i] = 0
    for category in badges_received:
        index = headers.index(category['badges__category__name'])
        category_points[index - badge_category_start] = category_points[
                                                            index - badge_category_start] + category[
                                                            'badges__points__sum']
        points = points + category['badges__points__sum']
    row_of_user = ["Week 1 " + str(date.date()) + ' -- ' + str(date_7.date())] + category_points + [points]
    writer.writerow(row_of_user)

    # week 2
    date = date_7
    date_7 = date - datetime.timedelta(days=7)
    points = 0
    badges_received = Reward.objects.filter(user=user, timestamp__lte=date, timestamp__gt=date_7).values(
        'badges__category__name').annotate(Sum('badges__points'))
    for i in range(0, len(category_points)):
        category_points[i] = 0
    for category in badges_received:
        index = headers.index(category['badges__category__name'])
        category_points[index - badge_category_start] = category_points[
                                                            index - badge_category_start] + category[
                                                            'badges__points__sum']
        points = points + category['badges__points__sum']
    row_of_user = ["Week 2 " + str(date.date()) + ' -- ' + str(date_7.date())] + category_points + [points]
    writer.writerow(row_of_user)

    # week 3
    date = date_7
    date_7 = date - datetime.timedelta(days=7)
    points = 0
    badges_received = Reward.objects.filter(user=user, timestamp__lte=date, timestamp__gt=date_7).values(
        'badges__category__name').annotate(Sum('badges__points'))
    for i in range(0, len(category_points)):
        category_points[i] = 0
    for category in badges_received:
        index = headers.index(category['badges__category__name'])
        category_points[index - badge_category_start] = category_points[
                                                            index - badge_category_start] + category[
                                                            'badges__points__sum']
        points = points + category['badges__points__sum']
    row_of_user = ["Week 3 " + str(date.date()) + ' -- ' + str(date_7.date())] + category_points + [points]
    writer.writerow(row_of_user)

    # week 4
    date = date_7
    date_7 = date - datetime.timedelta(days=7)
    points = 0
    badges_received = Reward.objects.filter(user=user, timestamp__lte=date, timestamp__gt=date_7).values(
        'badges__category__name').annotate(Sum('badges__points'))
    for i in range(0, len(category_points)):
        category_points[i] = 0
    for category in badges_received:
        index = headers.index(category['badges__category__name'])
        category_points[index - badge_category_start] = category_points[
                                                            index - badge_category_start] + category[
                                                            'badges__points__sum']
        points = points + category['badges__points__sum']
    row_of_user = ["Week 4 " + str(date.date()) + ' -- ' + str(date_7.date())] + category_points + [points]
    writer.writerow(row_of_user)

    return response


@login_required
def get_team_file(request):
    date = timezone.now()
    date_7 = date - datetime.timedelta(days=7)
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
        badges_received = Reward.objects.filter(user=member.user, timestamp__lte=date, timestamp__gt=date_7).values(
            'badges__category__name').annotate(Sum('badges__points'))
        for category in badges_received:
            index = headers.index(category['badges__category__name'])
            category_points[index - badge_category_start] = category_points[
                                                                index - badge_category_start] + category[
                                                                'badges__points__sum']
            points = points + category['badges__points__sum']
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
            response['Content-Disposition'] = 'attachment; filename=Sushiksha-All-Users-Points ' + str(
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
                badges_received = Reward.objects.filter(user=user, timestamp__lte=end, timestamp__gte=beginning).values(
                    'badges__category__name').annotate(Sum('badges__points'))
                for i in range(0, len(category_points)):
                    category_points[i] = 0
                for category in badges_received:
                    index = headers.index(category['badges__category__name'])
                    category_points[index - badge_category_start] = category_points[
                                                                        index - badge_category_start] + category[
                                                                        'badges__points__sum']
                    points = points + category['badges__points__sum']
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
        return render(request, 'analytics/logs-users.html', context=context)


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
                                                            timestamp__gte=beginning).values(
                        'badges__category__name').annotate(Sum('badges__points'))
                    for category in badges_received:
                        index = headers.index(category['badges__category__name'])
                        category_points[index - badge_category_start] = category_points[
                                                                            index - badge_category_start] + category[
                                                                            'badges__points__sum']
                        points = points + category['badges__points__sum']
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
        return render(request, 'analytics/logs-users.html', context=context)


@login_required
def get_single_user_file_large(request):
    if request.POST:
        form = UserRangeRequestForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            beginning = form.cleaned_data['beginning']
            end = form.cleaned_data['end']
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=Sushiksha-' + str(user) + '-Points' + str(
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
                                                        timestamp__gt=next).values('badges__category__name').annotate(
                    Sum('badges__points'))
                for category in badges_received:
                    index = headers.index(category['badges__category__name'])
                    category_points[index - badge_category_start] = category_points[
                                                                        index - badge_category_start] + category[
                                                                        'badges__points__sum']
                    points = points + category['badges__points__sum']
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
                                                    timestamp__gt=beginning).values('badges__category__name').annotate(
                Sum('badges__points'))
            for category in badges_received:
                index = headers.index(category['badges__category__name'])
                category_points[index - badge_category_start] = category_points[
                                                                    index - badge_category_start] + category[
                                                                    'badges__points__sum']
                points = points + category['badges__points__sum']
            row_of_team = ["Week " + str(week_counter) + '--' + str(end.date()) + ' -- ' + str(
                beginning.date())] + category_points + [
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
        return render(request, 'analytics/logs-users.html', context=context)
