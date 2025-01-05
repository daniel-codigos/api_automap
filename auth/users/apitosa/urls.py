from django.urls import path
from . import views


urlpatterns = [
    path('start', views.get_in),
    path('fin', views.get_off),
    path('show_hours',views.get_in_hour),
    path('register_new_hour',views.hour_view_register),
    path('delete_hour/<id>',views.delete_hourss.as_view()),
    path('savebad',views.saveBad.as_view()),
    path('removebad',views.removeBad.as_view()),
    path('piensabad', views.piensaBad.as_view()),
    path('getConfig',views.getConfig.as_view()),
    path('saveConfig',views.saveConfig.as_view()),
    path('saveUser',views.saveUser.as_view())
    #path('show', views.get_Info)
]


