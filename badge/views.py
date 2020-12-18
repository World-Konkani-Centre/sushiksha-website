from django.shortcuts import render
from users.models import Reward
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def badge_list(request):
    query = Reward.objects.order_by('-timestamp')
    paginator = Paginator(query, 15)

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
