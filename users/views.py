from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import UserUpdateForm, ProfileUpdateForm, RewardForm, UserRegisterForm, BadgeForm
from .models import Pomodoro, Badge, Profile, House, Teams
from .utils import collect_badges, get_house_data, get_team_data


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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have logged into your account!')
            return redirect('home')

        else:
            messages.error(request, 'Invalid Credential')
            return redirect(request.META['HTTP_REFERER'])
    else:
        return render(request, 'login.html', {'title': "Login"})


@login_required
def profile(request):
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

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': "Profile",
        'badges': zipped_data,
    }
    return render(request, 'profile.html', context=context)


@login_required
def log_pomodoro(request):
    pomodoro = Pomodoro.objects.filter(user=request.user).first()

    if request.POST:
        productivity = int(request.POST['productivity'])
        energy = int(request.POST['energy'])
        productivity = round((productivity * 0.05), 2)
        energy = round((energy * 0.05), 2)
        pomodoro.count += 1
        pomodoro.energy = (pomodoro.energy + energy)/2
        pomodoro.productivity = (pomodoro.productivity + productivity)/2
        pomodoro.save()
        messages.success(request, f'Your data has been recorded.')
        return redirect(request.META['HTTP_REFERER'])
    else:
        data = Pomodoro.objects.all().order_by('-count')
        context = {
            'leaderboard': data,
            'title': "Analytics",
        }
        for i in data:
            print(i, i.id, i.count, i.user.profile.image.url)
        return render(request, 'leaderboard.html', context=context)


@login_required
def search(request):
    queryset = User.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(username__icontains=query) |
            Q(profile__batch__icontains=query) |
            Q(profile__guidance__icontains=query) |
            Q(email__icontains=query)
        ).distinct()

    context = {
        'users': queryset
    }
    return render(request, 'trainers.html', context=context)


class UserListView(ListView):
    model = User
    template_name = 'trainers.html'
    context_object_name = 'users'


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
    badges = Badge.objects.all()
    if request.POST:
        if form.is_valid():
            if user.id == request.user.id:
                messages.error(request, 'You cannot give a badge to yourself!')
            else:
                if form.instance.badges.featured:
                    if request.user.profile.role:
                        form.instance.user = user
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
                    return redirect(reverse('user-detail', kwargs={'pk': user.id}))

    context = {
        'heading': f'Give a badge to {user.username}',
        'form': form,
        'badges': badges
    }
    return render(request, 'badge-create.html', context=context)


@login_required()
def badge(request):
    form = BadgeForm(request.POST or None)
    badges = Badge.objects.all()
    if request.POST:
        if form.is_valid():
            if form.instance.user.id == request.user.id:
                messages.error(request, 'You cannot give a badge to yourself!')
            else:
                if form.instance.badges.featured:
                    if request.user.profile.role:
                        form.instance.awarded_by = request.user.username
                        form.save()
                        messages.info(request, 'Your Badge submission is under review, it will be updated shortly')
                        return redirect(reverse('user-detail', kwargs={'pk': form.instance.user.id}))
                    else:
                        messages.error(request, 'The badge that you have chosen can only be given by mentor')
                else:
                    form.instance.awarded_by = request.user.username
                    form.save()
                    messages.info(request, 'Your Badge submission is under review, it will be updated shortly')
                    return redirect(reverse('user-detail', kwargs={'pk': form.instance.user.id}))

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
