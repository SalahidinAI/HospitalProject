from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator
from rest_framework.exceptions import ValidationError
from datetime import time, timedelta, datetime

ROLE_CHOICES = (
    ('doctor', 'doctor'),
    ('patient', 'patient'),
)


class UserProfile(AbstractUser):
    contact = PhoneNumberField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='user_picture/', null=True, blank=True)
    GENDER_CHOICES = (
        ('mail', 'mail'),
        ('female', 'female'),
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=8, null=True, blank=True)


class Specialty(models.Model):
    specialty_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.specialty_name


class Department(models.Model):
    department_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.department_name


class Doctor(UserProfile):
    specialty = models.ManyToManyField(Specialty, related_name='specialty_doctors')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='department_doctors', null=True, blank=True)
    WORKING_DAYS_CHOICES = (
        ('ПН', 'ПН'),
        ('ВТ', 'ВТ'),
        ('СР', 'СР'),
        ('ЧТ', 'ЧТ'),
        ('ПТ', 'ПТ'),
        ('СБ', 'СБ'),
    )
    working_days = MultiSelectField(choices=WORKING_DAYS_CHOICES, max_length=18)
    experience = models.PositiveSmallIntegerField(validators=[MaxValueValidator(35)], null=True, blank=True)
    shift_start = models.TimeField(null=True, blank=True)
    shift_end = models.TimeField(null=True, blank=True)
    service_price = models.PositiveSmallIntegerField(null=True, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=8, default='doctor')

    def __str__(self):
        return self.first_name

    def get_avg_rating(self):
        feedbacks = self.doctor_feedbacks.all()
        if feedbacks.exists():
            stars = [i.rating for i in feedbacks if i.rating]
            return round(sum(stars) / len(stars), 1)
        return 0

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def clean(self):
        min_shift_start = time(8, 0)

        start_dt = datetime.combine(datetime.today(), self.shift_start)
        end_dt = datetime.combine(datetime.today(), self.shift_end)

        if self.shift_start < min_shift_start:
            raise ValidationError({"shift_start": "Shift cannot start earlier than 08:00 AM."})

        if (end_dt - start_dt) < timedelta(minutes=30):
            raise ValidationError({"shift_end": "Shift duration must be at least 4 hours."})


class Patient(UserProfile):
    BLOOD_CHOICES = (
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('III+', 'III+'),
    )
    blood_group = models.CharField(choices=BLOOD_CHOICES, max_length=4, null=True, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=8, default='patient')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('canceled', 'canceled'),
        ('planned', 'planned'),
        ('at appointment', 'at appointment'),
        ('completed', 'completed'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=16, default='planned')
    date_time = models.DateTimeField()

    def __str__(self):
        return f'patient: {self.patient}, doctor:{self.doctor}'

    class Meta:
        ordering = ['date_time']


class Record(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=128)
    treatment = models.CharField(max_length=256)
    prescribed_medication = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.doctor} > {self.patient}'


class Feedback(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_feedbacks')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 10)], null=True, blank=True)
    comment = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'patient: {self.patient} > doctor: {self.doctor}'

    class Meta:
        unique_together = ('patient', 'doctor')

    def clean(self):
        super().clean()
        if not self.rating and not self.comment:
            raise ValidationError('rating or comment dont leave empty')


class Chat(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def clean(self):
        super().clean()

        if not self.doctor and not self.patient:
            raise ValidationError('Choose doctor or patient at least')


class Message(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    video = models.FileField(upload_to='chat_videos/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        if not self.text and not self.image and not self.video:
            raise ValidationError('Error, sent text, image or video!')

        if not self.doctor and not self.patient:
            raise ValidationError('Choose doctor or patient at least')


