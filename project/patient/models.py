from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Appointment(models.Model):
    class Status(models.TextChoices):
        WAITING = 'waiting', 'Waiting'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'type': 'patient'},
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'type': 'doctor'},
        related_name='doctor_appointments'
    )

    visit_reason = models.TextField(help_text="Main reason for visit")
    symptoms = models.TextField(help_text="Symptoms described by patient")
    diseases = models.TextField(blank=True, null=True, help_text="Diagnosed diseases")
    treatments = models.TextField(blank=True, null=True, help_text="Treatment plan")
    symptom_start_date = models.DateField(blank=True, null=True)

    has_visited_before = models.BooleanField(default=False)
    same_reason_as_before = models.BooleanField(default=False)
    has_allergy_or_sensitivity = models.BooleanField(default=False)
    allergy_details = models.TextField(blank=True, null=True)

    queue_number = models.PositiveIntegerField(help_text="Patient order in today's queue")
    expected_check_time = models.TimeField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WAITING
    )

    appointment_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_expected_time(self, avg_minutes_per_patient=15):
        """
        Calculates expected check time based on queue number and average time per patient.
        """
        start_time = timezone.datetime.combine(
            self.appointment_date,
            timezone.datetime.strptime("09:00", "%H:%M").time()  # Clinic start time
        )
        return (start_time + timedelta(minutes=(self.queue_number - 1) * avg_minutes_per_patient)).time()

    def save(self, *args, **kwargs):
        # Auto-set expected_check_time if not provided
        if not self.expected_check_time and self.queue_number:
            self.expected_check_time = self.calculate_expected_time()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'appointments'
        ordering = ['appointment_date', 'queue_number']

    def __str__(self):
        return f"Appointment {self.queue_number} - {self.patient.get_full_name()} with Dr. {self.doctor.get_full_name()}"
