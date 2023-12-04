from django.db import models
from django.contrib.auth.models import User

# This database is built using one to many relationship architecture

class Topic (models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name


class Room (models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null = True) # Refers to the owner of the room (One to many relationship)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True) # connceting Room and Topic table 
    name = models.CharField(max_length = 200)
    description = models.TextField(null = True, blank = True) # null = true: allows description to be empty in the db. blank = true: allows user to submit an empty form
    participants = models.ManyToManyField(User, related_name = "participants", blank = True) # This creates a many to many relationship
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta: # This displays the latest created and updated rooms first (Sorting)
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message (models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE) # Connecting user and message table
    room = models.ForeignKey(Room, on_delete = models.CASCADE) # Delete messages if the Room is deleted
    body = models.TextField()
    update = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return self.body[0:50]