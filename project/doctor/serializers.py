from rest_framework import serializers
from patient.models import Appointment
from .models import Treatment


class TreatmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['diagnosis', 'treatment_plan', 'prescribed_medications', 'start_date', 'end_date', 'follow_up_date', 'notes']

    def create(self, validated_data):
        request = self.context['request']
        appointment = self.context['appointment']
        treatment = Treatment.objects.create(
            patient=appointment.patient,
            doctor=request.user,
            **validated_data
        )
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
        fields = ['id', 'patient_name', 'queue_number', 'expected_check_time', 'status']
