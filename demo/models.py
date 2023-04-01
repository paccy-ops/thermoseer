from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy, reverse
from django.utils import timezone


# Create your models here.
class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='normal')


class Temperature(models.Model):
    STATUS_CHOICES = (("high", "High"), ("normal", "Normal"))
    name = models.CharField(max_length=250)
    scanner_id = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    temp = models.CharField(max_length=50)
    dept = models.CharField(max_length=250)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="normal")

    objects = models.Manager()
    normal = PublishManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name