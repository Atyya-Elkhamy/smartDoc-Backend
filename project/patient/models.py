from django.db import models
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from doctor.models import Treatment

class Appointment(models.Model):
    class Status(models.TextChoices):
        WAITING = 'waiting', 'Waiting'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'type': 'patient'},
        related_name="appointments"
    )
    treatment = models.ForeignKey(Treatment,on_delete=models.SET_NULL,null=True,blank=True,related_name="appointments")
    visit_reason = models.TextField(help_text="Main reason for visit")
    symptoms = models.TextField(help_text="Symptoms described by patient")
    diseases = models.TextField(blank=True, null=True, help_text="Diagnosed diseases")
    treatments = models.TextField(blank=True, null=True, help_text="Treatment plan")
    symptom_start_date = models.DateField(blank=True, null=True)

    has_visited_before = models.BooleanField(default=False)
    same_reason_as_before = models.BooleanField(default=False)
    has_allergy_or_sensitivity = models.BooleanField(default=False)
    allergy_details = models.TextField(blank=True, null=True)

    queue_number = models.PositiveIntegerField(
        editable=False,
        help_text="Patient order in today's queue"
    )
    expected_check_time = models.TimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WAITING
    )

    appointment_date = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def calculate_expected_time(self, avg_minutes_per_patient=15):
        now = timezone.now()
        patients_ahead = Appointment.objects.filter(
            appointment_date=self.appointment_date,
            status=Appointment.Status.WAITING,
            queue_number__lt=self.queue_number
        ).count()
        wait_time = timedelta(minutes=patients_ahead * avg_minutes_per_patient)
        return (now + wait_time).time()

    def save(self, *args, **kwargs):
        if not self.queue_number:
            last_appt = Appointment.objects.filter(
                appointment_date=self.appointment_date
            ).order_by('-queue_number').first()
            self.queue_number = last_appt.queue_number + 1 if last_appt else 1
        if self.status == Appointment.Status.WAITING:
            self.expected_check_time = self.calculate_expected_time()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'appointments'
        ordering = ['appointment_date', 'queue_number']
        unique_together = ('appointment_date', 'queue_number')

    def __str__(self):
        return f"Appointment #{self.queue_number} - {self.patient.get_full_name()}"
