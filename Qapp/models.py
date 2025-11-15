from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    qid = models.CharField(max_length=15, unique=True, null=True, blank=True)
    anonymous = models.BooleanField(default=True,null=True, blank=True)

    def __str__(self):
        return self.username
    
    def get_full_name(self):   
        return f"{self.first_name} {self.last_name}"

class Features(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name