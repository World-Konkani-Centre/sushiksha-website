from django.shortcuts import render
from .models import Goodie


def goodies(request):
    queryset = Goodie.objects.all().filter(is_shown=True)
    context = {
        'queryset': queryset,
        'title': 'Goodies'
    }
    return render(request, 'goodies/goodies.html', context)