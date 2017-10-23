from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.modeladmin_mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin)
from edc_pharma.forms import PrescriptionForm
from edc_pharma.models import DispenseAppointment, Prescription, WorkList

from django.contrib import admin

from .admin_site import edc_pharma_admin
from .forms import DispenseAppointmentForm, WorklistForm


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin):
    pass


@admin.register(DispenseAppointment, site=edc_pharma_admin)
class DispenseAppointmentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = DispenseAppointmentForm


@admin.register(WorkList, site=edc_pharma_admin)
class WorkListAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = WorklistForm


@admin.register(Prescription, site=edc_pharma_admin)
class PrescriptionAdmin(ModelAdminMixin, admin.ModelAdmin):

    fieldsets = (
        ('Patient Summary', {
            'fields': (
                'is_consented',
                'subject_identifier',
                'arm')}),
        ('Medication', {
            'fields': (
                'category',
                'medication_description',)}),
        ('Result', {
            'fields': (
                'duration',
                'result',
                'description',
                'recommanded_result',
            )}),)

    form = PrescriptionForm
