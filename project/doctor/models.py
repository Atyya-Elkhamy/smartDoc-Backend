from django.db import models
from django.conf import settings


class Treatment(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'type': 'patient'},
        related_name='treatments'
    )
    diagnosis = models.TextField()
    treatment_plan = models.TextField() 
    prescribed_medications = models.TextField(blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'treatments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Treatment for {self.patient.get_full_name()}"
