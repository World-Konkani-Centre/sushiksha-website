from django.contrib.auth.models import User
from django.db import models


class Objective(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    objective = models.CharField(max_length=80)

    def __str__(self):
        return self.objective

    class Meta:
        verbose_name = "Objective"
        verbose_name_plural = "Objectives"


class KR(models.Model):
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    key_result = models.CharField(max_length=80)
    hours = models.IntegerField(default=1, help_text="Number of hours you wish to spend on this kr")
    percentage = models.IntegerField(help_text="What is the completion percentage", default=0)

    def __str__(self):
        return f'{self.key_result}'

    class Meta:
        verbose_name = "Key Result"
        verbose_name_plural = "Key Results"


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    key_result = models.ForeignKey(KR, on_delete=models.CASCADE)
    update = models.TextField(help_text="Brief description on the progress")
    time_spent = models.IntegerField(default=0, help_text="Time spent on the task in minutes")

    def __str__(self):
        return f'{self.user}-{self.date_time}'

    class Meta:
        verbose_name = "Entry"
        verbose_name_plural = "Entries"
