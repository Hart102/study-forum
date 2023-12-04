from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message

# Register tables to view them on django admin dashboard
admin.site.register(Room) 
admin.site.register(Topic)
admin.site.register(Message)
