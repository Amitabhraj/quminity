from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    qid = models.CharField(max_length=15, unique=True, null=True, blank=True)
    anonymous = models.BooleanField(default=True,null=True, blank=True)
