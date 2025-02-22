from django.db.models import Q
from .models import *
from .serializers import *
from rest_framework import viewsets, generics
from .permissions import *
from .paginations import TwoObject
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import DoctorFilter
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class DoctorRegisterView(generics.CreateAPIView):
    serializer_class = DoctorRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PatientRegisterView(generics.CreateAPIView):
    serializer_class = PatientRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SpecialtyListAPIView(generics.ListAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtyListSerializer
    pagination_class = TwoObject


class SpecialtyDetailAPIView(generics.RetrieveAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtyDetailSerializer


class DepartmentListAPIView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentListSerializer
    pagination_class = TwoObject


class DepartmentDetailAPIView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentDetailSerializer


class DoctorListAPIView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorListSerializer
    pagination_class = TwoObject
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DoctorFilter
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['first_name', 'experience']


class DoctorDetailAPIView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorInfoSerializer


class DoctorOwnListAPIView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorInfoSerializer

    def get_queryset(self):
        return Doctor.objects.filter(id=self.request.user.id)


class DoctorEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [CheckProfileEdit]


class PatientListAPIView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientListSerializer

    def get_queryset(self):
        return Patient.objects.filter(id=self.request.user.id)


class PatientDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientDetailSerializer
    permission_classes = [CheckProfileEdit]


class AppointmentCreateAPIView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [CheckPatient]


class AppointmentListAPIView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentListSerializer
    pagination_class = TwoObject

    def get_queryset(self):
        return Appointment.objects.filter(
            Q(patient=self.request.user) |
            Q(doctor=self.request.user)
        )


class AppointmentEditAPIView(generics.RetrieveUpdateAPIView):
    queryset = Appointment.objects.all()
    permission_classes = [CheckDoctorOrPatientAppointEdit]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AppointmentEditSerializer
        return AppointmentListSerializer


class RecordCreateAPIView(generics.CreateAPIView):
    serializer_class = RecordSerializer
    permission_classes = [CheckDoctor]


class RecordListAPIView(generics.ListAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordListSerializer

    def get_queryset(self):
        return Record.objects.filter(
            Q(patient=self.request.user) |
            Q(doctor=self.request.user)
        )


class FeedbackCreateAPIView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [CheckPatient]
