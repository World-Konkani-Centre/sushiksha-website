from django.shortcuts import render, redirect
from .models import Contact, OneOneSession
from django.contrib import messages
from django.core.mail import send_mail
# from django.contrib.auth.decorators import login_required
# from .forms import GalleryForm


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
        return render(request, 'webpages/contact.html', {})


# def events(request):
#     events_query = Events.objects.all()
#     context = {
#         'event_list': events_query,
#     }
#     if request.POST:
#         name = request.POST['name']
#         email = request.POST['email']
#
#         comment = "Hello," + name + "Here is the link for the event"
#         send_mail("Link Request", comment, None, [email])
#
#         if name:
#             messages.success(request, f'{name} Please check your mail for link')
#         else:
#             messages.error(request, 'There was an error while sending the mail')
#
#         return redirect(request.META['HTTP_REFERER'])
#
#     else:
#         return render(request, 'events.html', context=context)


# @login_required
# def gallery(request):
#     form = GalleryForm(request.POST, request.FILES)
#     if request.POST:
#         if form.is_valid():
#             form.instance.user = request.user
#             form.save()
#             messages.success(request, 'Image added')
#             return redirect('about')
#     context = {
#         'form': form
#     }
#     return render(request, 'gallery_photo_submit.html', context=context)


def pentathlon(request):
    return render(request, 'event/pentathlon.html')

def sessions(request):
    query_set = OneOneSession.objects.all()
    context = {
        'sessions': query_set,
    }
    return render(request, 'event/sessions.html', context=context)
