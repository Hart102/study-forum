from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

# Generating a dynamic form based on the fields defined in room class
# THis was used in creating rooms
class RoomForm (ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ['host', 'participants'] # Exclude this field while generating a form


class UserForm (ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']