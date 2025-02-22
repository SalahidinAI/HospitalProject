from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class DoctorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = Doctor.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class PatientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = Patient.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class SpecialtyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'specialty_name']


class SpecialtyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['specialty_name']


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']


class DepartmentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name']


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['username', 'first_name', 'last_name', 'password', 'profile_picture', 'email',
                  'contact', 'gender', 'working_days', 'experience', 'shift_start', 'shift_end',
                  'service_price', 'role', 'department', 'specialty']


class DoctorListSerializer(serializers.ModelSerializer):
    specialty = SpecialtyNameSerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'profile_picture', 'first_name', 'last_name', 'gender', 'specialty']


class PatientSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['profile_picture', 'username']


class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'profile_picture', 'first_name', 'last_name', 'contact', 'gender', 'blood_group']


class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['profile_picture', 'username', 'first_name', 'last_name', 'email', 'password', 'contact', 'gender', 'blood_group', 'role']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentListSerializer(serializers.ModelSerializer):
    patient = PatientListSerializer()
    doctor = DoctorListSerializer()
    date_time = serializers.DateTimeField(format='%d %B %Y %H:%M')

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'status', 'date_time']


class AppointmentEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['status']


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'


class RecordListSerializer(serializers.ModelSerializer):
    patient = PatientListSerializer()
    doctor = DoctorListSerializer()
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Record
        fields = ['id', 'patient', 'doctor', 'diagnosis', 'treatment', 'prescribed_medication', 'created_at']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class FeedbackListSerializer(serializers.ModelSerializer):
    patient = PatientSimpleSerializer()
    created_at = serializers.DateTimeField(format='%d %B %Y %H:%M')

    class Meta:
        model = Feedback
        fields = ['patient', 'rating', 'comment', 'created_at']


class SpecialtyDetailSerializer(serializers.ModelSerializer):
    specialty_doctors = DoctorListSerializer(many=True, read_only=True)

    class Meta:
        model = Specialty
        fields = ['id', 'specialty_name', 'specialty_doctors']


class DepartmentDetailSerializer(serializers.ModelSerializer):
    department_doctors = DoctorListSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'department_name', 'department_doctors']


class DoctorInfoSerializer(serializers.ModelSerializer):
    experience = serializers.SerializerMethodField()
    shift_start = serializers.TimeField(format='%H:%M')
    shift_end = serializers.TimeField(format='%H:%M')
    department = DepartmentNameSerializer()
    specialty = SpecialtyNameSerializer(many=True, read_only=True)
    doctor_feedbacks = FeedbackListSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id', 'profile_picture', 'first_name', 'last_name', 'email',
                  'contact', 'gender', 'working_days', 'experience', 'shift_start', 'shift_end',
                  'service_price', 'department', 'specialty', 'avg_rating', 'doctor_feedbacks']

    def get_experience(self, obj):
        if obj.experience == 1:
            return f'{obj.experience} year'
        return f'{obj.experience} years'

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()
