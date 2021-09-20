from django.shortcuts import render
from users.models import Reward
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from .filters import RewardFilter
from .models import BadgeClaim


def badge_list(request):
    query = Reward.objects.order_by('-timestamp')

    f = RewardFilter(request.GET, queryset=query)
    paginated_queryset = f.qs

    paginator = Paginator(paginated_queryset, 30)

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
    return render(request, 'badges/rewards.html', context=context)


def badge_claim(request):
    claim_forms = BadgeClaim.objects.all()
    context = {
        'forms': claim_forms
    }
    return render(request, 'badges/badge_claim_list.html', context=context)


def badge_claim_form(request, pk):
    form = get_object_or_404(BadgeClaim, id=pk)
    context = {
        'form': form
    }
    return render(request, 'badges/badge_claim_form.html', context=context)
