from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class User(AbstractUser):
  username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
  email = models.EmailField(unique = True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']
  def __str__(self):
      return "{}".format(self.email)