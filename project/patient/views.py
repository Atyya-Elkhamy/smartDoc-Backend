from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from patient.models import Appointment
from django.utils import timezone
from .serializers import *


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



class PatientTreatmentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, appointment_id):
        appointment = get_object_or_404(
            Appointment,
            id=appointment_id,
            patient=request.user
        )
        if not appointment.treatment:
            return Response(
                {"message": "No treatment found for this appointment."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TreatmentSerializer(appointment.treatment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PatientAppointmentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.filter(
            patient=request.user
        ).order_by('-appointment_date')

        serializer = AppointmentDetailSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AppointmentUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        serializer = AppointmentCreateSerializer(
            appointment,
            data=request.data,
            partial=True, 
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
class TodayAppointmentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.type != 'patient':
            return Response({"detail": "Only patients can view this data."}, status=403)
        today = timezone.localdate()
        appointments = Appointment.objects.filter(
            patient=request.user,
            appointment_date=today,
            status=Appointment.Status.WAITING
        )
        serializer = AppointmentDetailSerializer(appointments, many=True)
        return Response(serializer.data)
    
class AppointmentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, appointment_id):
        appointment = get_object_or_404(
            Appointment,
            id=appointment_id,
            patient=request.user
        )
        serializer = AppointmentDetailSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AppointmentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentAllSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)