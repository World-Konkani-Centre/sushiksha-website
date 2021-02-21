from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from users.models import Profile
from .models import Goodie, Orders


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


def category_goodies(request, tag):
    queryset = Goodie.objects.filter(is_shown=True, tag=tag)
    context = {
        'queryset': queryset,
        'title': 'Goodies'
    }
    return render(request, 'goodies/goodies.html', context)


def place(request, id):
    goodie = get_object_or_404(Goodie, id=id)
    user = get_object_or_404(User, id=request.user.id)
    profile = get_object_or_404(Profile, user=user)
    if profile.suShells < goodie.suShells or profile.rank != "Caesar":
        messages.error(request, "Your order for " + goodie.title + " could not be placed, insufficient amount/rank not "
                                                                   "attained")
        return redirect('goodies')
    profile.suShells -= goodie.suShells
    profile.save()
    Orders.objects.create(user=user, goodie=goodie)
    messages.success(request, "Your order for " + goodie.title + " has been placed")
    return redirect('goodies')
