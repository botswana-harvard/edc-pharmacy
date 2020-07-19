from datetime import date
from dateutil.relativedelta import relativedelta

from django.apps import apps as django_apps
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords

from edc_base.model.models import BaseUuidModel
from edc_base.utils import formatted_age
from edc_constants.choices import GENDER

from .choices import DISPENSE_TYPES
from .constants import TABLET, SYRUP, IM, IV, SUPPOSITORY, SOLUTION, CAPSULE

app_config = django_apps.get_app_config('edc_pharma')


class Protocol(BaseUuidModel):

    number = models.CharField(max_length=30)

    name = models.CharField(max_length=200, unique=True)

    objects = models.Manager()

    history = HistoricalRecords()

    def __str__(self):
        return self.number

    class Meta:
        app_label = 'edc_pharma'


class Site(BaseUuidModel):

    protocol = models.ForeignKey(Protocol)

    site_code = models.CharField(
        max_length=20,
        validators=[RegexValidator('[\d]+', 'Invalid format.')])

    telephone_number = models.CharField(
        max_length=7,
        validators=[RegexValidator('^[2-8]{1}[0-9]{6}$', 'Invalid format.')])

    objects = models.Manager()

    history = HistoricalRecords()

    def __str__(self):
        return '{}, Protocol: {}'.format(self.site_code, self.protocol)

    class Meta:
        app_label = 'edc_pharma'


class Medication(BaseUuidModel):

    name = models.CharField(max_length=200)

    protocol = models.ForeignKey(Protocol)

    storage_instructions = models.TextField(max_length=200)

    objects = models.Manager()

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'edc_pharma'


def validate_dob(value):
    if value:
        age_in_years = relativedelta(date.today(), value).years
        if age_in_years <= 18:
            raise ValidationError(
                ('Mininum age is 18 years, got %(age_in_years)s.'),
                params={'age_in_years': age_in_years},
            )
        if age_in_years >= 65:
            raise ValidationError(
                ('Maximum age is 65, got %(age_in_years)s.'),
                params={'age_in_years': age_in_years},
            )


class Patient(BaseUuidModel):

    subject_identifier = models.CharField(max_length=20, unique=True)

    initials = models.CharField(
        max_length=5,
        validators=[RegexValidator(r'^[A-Z]{2,3}$', message='Use CAPS, 2-3 letters')],
        help_text='Format is AA or AAA')

    gender = models.CharField(
        max_length=10,
        choices=GENDER)

    dob = models.DateField(
        blank=True,
        null=True,
        validators=[validate_dob])

    sid = models.CharField(
        max_length=20,
        validators=[RegexValidator('[\d]+', 'Invalid format.')],
    )

    consent_date = models.DateTimeField(default=date.today, editable=False)

    site = models.ForeignKey(Site)

    objects = models.Manager()

    history = HistoricalRecords()

    def __str__(self):
        return '{}, ({}), Site {}'.format(self.subject_identifier, self.initials, self.site.site_code)

    @property
    def born(self):
        return self.dob.strftime('%Y-%m-%d')

    @property
    def age(self):
        return formatted_age(self.dob, date.today())

    class Meta:
        app_label = 'edc_pharma'


