from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import EntryCreationForm, ObjectiveCreationForm, KRCreationForm
from .models import Entry, Objective
from django.shortcuts import get_object_or_404


@login_required
def create_objectives(request):
    if request.POST:
        form = ObjectiveCreationForm(request.POST)
        if form.is_valid():
            objective = form.save(commit=False)
            objective.user = get_object_or_404(User, id=request.user.id)
            objective.save()
            messages.success(request, 'Objective Created successfully')
            return redirect('okr-view-data')
    else:
        form = ObjectiveCreationForm()
    context = {
        'form': form
    }
    return render(request, 'OKR/create_objectives.html', context=context)


@login_required
def create_key_results(request):
    if request.POST:
        form = KRCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Key Result Created successfully')
            return redirect('okr-view-data')
    form = KRCreationForm()
    form.fields['objective'].queryset = Objective.objects.filter(user=request.user)
    context = {
        'form': form
    }
    return render(request, 'OKR/create_kr.html', context=context)


@login_required
def insert_data(request):
    if request.POST:
        form = EntryCreationForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = get_object_or_404(User, id=request.user.id)
            entry.save()
            messages.success(request, 'Entry Created successfully')
            return redirect('okr-view-data')
    form = EntryCreationForm()
    context = {
        'form': form
    }
    return render(request, 'OKR/create_new_entry.html', context=context)


@login_required
def view_data(request):
    data = Entry.objects.filter(user=request.user)
    context = {
        'data': data
    }
    return render(request, 'OKR/show_entry.html', context=context)


@login_required
def load_okr(request):
    context = {

    }
    return render(request, 'webpages/index.html', context=context)
