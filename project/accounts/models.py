from django.db import models
from django.contrib.auth.models import AbstractUser


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

    def assign_type_for_superuser(self):
        if self.is_superuser:
            self.type = self.UserType.DOCTOR

    def save(self, *args, **kwargs):
        self.assign_type_for_superuser()
        super().save(*args, **kwargs)
