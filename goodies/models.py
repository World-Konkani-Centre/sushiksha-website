from django.db import models


class Goodie(models.Model):
    title = models.CharField(max_length=30)
    tag = models.CharField(max_length=10)
    is_shown = models.BooleanField(default=True)
    thumbline = models.ImageField(upload_to='goodies')
    is_link = models.BooleanField(default=False)
    description = models.TextField()
    is_image = models.BooleanField(default=True)
    hd_image = models.ImageField(upload_to='goodies', blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}'