class Dispense(BaseUuidModel):

    date_hierarchy = '-prepared_datetime'

    patient = models.ForeignKey(Patient)

    medication = models.ForeignKey(Medication)

    dispense_type = models.CharField(
        max_length=15,
        choices=DISPENSE_TYPES,
        default=TABLET
    )

    infusion_number = models.IntegerField(
        blank=True,
        null=True,
        help_text="Only required if dispense type IV or IM is chosen")

    number_of_tablets = models.IntegerField(
        blank=True,
        null=True,
        help_text="Only required if dispense type TABLET, CAPSULES, SUPPOSITORIES is chosen")

    dose = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Only required if dispense type SYRUP or SOLUTION is chosen")

    times_per_day = models.IntegerField(
        blank=True,
        null=True,
        help_text="Only required if dispense type TABLET, CAPSULES, SUPPOSITORIES, SYRUP is chosen")

    total_number_of_tablets = models.IntegerField(
        blank=True,
        null=True,
        help_text="Only required if dispense type TABLET or SUPPOSITORY  is chosen")

    total_volume = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Only required if dispense type is SYRUP, IM, IV is chosen")

    concentration = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        help_text="Only required if dispense type IV, IM, CAPSULES, SOLUTION, SUPPOSITORIES, TABLET is chosen")

    duration = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Only required if dispense type IV or IM is chosen")

    weight = models.DecimalField(
        verbose_name='Weight in kg',
        decimal_places=2,
        max_digits=5,
        blank=True,
        null=True,
        help_text="Only required if IV or IM is chosen")

    prepared_datetime = models.DateTimeField(default=timezone.now)

    prepared_date = models.DateTimeField(default=date.today, editable=False)

    objects = models.Manager()

    history = HistoricalRecords()

    def __str__(self):
        return str(self.patient)

    @property
    def refill_date(self):
        refill_date = None
        if self.dispense_type == TABLET:
            days = self.total_number_of_tablets / (self.times_per_day * self.number_of_tablets)
            refill_date = date.today() + relativedelta(days=days + 1)
        return refill_date

    @property
    def prescription(self):
        if self.dispense_type == TABLET:
            if self.number_of_tablets > 1:
                prescription = (
                    '{medication} {number_of_tablets} tablets {times_per_day} times per day '
                    '({total_number_of_tablets} tablets)'.format(
                        medication=self.medication.name,
                        number_of_tablets=self.number_of_tablets,
                        times_per_day=self.times_per_day,
                        total_number_of_tablets=self.total_number_of_tablets))
            else:
                prescription = (
                    '{medication} 1 tablet {times_per_day} time per day '
                    '({total_number_of_tablets} tablets)'.format(
                        medication=self.medication.name,
                        times_per_day=self.times_per_day,
                        total_number_of_tablets=self.total_number_of_tablets))
        if self.dispense_type == SYRUP:
            prescription = (
                '{medication} {dose} dose {times_per_day} times a day '
                '({total_volume})'.format(
                    medication=self.medication.name,
                    dose=self.dose,
                    times_per_day=self.times_per_day,
                    total_volume=self.total_volume))
        if self.dispense_type == SOLUTION:
            prescription = (
                '{medication} {dose} dose {times_per_day} times a day '
                '({total_volume})'.format(
                    medication=self.medication.name,
                    dose=self.dose,
                    times_per_day=self.times_per_day,
                    total_volume=self.total_volume))
        if self.dispense_type == IV:
            prescription = (
                '{medication} Intravenous {concentration} {duration} '
                '({total_volume})'.format(
                    medication=self.medication.name,
                    duration=self.duration,
                    concentration=self.concentration,
                    times_per_day=self.times_per_day,
                    total_volume=self.total_volume))
        if self.dispense_type == IM:
            prescription = (
                '{medication} IntraMuscular {concentration} {duration} '
                '({total_volume})'.format(
                    medication=self.medication.name,
                    duration=self.duration,
                    concentration=self.concentration,
                    times_per_day=self.times_per_day,
                    total_volume=self.total_volume))
        if self.dispense_type == SUPPOSITORY:
            prescription = (
                '{medication} {number_of_tablets} suppository {times_per_day} times per day '
                '({total_number_of_tablets} suppository)'.format(
                    medication=self.medication.name,
                    number_of_tablets=self.number_of_tablets,
                    times_per_day=self.times_per_day,
                    total_number_of_tablets=self.total_number_of_tablets))
        if self.dispense_type == CAPSULE:
            prescription = (
                '{medication} {number_of_tablets} capsules {times_per_day} times per day '
                '({total_number_of_tablets} capsules)'.format(
                    medication=self.medication.name,
                    number_of_tablets=self.number_of_tablets,
                    times_per_day=self.times_per_day,
                    total_number_of_tablets=self.total_number_of_tablets))
        return prescription

    @property
    def label_context(self):
        label_context = {
            'site': self.patient.site,
            'telephone_number': self.patient.site.telephone_number,
            'patient': self.patient.subject_identifier,
            'initials': self.patient.initials,
            'sid': self.patient.sid,
            'times_per_day': self.times_per_day,
            'drug_name': self.medication,
            'prepared_datetime': self.prepared_datetime.strftime("%d-%m-%y %H:%M"),
            'prepared_by': Profile.objects.get(user__username=self.user_created).initials,
            'storage_instructions': self.medication.storage_instructions,
            'protocol': self.medication.protocol,
            'weight': self.weight,
        }
        if self.dispense_type == TABLET:
            label_context.update({
                'number_of_tablets': self.number_of_tablets,
                'total_number_of_tablets': self.total_number_of_tablets,
            })
        elif self.dispense_type == SYRUP:
            label_context.update({
                'number_of_teaspoons': self.dose,
                'total_volume': self.total_volume,
            })
        elif self.dispense_type == IV:
            label_context.update({
                'concentration': self.concentration,
                'total_volume': self.total_volume,
                'infusion': self.infusion_number,
            })
        elif self.dispense_type == IM:
            label_context.update({
                'concentration': self.concentration,
                'total_volume': self.total_volume,
                'infusion': self.infusion_number,
            })
        elif self.dispense_type == SOLUTION:
            label_context.update({
                'number_of_teaspoons': self.dose,
                'concentration': self.concentration,
                'total_volume': self.total_volume
            })
        elif self.dispense_type == CAPSULE:
            label_context.update({
                'concentration': self.concentration,
                'total_volume': self.total_volume
            })
        elif self.dispense_type == SUPPOSITORY:
            label_context.update({
                'concentration': self.concentration,
                'total_volume': self.total_volume
            })
        return label_context

    class Meta:
        app_label = 'edc_pharma'
        unique_together = (('patient', 'medication', 'prepared_date'), )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    initials = models.CharField(
        max_length=4,
        validators=[RegexValidator(r'^[A-Z]{2,3}$', message='Use CAPS, 2-4 letters')],)
