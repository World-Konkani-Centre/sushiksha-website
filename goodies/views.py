from django.shortcuts import render


def goodies(request):
    return render(request, 'goodies/goodies.html')