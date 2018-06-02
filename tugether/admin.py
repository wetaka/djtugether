from django.contrib import admin

# Register your models here.
from tugether.models import User, Event, Comment, Category, Noti

class EventAdmin(admin.ModelAdmin) :


    list_display = ('id', 'createby','location', 'approve','description',
        'facebook','line','web','phone','bcapprove','createdate',
        'updatedate','eventstdate','eventenddate','active','limited')

    list_editable = ('approve',)



admin.site.register(Event, EventAdmin)
