from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.db import models


class CodeSnapshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    repository_username = models.CharField(max_length=100)


class Opinion(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opinion_by')
    on = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opinion_on')
    opinion_type = models.CharField(max_length=100)


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = PointField
    date = models.DateField(auto_now_add=True)


class Message(models.Model):
    message_text = models.TextField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
