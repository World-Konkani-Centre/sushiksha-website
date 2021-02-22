from django.contrib.auth.models import User
from django.db import models

STATUS = (
    ("Getting Ready", "Getting Ready"),
    ("Packaging", "Packaging"),
    ("Transporting", "Transporting"),
    ("Delivered", "Delivered"),
)


class Goodie(models.Model):
    title = models.CharField(max_length=30)
    suShells = models.IntegerField(default=0)
    tag = models.CharField(max_length=10)
    is_shown = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to='goodies')
    is_link = models.BooleanField(default=False)
    description = models.TextField()
    is_image = models.BooleanField(default=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}'


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET("User Deleted"))
    goodie = models.ForeignKey(Goodie, on_delete=models.SET("Goodie Deleted"))
    status = models.CharField(max_length=40, choices=STATUS, default="Getting Ready")
    tracking_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.user}--{self.goodie}'
