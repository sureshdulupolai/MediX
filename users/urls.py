from django.urls import path, include
from . import views

urlpatterns = [
    path('user-signup/', views.SignupPage, name='signup'),
    path('user-login/', views.Login_in, name='login'),
    path('user-logout-confirm/', views.logout_ask, name='logout_confirm'),
    path('user-logout/', views.Logout_in, name='logout'),
    path('user-profile/', views.ProfilePage, name='profile'),
    path('user-profile/<str:profile_data>/', views.profileData,name="profile_link"),
    path('user-edit-profile/', views.ProfileEdit, name='edit_profile'),
    path('check-connection/<int:item_id>/<str:data>/', views.checkConnection, name='check_connection'),
    # path('check-connection/<int:st_id>/', views.checkConnectionShorts, name='check_connection'),
]
