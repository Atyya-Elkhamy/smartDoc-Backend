from rest_framework import serializers
from patient.models import Appointment
from .models import Treatment


class TreatmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = [
            "diagnosis", "treatment_plan", "prescribed_medications",
            "start_date", "end_date", "follow_up_date", "notes"
        ]
        read_only_fields = [] 

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError({
                "end_date": "End date must be greater than start date."
            })
        return attrs

    def create(self, validated_data):
        appointment = self.context["appointment"]
        treatment = Treatment.objects.create(
            patient=appointment.patient,
            **validated_data
        )
        appointment.treatment = treatment
        appointment.status = Appointment.Status.COMPLETED
        appointment.save()
        return treatment

class AppointmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['status']


class PatientListSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    queue_number = serializers.IntegerField(read_only=True)
    expected_check_time = serializers.TimeField(read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
