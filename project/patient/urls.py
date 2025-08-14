from django.urls import path
from .views import *

urlpatterns = [
    path('appointments/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('treatments/<int:appointment_id>/', PatientTreatmentsView.as_view(), name='patient-treatments'),
    path('appointments/update/<int:appointment_id>/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointments/delete/<int:appointment_id>/', AppointmentDeleteView.as_view(), name='appointment-delete'),
    path('appointments/all/', PatientAppointmentsView.as_view(), name='patient-appointments'),
    path('appointments/today/', TodayAppointmentsView.as_view(), name='today-appointments'),
    path('appointments/<int:appointment_id>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('show-all-appointments/', AppointmentListView.as_view(), name='appointment-list'),
]
