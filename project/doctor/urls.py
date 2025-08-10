from django.urls import path
from .views import CreateTreatmentView, ChangeAppointmentStatusView, TodayPatientsListView, PatientHistoryView

urlpatterns = [
    path('treatment/<int:appointment_id>/', CreateTreatmentView.as_view(), name='create-treatment'),
    path('status/<int:appointment_id>/', ChangeAppointmentStatusView.as_view(), name='change-appointment-status'),
    path('today/', TodayPatientsListView.as_view(), name='today-patients'),
    path('history/<int:patient_id>/', PatientHistoryView.as_view(), name='patient-history'),
]
