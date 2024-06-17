from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class CodeSnapshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    repository_username = models.CharField(max_length=100)


class Opinion(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    on = models.ForeignKey(User, on_delete=models.CASCADE)
    opinion_type = models.CharField(max_length=100)


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Message(models.Model):
    message_text = models.TextField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
