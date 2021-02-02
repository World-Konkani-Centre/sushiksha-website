from django.shortcuts import render, redirect
from contact.models import Testimonial, Faq
from users.models import House, Teams
from blog.models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout


def index(request):
    featured = Post.objects.filter(featured=True)
    faqs = Faq.objects.all()
    testimonial = Testimonial.objects.all()
    context = {
        'faqs': faqs,
        'testimonial': testimonial,
        'featured': featured,
        'title': 'Home'
    }
    return render(request, 'webpages/index.html', context=context)


def about(request):
    # featured = Gallery.objects.filter(featured=True)
    # common = Gallery.objects.filter(featured=False)
    context = {
        'title': 'About US',
        # 'featured': featured,
        # 'common': common
    }
    return render(request, 'webpages/about.html', context=context)


def house(request, id):
    house_set = get_object_or_404(House, id=id)
    context = {
        'query_set': house_set
    }
    return render(request, 'member-list/house.html', context=context)


def team(request, id):
    team_set = get_object_or_404(Teams, id=id)
    context = {
        'query_set': team_set
    }
    return render(request, 'member-list/team.html', context=context)


def handler404(request, exception):
    context = {
        'error_no': 404,
        'error_detail': 'Page Not Found'
    }
    return render(request, 'webpages/404.html', context)


def handler500(request):
    context = {
        'error_no': 500,
        'error_detail': 'Server Error'
    }
    return render(request, 'webpages/404.html', context)


def handler400(request, exception):
    context = {
        'error_no': 400,
        'error_detail': 'Bad Request'
    }
    return render(request, 'webpages/404.html', context)


def handler403(request, exception):
    context = {
        'error_no': 403,
        'error_detail': 'Permission Denied'
    }
    return render(request, 'webpages/404.html', context)


def my_logout(request):
    logout(request)
    return redirect('home')
