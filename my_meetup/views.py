
#from pyexpat.errors import messages
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .forms import MyUserRegistration, RegistrationForm, UserMeetupForm, Profileform, SpeakerForm
from . models import Meetup, MyUser, Speaker
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
import datetime



# Create your views here.

#Login View
def index(request):
    return render(request, 'my_meetup/main.html')
def loginpage(request):
    if request.user.is_authenticated:
        redirect('home')
    if request.method=='POST':
        email=request.POST.get('email')
       
        password=request.POST.get('password')
  
        try:
            user=MyUser.objects.get(email=email)
        except:
            messages.error(request, 'username does not exist')
        user=authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
             messages.error(request, 'password does not match')
    return render(request, 'my_meetup/login.html')

def add_speaker(request, slug):
    
    try:
        selected_meetup=Meetup.objects.get(slug=slug)
        if request.method=='GET':
            speaker_form=SpeakerForm()
        else:
            speaker_form=SpeakerForm(request.POST, request.FILES)
            if speaker_form.is_valid():
                speaker_form.instance.user==request.user.id
                speaker_form.instance.meetup_name=selected_meetup.title
                speaker=speaker_form.save(commit=False)
                speaker=speaker_form.save()
                selected_meetup.meetup_speakers.add(speaker)
                return redirect('home')
            
        return render(request, 'meetups/speaker_form.html', {
            'meetup':selected_meetup,
            'form':speaker_form,


                })
    except Exception as exc:
        return redirect('home')


def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    meetups=Meetup.objects.filter(activate=True)
    meetups=meetups.filter(
        Q(title__icontains=q)|
        Q(location_name__icontains=q)|
        Q(to_date__icontains=q))


    count=meetups.count()
    meetups=meetups.order_by('-create')
    return render(request, 'my_meetup/home.html', {'meetups':meetups, 'count':count})


#User registration
def register(request):
    form=MyUserRegistration()
    if request.method=="POST":
        form=MyUserRegistration(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    
    return render(request, 'my_meetup/register.html',{'form':form})


        
def meetup_details(request, pk):
    try:
        selected_meetup=Meetup.objects.get(pk=pk)
        if request.method=='GET':
            registration_form=RegistrationForm()
        else:
            registration_form=RegistrationForm(request.POST)
            if registration_form.is_valid():
                participant=registration_form.save()
                selected_meetup.participants.add(participant)
                return redirect('comfirm-registration')
        return render(request, 'my_meetup/meetup_details.html', {
            'meetup': selected_meetup,
            'form':registration_form
        })
        
    except Exception as exc:
        selected_meetup=Meetup.objects.get(pk=pk)
        return render(request, 'my_meetup/meetup_details.html', {'form':registration_form}) 


def upcoming_meetups(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    meetups=Meetup.objects.filter(activate=True)
    todayDate=datetime.date.today()
    meetups=meetups.filter(
        Q(title__icontains=q)|
        Q(location_name__icontains=q)|
        Q(from_date__icontains=q)|
        Q(to_date__icontains=q)
        )
    meetups=meetups.order_by('-create')
    return render(request, 'meetups/upcoming_meetups.html', {
        'todayDate':todayDate,
        'meetups':meetups
        
        })




def user_meetup(request, pk):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    user_meetups=Meetup.objects.filter(user=pk)
    user_meetups=user_meetups.order_by('-create')
    user_meetups=user_meetups.filter(
        Q(title__icontains=q)|
        Q(location_name__icontains=q)
    )
    count=user_meetups.count()

    return render(request, 'my_meetup/user_meetups.html', {'meetups':user_meetups, 'count':count})


#Update view
class MeetupUpdate(LoginRequiredMixin, UpdateView):
    model=Meetup
    form_class=UserMeetupForm
    template_name='my_meetup/meetup_form.html'
    success_url=reverse_lazy('home')




class MeetupCreate(LoginRequiredMixin, CreateView):
    model=Meetup
    form_class=UserMeetupForm
    success_url=reverse_lazy('home')
    template_name='my_meetup/meetup_form.html'
    def form_valid(self, form): 
        form.instance.user=self.request.user
        form.instance.slug=form.instance.title.replace(' ', '-').lower()
        return super(MeetupCreate, self).form_valid(form)


class MeetupDelete(LoginRequiredMixin, DeleteView):
    model=Meetup
    context_object_name='meetup'
    template_name='my_meetup/delete_meetup.html'
    success_url=reverse_lazy('home')

def profile(request, pk):
    user=request.user
    form=Profileform(instance=user)
    if request.method=='POST':
        form=Profileform(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'my_meetup/profile.html', {'form':form})

@login_required(login_url='login')
def user_speakers(request, pk):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    
    user_speakers=Speaker.objects.order_by('-id')
    user_speakers=Speaker.objects.filter(user=pk)
    speakers=user_speakers.filter(
        Q(name__icontains=q)|
        Q(meetup_name__icontains=q)
        
        ) 
    count=user_speakers.count()
    return render(request, 'my_meetup/user_speakers.html', {'speakers':speakers, 'count':count} )

#speakers update
class SpeakerUpdate(LoginRequiredMixin, UpdateView):
    model=Speaker
    form_class = SpeakerForm
    template_name='my_meetup/add_speakers.html'
    success_url=reverse_lazy('meetups')
    
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(SpeakerUpdate, self).form_valid(form)
    
#Delete Speakers
class SpeakerDelete(LoginRequiredMixin,DeleteView):
    model=Speaker
    context_object_name='speaker'
    template_name='my_meetup/delete_speaker.html'
    success_url=reverse_lazy('meetups')


def comfirm_registration(request):
    return render(request, 'my_meetup/registration_success.html')
