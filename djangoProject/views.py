from django.shortcuts import render
from contact.models import Testimonial, Faq
from users.models import House, Teams
from django.shortcuts import get_object_or_404


def index(request):
    faqs = Faq.objects.all()
    context = {
        'faqs': faqs,
        'title': 'Home'
    }
    return render(request, 'index.html', context=context)


def about(request):
    testimonial = Testimonial.objects.all()
    context = {
        'testimonial': testimonial,
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
