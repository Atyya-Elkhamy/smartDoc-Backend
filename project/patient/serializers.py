from rest_framework import serializers
from doctor.models import Treatment
from patient.models import Appointment

class AppointmentCreateSerializer(serializers.ModelSerializer):
    treatment = serializers.PrimaryKeyRelatedField(
        queryset=Treatment.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = [
            'expected_check_time',
            'status',
            'appointment_date',
            'queue_number',
            'patient',
        ]

    def create(self, validated_data):
        patient = self.context['request'].user
        validated_data['patient'] = patient
        return super().create(validated_data)

class ExpectedTimeSerializer(serializers.ModelSerializer):
    expected_check_time = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'queue_number', 'expected_check_time']

    def get_expected_check_time(self, obj):
        expected_time = self.context.get("expected_time")
        return expected_time.strftime("%H:%M") if expected_time else None


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = [
            'id',
            'diagnosis',
            'treatment_plan',
            'prescribed_medications',
            'start_date',
            'end_date',
        ]


class AppointmentDetailSerializer(serializers.ModelSerializer):
    treatment = TreatmentSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        exclude = ['treatment']

