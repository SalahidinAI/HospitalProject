from rest_framework import permissions


class CheckDoctorOrPatientAppointEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'doctor':
            return obj.doctor == request.user
        return obj.patient == request.user


class CheckProfileEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id


class CheckDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'doctor'


class CheckPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'patient'
