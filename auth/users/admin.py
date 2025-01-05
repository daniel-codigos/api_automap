from django.contrib import admin

# Register your models here.
from .models import User, show_info,Register_new_hour,Save_config
#Show_infos

admin.site.register(User)
admin.site.register(Save_config)


