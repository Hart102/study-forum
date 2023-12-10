from django.forms import ModelForm
from .models import Room

# Generating a dynamic form based on the fields defined in room class
# THis was used in creating rooms
class RoomForm (ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ['host', 'participants'] # Exclude this field while generating a form