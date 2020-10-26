from django.shortcuts import render
from contact.models import Testimonial, Faq
from users.models import House, Teams
from blog.models import Post
from django.shortcuts import get_object_or_404


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
    return render(request, 'index.html', context=context)


def about(request):
    context = {
        'title': 'About US'
    }
    return render(request, 'about.html', context=context)


def house(request, id):
    house_set = get_object_or_404(House, id=id)
    context = {
        'query_set': house_set
    }
    return render(request, 'house.html', context=context)


def team(request, id):
    team_set = get_object_or_404(Teams, id=id)
    context = {
        'query_set': team_set
    }
    return render(request, 'team.html', context=context)
