from django.urls import path
from .views import *

urlpatterns = [
    path('register/doctor/', DoctorRegisterView.as_view(), name='register_doctor'),
    path('register/patient/', PatientRegisterView.as_view(), name='register_patient'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('specialty/', SpecialtyListAPIView.as_view(), name='specialty_list'),
    path('specialty/<int:pk>/', SpecialtyDetailAPIView.as_view(), name='specialty_detail'),

    path('department/', DepartmentListAPIView.as_view(), name='department_list'),
    path('department/<int:pk>/', DepartmentDetailAPIView.as_view(), name='department_detail'),

    path('doctor/', DoctorListAPIView.as_view(), name='doctor_list'),
    path('doctor/<int:pk>/', DoctorDetailAPIView.as_view(), name='doctor_detail'),
    path('doctor_list/', DoctorOwnListAPIView.as_view(), name='doctor_own_list'),
    path('doctor_list/<int:pk>/', DoctorEditAPIView.as_view(), name='doctor_own_edit'),

    path('patient/', PatientListAPIView.as_view(), name='patient_list'),
    path('patient/<int:pk>/', PatientDetailAPIView.as_view(), name='patient_edit'),

    path('appointment/create/', AppointmentCreateAPIView.as_view(), name='appointment_create'),
    path('appointment/', AppointmentListAPIView.as_view(), name='appointment_list'),
    path('appointment/<int:pk>/', AppointmentEditAPIView.as_view(), name='appointment_detail'),

    path('record/', RecordListAPIView.as_view(), name='record_list'),
    path('record/create/', RecordCreateAPIView.as_view(), name='record_create'),

    path('feedback/create/', FeedbackCreateAPIView.as_view(), name='feedback_create'),
]
