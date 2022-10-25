from django.contrib import admin
from.models import MyUser, Meetup, Speaker, Participant
# Register your models here.
class MeetupAdmin(admin.ModelAdmin):
    list_display=('title', 'slug', 'user',)
    list_filter=('title',)
    prepopulated_fields={'slug': ('title',)}
class SpeakerAdmin(admin.ModelAdmin):
    list_display=('name', 'email', 'phone','user',)
    list_filter=('name',)

admin.site.register(MyUser)
admin.site.register(Meetup, MeetupAdmin)
admin.site.register(Participant)
admin.site.register(Speaker,SpeakerAdmin)