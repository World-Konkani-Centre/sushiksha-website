from django.shortcuts import render
from users.models import Reward
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .filters import RewardFilter


def badge_list(request):
    query = Reward.objects.order_by('-timestamp')

    f = RewardFilter(request.GET, queryset=query)
    paginated_queryset = f.qs

    paginator = Paginator(paginated_queryset, 10)

    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'query': paginated_queryset,
        'reward_filter': f,
        'page_request_var': page_request_var,
        'title': "Badges awarded"
    }
    return render(request, 'rewards.html', context=context)


def badge_search(request):
    queryset = Reward.objects.order_by('-timestamp')
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(user__username__icontains=query) |
            Q(user__profile__name__icontains=query) |
            Q(awarded_by=query) |
            Q(badges__title__icontains=query)
        ).distinct()

    paginator = Paginator(queryset, 40)

    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'query': paginated_queryset,
        'page_request_var': page_request_var,
        'title': "Badges awarded"
    }

    return render(request, 'rewards.html', context=context)
