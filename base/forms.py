from django.forms import ModelForm
from .models import Room

# Generating a dynamic form based on the fields defined in room class
# THis for is used in creating rooms
class RoomForm (ModelForm):
    class Meta:
        model = Room
        fields = "__all__"