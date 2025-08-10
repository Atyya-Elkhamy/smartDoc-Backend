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
        serializer = AppointmentCreateSerializer(
            data=request.data,
            context={'request': request}
        )
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
        appointment = get_object_or_404(
            Appointment,
            id=appointment_id,
            patient=request.user
        )
        treatments = Treatment.objects.filter(patient=request.user)
        if not treatments.exists():
            return Response(
                {"message": "No treatments found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TreatmentSerializer(treatments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PatientAppointmentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, patient_id):
        appointments = Appointment.objects.filter(patient_id=patient_id).order_by('-appointment_date')
        if not appointments.exists():
            return Response(
                {"message": "No appointments found for this patient."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = AppointmentCreateSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AppointmentUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        serializer = AppointmentCreateSerializer(
            appointment,
            data=request.data,
            partial=False, 
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Appointment updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.delete()
        return Response(
            {"message": "Appointment deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
