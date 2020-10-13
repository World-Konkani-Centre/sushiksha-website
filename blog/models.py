from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile
from tinymce import HTMLField


class Categories(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='blog-post-thumbnail')
    categories = models.ManyToManyField(Categories)

    def __str__(self):
        return f"{self.author.user.username} post {self.title}"

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'id': self.pk})

    def get_update_url(self):
        return reverse('blog-update', kwargs={'id': self.pk})

    def get_delete_url(self):
        return reverse('blog-delete', kwargs={'id': self.pk})

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Comment"
