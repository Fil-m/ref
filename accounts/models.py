# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Ad(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    url_name = models.CharField(max_length=100)  # Тут збережемо URL name, щоб використовувати в {% url %}
    order = models.IntegerField(default=0)  # Для сортування



    def __str__(self):
        return self.title