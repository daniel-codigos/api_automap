from django.contrib import admin
from django.urls import path, include
from .views import RegisterView, LoginView, UserView,LogoutView,RefreshView, MyTokenObtainPairView,get_verify
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView
#from auth.apitosa import views


#minuto 31

urlpatterns = [
    #path('register',RegisterView.as_view()),
    #path('login',LoginView.as_view()),
    path('login',MyTokenObtainPairView.as_view(), name='token_access'),
    path('user',UserView.as_view()),
    path('user2/',include('users.apitosa.urls')),
    path('logout',LogoutView.as_view()),
    path('refresh',TokenRefreshView.as_view(), name='token_refresh'),
    path('verify', get_verify),
    #path('refresh',RefreshView.as_view()),
]
