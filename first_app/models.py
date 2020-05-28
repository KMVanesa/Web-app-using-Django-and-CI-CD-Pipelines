from django.db import models
from django.contrib.auth.models import User


# class Register(models.Model):
#     email = models.EmailField(max_length=50, unique=True)
#     first_name = models.CharField(max_length=264)
#     last_name = models.CharField(max_length=264)
#     password = models.CharField(max_length=264)
#
#     def __str__(self):
#         return self.email


# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
