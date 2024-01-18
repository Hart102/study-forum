from rest_framework.serializers import ModelSerializer
from base.models import Room



# Serializers converts pyhon data into json format
class RoomSerializer (ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'