from tkinter import Widget
from turtle import textinput
from xml.dom.minidom import Attr
from.models import Meetup, MyUser, Participant, Speaker
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, Textarea, PasswordInput,DateTimeInput, DateInput
#from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, CheckBoxInput



class UserMeetupForm(forms.ModelForm):
    class Meta:
        model=Meetup
        fields=['title','from_date', 'to_date', 'meetup_time', 'description', 'organizer_email', 'location_name', 'location_address', 'activate','image']

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=Participant
        fields=['email']

class MyUserRegistration(UserCreationForm):
    class Meta:
        model=MyUser
        fields=['name', 'username', 'email', 'password1', 'password2']

class SpeakerForm(forms.ModelForm):
    class Meta:
        model=Speaker
        fields=['name', 'email', 'phone', 'bio', 'image']


class Profileform(ModelForm):
    class Meta:
        model=MyUser
        fields=['username', 'name','email', 'bio', 'phone', 'birth_date', 'image']