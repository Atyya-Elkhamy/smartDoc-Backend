from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date


class User(AbstractUser):
    class UserType(models.TextChoices):
        PATIENT = 'patient', 'Patient'
        DOCTOR = 'doctor', 'Doctor'
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female')],
        null=True, blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='users/', null=True, blank=True)
    type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.PATIENT
    )
    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        return (
            today.year - self.date_of_birth.year -
            ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        )
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.type = self.UserType.DOCTOR
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'accounts'
