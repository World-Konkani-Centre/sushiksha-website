from django.shortcuts import get_object_or_404, render, redirect
from .models import Contact, OneOneSession, Polls
from django.contrib import messages
from django.core.mail import send_mail


def contact(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        comment = request.POST['message']
        comment = name + " with the email, " + email + ", sent the following message:\n\n" + comment
        send_mail(subject, comment, None, ['sushikshawkc@gmail.com'])
        message = Contact()
        message.name = name
        message.email = email
        message.subject = subject
        message.comments = comment
        message.save()
        if email:
            messages.success(request, 'Thank you for showing interest in '
                                      'the Sushiksha, We will contact you '
                                      'within '
                                      '24hrs.')
        else:
            pass
        return redirect(request.META['HTTP_REFERER'])
    else:
        return render(request, 'webpages/contact.html', {})

def pentathlon(request):
    return render(request, 'event/pentathlon.html')

def sessions(request):
    query_set = OneOneSession.objects.all()
    context = {
        'sessions': query_set,
    }
    return render(request, 'event/sessions.html', context=context)


def poll(request):
    queryset = Polls.objects.all()
    context = {
        'title': 'Poll',
        'queryset': queryset
    }

    return render(request, 'poll/poll-list.html', context=context)


def vote(request, id, passw):
    pollv = get_object_or_404(Polls, id=id)
    if pollv.password != passw:
        messages.error(request, f'Wrong Password!!')
        return redirect('poll')
    
    context = {
        'title': f'{pollv.title}',
        'poll': pollv
    }

    return render(request, 'poll/poll-single.html', context=context)


def votepass(request, id):
    pollv = get_object_or_404(Polls, id=id)
    if request.POST:
        try:
            passw = int(request.POST.get('passw'))
            if pollv.password != passw:
                messages.error(request, f'Wrong Password!!')
                return redirect('auth-vote', id=id)
            return redirect('vote', id=id, passw=passw)
        except:
            return redirect('auth-vote', id=id)
        
    context = {
        'title': f'{pollv.title} Password',
        'poll': pollv
    }
    return render(request, 'poll/poll-auth.html', context=context)


def work_from_wkc(request):
    context = {
        'title': 'Work From WKC',
    }
    return render(request, 'badge_claim/blog.html', context=context)


    
def archive(request):
    return render(request, 'event/archive.html')
