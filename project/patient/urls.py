from django.urls import path
from .views import *

urlpatterns = [
    path('appointments/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('expected-time/<int:appointment_id>/', ExpectedTimeView.as_view(), name='expected-time'),
    path('treatments/<int:appointment_id>/', PatientTreatmentsView.as_view(), name='patient-treatments'),
    path('appointments/update/<int:appointment_id>/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointments/delete/<int:appointment_id>/', AppointmentDeleteView.as_view(), name='appointment-delete'),
    path('appointments/<int:patient_id>/', PatientAppointmentsView.as_view(), name='patient-appointments'),
]
