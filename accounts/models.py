from django.contrib.auth.models import AbstractUser, User
from django.db import models


# class User(AbstractUser):
#     photo=models.ImageField()
#     adress=models.TextField()
#     date_of_brith=models.DateTimeField()
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='users/',blank=True,null=True)
    date_of_birth=models.DateField(blank=True,null=True)
    def __str__(self):
        return f"{self.user} profili"