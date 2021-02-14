from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    comments = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Events(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    date_and_time = models.CharField(max_length=50)
    link = models.URLField(default='https://us02web.zoom.us/j/89238479481?pwd=VG5SRzZlUjBWQUpBd1NEbm4yS2Z1Zz09')
    poster = models.ImageField(upload_to='events')

    def __str__(self):
        return self.title


class Faq(models.Model):
    short_title = models.CharField(max_length=50)
    question = models.CharField(max_length=300)
    answer = models.TextField()

    def __str__(self):
        return self.short_title


class Testimonial(models.Model):
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    image = models.ImageField(upload_to='testimonial')
    testimonial = models.TextField()

    def __str__(self):
        return f'{self.name} Testimonial'


class Gallery(models.Model):
    name = models.CharField(max_length=30)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='gallery')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}s uploaded {self.name}'


class OneOneSession(models.Model):
    heading = models.CharField(max_length=100, help_text='Heading to be displayed')
    overview = models.TextField(help_text='Description for each entries')
    button_name = models.CharField(max_length=40, help_text='The text which will be displayed on button')
    url = models.URLField(help_text="Calendly link or any other calender link which can be accessed by only logged user")
    color = ColorField(format='hexa', help_text='The accent color of the card')
    image = models.ImageField(upload_to='oneonesession', help_text='Image to be displayed in the card')

    class Meta:
        verbose_name = 'Mentor Session'
        verbose_name_plural = 'Mentors Sessions'
