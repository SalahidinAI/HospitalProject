from .models import Specialty, Department
from modeltranslation.translator import TranslationOptions, register


@register(Specialty)
class SpecialtyTranslationOptions(TranslationOptions):
    fields = ('specialty_name',)


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('department_name',)
