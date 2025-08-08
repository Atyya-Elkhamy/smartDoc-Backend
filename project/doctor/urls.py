from django.urls import path
from .views import CreateTreatmentView, ChangeAppointmentStatusView, TodayPatientsListView, PatientHistoryView

urlpatterns = [
    path('appointments/<int:appointment_id>/treatment/', CreateTreatmentView.as_view(), name='create-treatment'),
    path('appointments/<int:appointment_id>/status/', ChangeAppointmentStatusView.as_view(), name='change-appointment-status'),
    path('patients/today/', TodayPatientsListView.as_view(), name='today-patients'),
    path('patients/<int:patient_id>/history/', PatientHistoryView.as_view(), name='patient-history'),
]
