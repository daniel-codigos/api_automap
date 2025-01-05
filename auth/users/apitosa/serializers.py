from rest_framework.serializers import ModelSerializer
#from auth.users.models import show_info
from ..models import *



class show_info_serializer(ModelSerializer):
    class Meta:
        model = show_info
        fields = '__all__'

class register_hour_serializer(ModelSerializer):
    class Meta:
        model = Register_new_hour
        fields = '__all__'


class save_bad_info(ModelSerializer):
    class Meta:
        model = Save_bad
        fields = '__all__'

class SaveBadParteSerial(ModelSerializer):
    class Meta:
        model = SaveErrorParte
        fields = '__all__'


class save_config_serializer(ModelSerializer):
    class Meta:
        model = Save_config
        fields = '__all__'

class save_user(ModelSerializer):
    class Meta:
        model = SaveUser
        fields = '__all__'
