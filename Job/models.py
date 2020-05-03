from django.db import models
# from django.contrib.auth.models import User
import datetime
from django_in_telugu import settings
from django.utils import timezone


class Job(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    title = models.CharField(max_length=200)
    created_on = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='media/profile_pics', width_field=200, height_field=200)
    salary = models.FloatField()

    def __str__(self):
        return self.author
