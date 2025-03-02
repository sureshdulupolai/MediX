from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.Login_in, name='login'),
    path('logout-confirm/', views.logout_ask, name='logout_confirm'),
    path('logout/', views.Logout_in, name='logout'),
    path('profile/', views.ProfilePage, name='profile'),
]
