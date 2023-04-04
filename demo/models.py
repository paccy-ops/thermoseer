from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='normal')


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active='True')


class ScannerTemperature(models.Model):
    scanner_id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    dept = models.CharField(max_length=250)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_user = ActiveManager()

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('-created',)


class Temperature(models.Model):
    STATUS_CHOICES = (("high", "High"), ("normal", "Normal"))
    scanner = models.ForeignKey(ScannerTemperature, on_delete=models.CASCADE, related_name="scanners")
    temp = models.CharField(max_length=50)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="normal")

    objects = models.Manager()
    normal = PublishManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.scanner.name
