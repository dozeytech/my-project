from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    name=models.CharField(max_length=200, null=True)
    email=models.EmailField(unique=True, null=True)
    bio=models.TextField(null=True)
    image=models. ImageField(null=True)
    phone=models.CharField(max_length=200, blank=True, null=True)
    birth_date=models.DateField(null=True, blank=True)
    REQUIRED_FIELDS=[]
    #USERNAME_FIELD= 'email'

class Participant(models.Model):
    email=models.EmailField()
    def __str__(self):
        return self.email
class Speaker(models.Model):
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=50, null=True, blank=True)
    phone=models.CharField(max_length=50)
    image=models.ImageField(upload_to='speaker_images')
    bio=models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

class Meetup(models.Model):
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True,)
    title=models.CharField(max_length=200, unique=True)
    organizer_email=models.EmailField(max_length=200, null=True)
    slug=models.SlugField(unique=True)
    description=models.TextField()
    image=models.ImageField(upload_to='my_meetup_images')
    location_name=models.CharField(max_length=200, null=True, blank=True)
    location_address=models.TextField()
    activate=models.BooleanField(default=True)
    create=models.DateTimeField(auto_now_add=True)
    meetup_date=models.DateField(null=True, blank=True)
    meetup_time=models.TimeField()
    from_date=models.DateField()
    to_date=models.DateField()


    def __str__(self):
        return f'{self.title}-{self.organizer_email}'
