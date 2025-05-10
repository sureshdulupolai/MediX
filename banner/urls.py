from django.urls import path
from . import views

urlpatterns = [
    path('banner-upload/', views.bannerPage, name='banner'),
    path('banner-payment/<ObjId>/<Usernames>/', views.bannerPayment, name='bannerPayment'),
    path('on_approve/', views.On_Approve_View, name = 'on_approve'),
    path('payment_sucesss/<ObjId>/<Usernames>/', views.Payment_Success_View, name='payment_success'),
]