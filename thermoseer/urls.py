from django.urls import path
from . import views

app_name = 'thermoseer'
urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.loginuser, name="loginuser"),
    path('logout', views.logoutuser, name="logoutuser"),
    path('signup', views.signupuser, name="signupuser"),
    path('create/scanner', views.addId, name="add_id"),
    path('create/temperature', views.create_temperature, name="create_temperature"),
    path("thermoser/users", views.users_list, name="users_list"),
    path('thermoser/list', views.temperature_list, name='temperature_list'),
    path('thermoser/details', views.temperature_users_details, name='temperature_users_details'),
    path("thermoser/users/<int:temp_pk>", views.user_scanner_detail, name="user_scanner_detail"),
    path("thermoser/details/<int:temp_pk>", views.temperature_detail, name="temperature_detail"),


]
