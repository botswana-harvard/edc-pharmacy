from datetime import date

from django import forms
from django.db.models import Q
from django.urls.base import reverse

from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from .constants import TABLET, SYRUP, IV, CAPSULE, SOLUTION, IM, SUPPOSITORY
from .models import Dispense, Profile


class PatientSearchForm(forms.Form):

    subject_identifier = forms.CharField(
        label='Patient Identifier',
        max_length=36)

    def __init__(self, *args, **kwargs):
        super(PatientSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper = FormHelper()
        self.helper.form_action = reverse('home_url')
        self.helper.form_id = 'form-patient-search'
        self.helper.form_method = 'post'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            FieldWithButtons('subject_identifier', StrictButton('Search', type='submit')))


class DispenseForm(forms.ModelForm):

    def clean(self):
        if self.data['dispense_type'] == TABLET:
            self.validate_tablet()
        elif self.data['dispense_type'] == SYRUP:
            self.validate_syrup()
        elif self.data['dispense_type'] == IV:
            self.validate_iv()
        elif self.data['dispense_type'] == CAPSULE:
            self.validate_capsule()
        elif self.data['dispense_type'] == IM:
            self.validate_im()
        elif self.data['dispense_type'] == SOLUTION:
            self.validate_solution()
        elif self.data['dispense_type'] == SUPPOSITORY:
            self.validate_suppository()
        else:
            pass
        self.catch_unique_integrity_error()
        return self.cleaned_data

    def catch_unique_integrity_error(self):
        if Dispense.objects.filter(
                Q(patient=self.cleaned_data['patient']) &
                Q(medication=self.cleaned_data['medication']) &
                Q(prepared_date=date.today())):
            raise forms.ValidationError('Dispense record of this medication on this date already exists for this patient')
        return self.cleaned_data

    def validate_tablet(self):
        if self.data['dose']:
            raise forms.ValidationError({
                'dose': [
                    'You have selected dispense type tablet, you should NOT enter dose']})
        if not self.data['number_of_tablets']:
            raise forms.ValidationError({
                'number_of_tablets': [
                    'You have selected dispense type tablet, you should enter number of tablets']})
        if self.data['total_volume']:
            raise forms.ValidationError({
                'total_volume': [
                    'You have selected dispense type tablet, you should NOT enter total volume']})
        if self.data['duration']:
            raise forms.ValidationError({
                'duration': [
                    'You have selected dispense type tablet, you should NOT enter duration']})
        if not self.data['total_number_of_tablets']:
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'You have selected dispense type tablet, you should enter total number of tablets']})
        if not self.data['times_per_day']:
            raise forms.ValidationError({
                'times_per_day': [
                    'You have selected dispense type tablet, you should enter times per day']})
        if not self.data['concentration']:
            raise forms.ValidationError({
                'concentration': [
                    'You have selected dispense type tablet, you should enter concentration']})
        if float(self.data['total_number_of_tablets']) < float(self.data['times_per_day']) * float(self.data['number_of_tablets']):
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'Cannot have total number of tablets less than number of tablets by times per day']})

    def validate_capsule(self):
        if self.data['dose']:
            raise forms.ValidationError({
                'dose': [
                    'You have selected dispense type capsule, you should NOT enter dose']})
        if not self.data['number_of_tablets']:
            raise forms.ValidationError({
                'number_of_tablets': [
                    'You have selected dispense type capsule, you should enter number of tablets']})
        if self.data['total_volume']:
            raise forms.ValidationError({
                'total_volume': [
                    'You have selected dispense type capsule, you should NOT enter total volume']})
        if self.data['duration']:
            raise forms.ValidationError({
                'duration': [
                    'You have selected dispense type capsule, you should NOT enter duration']})
        if not self.data['total_number_of_tablets']:
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'You have selected dispense type capsule, you should enter total number of tablets']})
        if not self.data['times_per_day']:
            raise forms.ValidationError({
                'times_per_day': [
                    'You have selected dispense type capsule, you should enter times per day']})
        if not self.data['concentration']:
            raise forms.ValidationError({
                'concentration': [
                    'You have selected dispense type capsule, you should enter concentration']})
        if float(self.data['total_number_of_tablets']) < float(self.data['times_per_day']) * float(self.data['number_of_tablets']):
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'Cannot have total number of capsule less than number of capsule by times per day']})

    def validate_suppository(self):
        if self.data['dose']:
            raise forms.ValidationError({
                'dose': [
                    'You have selected dispense type suppository, you should NOT enter syrup dose']})
        if not self.data['number_of_tablets']:
            raise forms.ValidationError({
                'number_of_tablets': [
                    'You have selected dispense type suppository, you should enter number of suppository']})
        if self.data['total_volume']:
            raise forms.ValidationError({
                'total_volume': [
                    'You have selected dispense type suppository, you should NOT enter total dosage volume']})
        if self.data['duration']:
            raise forms.ValidationError({
                'duration': [
                    'You have selected dispense type suppository, you should NOT enter IV duration']})
        if not self.data['total_number_of_tablets']:
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'You have selected dispense type suppository, you should enter total number of suppository']})
        if not self.data['times_per_day']:
            raise forms.ValidationError({
                'times_per_day': [
                    'You have selected dispense type suppository, you should enter times per day']})
        if not self.data['concentration']:
            raise forms.ValidationError({
                'concentration': [
                    'You have selected dispense type suppository, you should enter concentration']})
        if float(self.data['total_number_of_tablets']) < float(self.data['times_per_day']) * float(self.data['number_of_tablets']):
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'Cannot have total number of suppository less than number of suppository by times per day']})

    def validate_syrup(self):
        if not self.data['dose']:
            raise forms.ValidationError({
                'dose': [
                    'You have selected dispense type syrup, you should enter dose']})
        if self.data['number_of_tablets']:
            raise forms.ValidationError({
                'number_of_tablets': [
                    'You have selected dispense type syrup, you should NOT enter number of tablets']})
        if self.data['total_number_of_tablets']:
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'You have selected dispense type syrup, you should NOT enter total number of tablets']})
        if not self.data['total_volume']:
            raise forms.ValidationError({
                'total_volume': [
                    'You have selected dispense type syrup, you should enter total volume']})
        if self.data['duration']:
            raise forms.ValidationError({
                'duration': [
                    'You have selected dispense type syrup, you should NOT enter duration']})
        if not self.data['concentration']:
            raise forms.ValidationError({
                'concentration': [
                    'You have selected dispense type syrup, you should enter concentration']})
        if not self.data['times_per_day']:
            raise forms.ValidationError({
                'times_per_day': [
                    'You have selected dispense type syrup, you should enter times per day']})

    def validate_iv(self):
        if self.data['dose']:
            raise forms.ValidationError({
                'dose': [
                    'You have selected dispense type IV, you should NOT enter dose']})
        if self.data['number_of_tablets']:
            raise forms.ValidationError({
                'number_of_tablets': [
                    'You have selected dispense type IV, you should NOT enter number of tablets']})
        if not self.data['total_volume']:
            raise forms.ValidationError({
                'total_volume': [
                    'You have selected dispense type IV, you should enter total volume']})
        if not self.data['duration']:
            raise forms.ValidationError({
                'duration': [
                    'You have selected dispense type IV, you should enter duration']})
        if not self.data['concentration']:
            raise forms.ValidationError({
                'concentration': [
                    'You have selected dispense type IV, you should enter concentration']})
        if self.data['total_number_of_tablets']:
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'You have selected dispense type IV, you should NOT enter total number of tablets']})
        if self.data['times_per_day']:
            raise forms.ValidationError({
                'times_per_day': [
                    'You have selected dispense type IV, you should NOT enter times per day']})
        if not self.data['infusion_number']:
            raise forms.ValidationError({
                'infusion_number': [
                    'You have selected dispense type IV, you should enter infusion']})

    def validate_im(self):
        if self.data['dose']:
            raise forms.ValidationError({
                'dose': [
                    'You have selected dispense type IM, you should NOT enter dose']})
        if self.data['number_of_tablets']:
            raise forms.ValidationError({
                'number_of_tablets': [
                    'You have selected dispense type IM, you should NOT enter number of tablets']})
        if not self.data['total_volume']:
            raise forms.ValidationError({
                'total_volume': [
                    'You have selected dispense type IM, you should enter total volume']})
        if not self.data['duration']:
            raise forms.ValidationError({
                'duration': [
                    'You have selected dispense type IM, you should enter duration']})
        if not self.data['concentration']:
            raise forms.ValidationError({
                'concentration': [
                    'You have selected dispense type IM, you should enter concentration']})
        if self.data['total_number_of_tablets']:
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'You have selected dispense type IM, you should NOT enter total number of tablets']})
        if self.data['times_per_day']:
            raise forms.ValidationError({
                'times_per_day': [
                    'You have selected dispense type IM, you should NOT enter times per day']})
        if not self.data['infusion_number']:
            raise forms.ValidationError({
                'infusion_number': [
                    'You have selected dispense type IV, you should enter infusion']})

    def validate_solution(self):
        if not self.data['dose']:
            raise forms.ValidationError({
                'dose': [
                    'You have selected dispense type solution, you should enter dose']})
        if self.data['number_of_tablets']:
            raise forms.ValidationError({
                'number_of_tablets': [
                    'You have selected dispense type solution, you should NOT enter number of tablets']})
        if self.data['total_number_of_tablets']:
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'You have selected dispense type solution, you should NOT enter total number of tablets']})
        if not self.data['total_volume']:
            raise forms.ValidationError({
                'total_volume': [
                    'You have selected dispense type solution, you should enter total volume']})
        if self.data['duration']:
            raise forms.ValidationError({
                'duration': [
                    'You have selected dispense type solution, you should NOT enter duration']})
        if not self.data['concentration']:
            raise forms.ValidationError({
                'concentration': [
                    'You have selected dispense type solution, you should enter concentration']})
        if not self.data['times_per_day']:
            raise forms.ValidationError({
                'times_per_day': [
                    'You have selected dispense type solution, you should enter times per day']})

    class Meta:
        model = Dispense
        fields = '__all__'


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
