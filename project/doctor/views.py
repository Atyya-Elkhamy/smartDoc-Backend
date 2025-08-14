from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from patient.models import Appointment
from .models import Treatment
from .serializers import *
from time import timezone

class CreateTreatmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        serializer = TreatmentCreateSerializer(
            data=request.data,
            context={
                "request": request,
                "appointment": appointment
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Treatment added successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeAppointmentStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        serializer = AppointmentStatusSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Status updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodayPatientsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.utils.timezone import now
        today = now().date()
        appointments = Appointment.objects.filter(
            appointment_date=today, status=Appointment.Status.WAITING
        ).order_by('queue_number')
        serializer = PatientListSerializer(appointments, many=True)
        return Response(serializer.data)


class PatientHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, patient_id):
        treatments = Treatment.objects.filter(patient_id=patient_id).order_by('-start_date')
        if not treatments.exists():
            return Response({"message": "No history found for this patient"}, status=status.HTTP_404_NOT_FOUND)
        data = [
            {
                "diagnosis": t.diagnosis,
                "treatment_plan": t.treatment_plan,
                "prescribed_medications": t.prescribed_medications,
                "start_date": t.start_date,
                "end_date": t.end_date,
                "follow_up_date": t.follow_up_date,
                "notes": t.notes,
            }
            for t in treatments
        ]
        return Response(data)
