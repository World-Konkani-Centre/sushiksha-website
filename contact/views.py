from django.shortcuts import render, redirect
from .models import Contact, Events
from django.contrib import messages
from django.core.mail import send_mail


def contact(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        comment = request.POST['message']
        comment = name + " with the email, " + email + ", sent the following message:\n\n" + comment
        send_mail(subject, comment, None, ['18praneeth@gmail.com'])
        message = Contact()
        message.name = name
        message.email = email
        message.subject = subject
        message.comments = comment
        message.save()
        if email:
            messages.success(request, 'Thank you for showing interest in '
                                      'the Sophists, We will contact you '
                                      'within '
                                      '24hrs.')
        else:
            pass
        return redirect(request.META['HTTP_REFERER'])
    else:
        return render(request, 'contact.html', {})


def events(request):
    events_query = Events.objects.all()
    context = {
        'event_list': events_query,
    }
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']

        comment = "Hello," + name + "Here is the link for the event"
        send_mail("Link Request", comment, None, [email])

        if name:
            messages.success(request, f'{name} Please check your mail for link')
        else:
            messages.error(request, 'There was an error while sending the mail')

        return redirect(request.META['HTTP_REFERER'])

    else:
        return render(request, 'events.html', context=context)

