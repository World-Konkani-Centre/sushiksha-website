import csv
import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils import timezone
from djqscsv import render_to_csv_response

from .forms import UserUpdateForm, ProfileUpdateForm, RewardForm, UserRegisterForm, BadgeForm
from .models import Pomodoro, Badge, Profile, House, Teams, Reward, BadgeCategory
from .utils import collect_badges, get_house_data, get_team_data, email_check


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
    return render(request, 'register.html', context)


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
        return render(request, 'login.html', {'title': "Login"})


@login_required
def profile(request):
    profile_details = {}
    reward, count = collect_badges(request.user)
    zipped_data = zip(reward, count)
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
            'degree':query.degree,
            'branch':query.branch,
            'profession': query.profession,
            'address': query.address,
            'guidance': query.guidance,
        }
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': "Profile",
        'badges': zipped_data,
        'profile_details': profile_details
    }
    return render(request, 'profile.html', context=context)


# @login_required
# def log_pomodoro(request):
#     pomodoro = Pomodoro.objects.filter(user=request.user).first()
#
#     if request.POST:
#         productivity = int(request.POST['productivity'])
#         energy = int(request.POST['energy'])
#         productivity = round((productivity * 0.05), 2)
#         energy = round((energy * 0.05), 2)
#         pomodoro.count += 1
#         pomodoro.energy = (pomodoro.energy + energy) / 2
#         pomodoro.productivity = (pomodoro.productivity + productivity) / 2
#         pomodoro.save()
#         messages.success(request, f'Your data has been recorded.')
#         return redirect(request.META['HTTP_REFERER'])
#     else:
#         data = Pomodoro.objects.all().order_by('-count')
#         context = {
#             'leaderboard': data,
#             'title': "Analytics",
#         }
#         for i in data:
#             print(i, i.id, i.count, i.user.profile.image.url)
#         return render(request, 'leaderboard.html', context=context)


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
    mentors = queryset.filter(profile__role=True)
    mentees = queryset.filter(profile__role=False)
    context = {
        'mentee': mentees,
        'mentors': mentors,
        'title': 'Members'
    }
    for user in mentees:
        print(user)
    for user in mentors:
        print(user)
    return render(request, 'search.html', context=context)


# class UserListView(ListView):
#     model = User
#     template_name = 'trainers.html'
#     context_object_name = 'users'


def user_list_view(request):
    mentors = Profile.objects.filter(role=True).order_by(Lower('user__username'))
    mentee = Profile.objects.filter(role=False).order_by(Lower('user__username'))
    context = {
        'mentors': mentors,
        'mentee': mentee,
        'title': "Members"
    }
    return render(request, 'trainers.html', context=context)


@login_required
def user_detail_view(request, pk):
    user = get_object_or_404(User, id=pk)
    reward, count = collect_badges(user)
    zipped_data = zip(reward, count)

    context = {
        'title': f"{user.username}",
        'user': user,
        'badges': zipped_data,
    }

    return render(request, 'profile-detail.html', context=context)


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
    return render(request, 'badge-create.html', context=context)


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
    return render(request, 'badge.html', context=context)


@login_required
def leader(request):
    data = Profile.objects.all()
    house = House.objects.all()
    team = Teams.objects.all()
    get_house_data(houses=house)
    get_team_data(teams=team)
    team = team.order_by('-points')
    house = house.order_by('-points')
    context = {
        'data': data,
        'house': house,
        'teams': team,
        'title': 'Leaderboard'
    }
    return render(request, 'leader.html', context=context)


@login_required
def get_logs(request):
    if request.user.is_superuser:
        return render(request, 'logs.html', context=None)


@login_required
def get_profile_file(request):
    if request.user.is_superuser:
        queryset = Profile.objects.all().values('user__username', 'name', 'batch', 'user__email'
                                                , 'phone', 'college', 'profession', 'linkedin',
                                                'github', 'okr', 'points', 'stars')
        return render_to_csv_response(queryset, filename='Sushiksha-Profiles' + str(datetime.date.today()),
                                      field_header_map={'user__username': 'Username', 'name': 'Name', 'batch': 'batch',
                                                        'user__email': 'email', 'phone': 'phone number',
                                                        'college': 'college',
                                                        'profession': 'profession', 'linkedin': 'linked in',
                                                        'github': 'github',
                                                        'okr': 'OKR', 'points': 'Total Points', 'stars': 'Stars'})


@login_required
def get_team_file(request):
    date = timezone.now()
    date_7 = date - datetime.timedelta(days=7)
    date_7 = date_7.date()
    if request.user.is_superuser:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Sushiksha-Team-Points' + str(
            datetime.date.today()) + '.csv'
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
                badges_received = Reward.objects.filter(user=member.user, timestamp__lte=date,timestamp__gt=date_7)
                for _badge in badges_received:
                    category_points[headers.index(_badge.badges.category.name) - badge_category_start] = \
                        category_points[
                            headers.index(
                                _badge.badges.category.name) - badge_category_start] + _badge.badges.points
                    points = points + _badge.badges.points
            row_of_team = [team.name, team.points] + category_points + [points]
            writer.writerow(row_of_team)
        return response


@login_required
def get_user_file(request):
    date = timezone.now()
    date_7 = date - datetime.timedelta(days=7)
    date_7 = date_7.date()
    if request.user.is_superuser:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Sushiksha-User-Points' + str(
            datetime.date.today()) + '.csv'
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

        users = User.objects.all().order_by('username')

        for user in users:
            points = 0
            badges_received = Reward.objects.filter(user=user, timestamp__lte=date,timestamp__gt=date_7)
            for i in range(0, len(category_points)):
                category_points[i] = 0
            for _badge in badges_received:
                category_points[headers.index(_badge.badges.category.name) - badge_category_start] = category_points[
                                                                                                         headers.index(
                                                                                                             _badge.badges.category.name) - badge_category_start] + _badge.badges.points
                points = points + _badge.badges.points
            row_of_user = [user.username, user.profile.name, user.email, user.profile.batch, user.profile.points,
                           user.profile.stars] + category_points + [points]
            writer.writerow(row_of_user)
        return response


@login_required
def get_house_file(request):
    date = timezone.now()
    date_7 = date - datetime.timedelta(days=7)
    date_7 = date_7.date()
    if request.user.is_superuser:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Sushiksha-House-Points' + str(
            datetime.date.today()) + '.csv'
        writer = csv.writer(response)
        headers = ['House Name', 'House Points']
        badge_category_start = 2
        category_points = []
        categories = BadgeCategory.objects.all().order_by('name')
        for category in categories:
            headers.append(category.name)
            category_points.append(0)
        headers.append('Points This Week')
        writer.writerow(headers)

        houses = House.objects.all().order_by('name')

        for house in houses:
            teams = house.teams.all()
            points = 0
            for i in range(0, len(category_points)):
                category_points[i] = 0
            for team in teams:
                members = team.members.all()
                for member in members:
                    badges_received = Reward.objects.filter(user=member.user,timestamp__lte=date,timestamp__gt=date_7)
                    for _badge in badges_received:
                        category_points[headers.index(_badge.badges.category.name) - badge_category_start] = \
                            category_points[headers.index(
                                _badge.badges.category.name) - badge_category_start] + _badge.badges.points
                        points = points + _badge.badges.points
            row_of_house = [house.name, house.points] + category_points + [points]
            writer.writerow(row_of_house)
        return response
