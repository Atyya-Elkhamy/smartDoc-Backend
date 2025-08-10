from rest_framework import serializers
from doctor.models import Treatment
from patient.models import Appointment


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = [
            'expected_check_time',
            'status',
            'appointment_date',
            'queue_number',  # prevent manual setting
            'patient',       # hide patient from input
        ]
    def create(self, validated_data):
        patient = self.context['request'].user
        validated_data['patient'] = patient
        return super().create(validated_data)


class ExpectedTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'queue_number', 'expected_check_time']


class TreatmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Treatment
        fields = ['id', 'diagnosis', 'treatment_plan', 'prescribed_medications', 'start_date', 'end_date', 'doctor_name']
