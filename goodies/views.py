from django.shortcuts import render, get_object_or_404
from .models import Goodie


def goodies(request):
    queryset = Goodie.objects.all().filter(is_shown=True)
    context = {
        'queryset': queryset,
        'title': 'Goodies'
    }
    return render(request, 'goodies/goodies.html', context)


def cart(request, id):
    item = get_object_or_404(Goodie, id=id)
    context = {
        'item': item,
        'title': 'Cart'
    }
    return render(request, 'goodies/cart.html', context)


def category_goodies(request,tag):
    queryset = Goodie.objects.filter(is_shown=True,tag=tag)
    context = {
        'queryset':queryset,
        'title':'Goodies'
    }
    return render(request, 'goodies/goodies.html', context)