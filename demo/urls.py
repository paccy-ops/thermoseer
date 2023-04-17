from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("post", views.PostViewSet, basename="post")

urlpatterns = [
    path("detail", views.detail, name="detail"),
    path("create", views.createTemperature, name="create"),
    path("view/data", views.view, name="view")
]

urlpatterns += router.urls
