from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone_nmb = models.CharField(max_length=12)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username
