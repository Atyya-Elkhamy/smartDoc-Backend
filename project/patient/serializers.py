from rest_framework import serializers
from doctor.models import Treatment
from patient.models import Appointment


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'visit_reason',
            'symptoms',
            'diseases',
            'treatments',
            'symptom_start_date',
            'has_visited_before',
            'same_reason_as_before',
            'has_allergy_or_sensitivity',
            'allergy_details',
            'queue_number'
        ]
        read_only_fields = ['expected_check_time', 'status', 'appointment_date']

    def create(self, validated_data):
        request = self.context['request']
        patient = request.user
        # Assign default doctor or select logic later
        doctor = validated_data.get('doctor')
        if not doctor:
            raise serializers.ValidationError("Doctor is required.")

        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            **validated_data
        )
        return appointment


class ExpectedTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'queue_number', 'expected_check_time']


class TreatmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)

    class Meta:
        model = Treatment
        fields = ['id', 'diagnosis', 'treatment_plan', 'prescribed_medications', 'start_date', 'end_date', 'doctor_name']
