from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def __str__(self):
        return self.username

    @property
    def full_name(self):

        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        if self.first_name:
            return self.first_name

        return None


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')

    image = models.ImageField(upload_to='user/image/', default='user/default.png')
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    profession = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
