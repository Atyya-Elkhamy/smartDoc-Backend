from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from patient.models import Appointment
from doctor.models import Treatment
from .serializers import AppointmentCreateSerializer, ExpectedTimeSerializer, TreatmentSerializer


class AppointmentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AppointmentCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            appointment = serializer.save()
            return Response({
                "message": "Appointment created successfully",
                "data": ExpectedTimeSerializer(appointment).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpectedTimeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
        serializer = ExpectedTimeSerializer(appointment)
        return Response(serializer.data)


class PatientTreatmentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
        treatments = Treatment.objects.filter(patient=request.user, doctor=appointment.doctor)
        if not treatments.exists():
            return Response({"message": "No treatments found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TreatmentSerializer(treatments, many=True)
        return Response(serializer.data)
