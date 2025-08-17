from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date


class User(AbstractUser):
    class UserType(models.TextChoices):
        PATIENT = 'patient', 'Patient'
        DOCTOR = 'doctor', 'Doctor'
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female')],
        null=True, blank=True
    )
    age = models.PositiveIntegerField(null=True, blank=True, editable=False)
    address = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='users/', null=True, blank=True)
    type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.PATIENT
    )

    class Meta:
        db_table = 'accounts'
