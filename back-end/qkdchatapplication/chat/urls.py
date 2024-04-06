from django.urls import path
from . import views

urlpatterns = [
    path('recieve/', views.MsgHandling.as_view(), name="msghandle"),
    path('encryption/', views.MsgEncryption.as_view(), name="msgencrypt")
] 