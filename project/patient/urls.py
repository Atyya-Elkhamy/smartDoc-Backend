from django.urls import path
from .views import AppointmentCreateView, ExpectedTimeView, PatientTreatmentsView

urlpatterns = [
    path('appointments/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointments/<int:appointment_id>/expected-time/', ExpectedTimeView.as_view(), name='expected-time'),
    path('appointments/<int:appointment_id>/treatments/', PatientTreatmentsView.as_view(), name='patient-treatments'),
]
