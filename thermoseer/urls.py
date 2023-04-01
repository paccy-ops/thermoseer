from django.urls import path
from . import views

app_name = 'thermoseer'
urlpatterns = [
    path('', views.home, name="home"),
    path('scanned', views.scanned_record, name="scanned_record"),
    path('login', views.loginuser, name="loginuser"),
    path('signup', views.signupuser, name="signupuser"),
    path('logout', views.logoutuser, name="logoutuser"),
    path('create/temperature', views.create_temperature, name="create_temperature"),
    path('thermoser/list', views.temperature_list, name='temperature_list'),
    path("thermoser/temperature/detail/<int:temp_pk>", views.temperature_detail, name="temperature_detail")
]
