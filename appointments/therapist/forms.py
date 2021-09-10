from django import forms
from django.db import models
from patient.models import *
from patient.forms import appointment_date_validation, HOUR_CHOICES
from datetime import date, time



YEAR_CHOICES = [(x+2021,y) for x,y in enumerate(list(range(2021,2051)))]

month_li = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

MONTH_CHOICES = [(x,y) for x,y in enumerate(month_li, 1)]

class CalendarForm(forms.Form):
    year = forms.ChoiceField(choices = YEAR_CHOICES)
    month = forms.ChoiceField(choices = MONTH_CHOICES)

class AppointmentResponseForm(forms.ModelForm):
    class Meta:
        model = AppointmentResponse
        fields = ['start_time', 'appointment_date']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date'}),
            'start_time': forms.Select(choices=HOUR_CHOICES),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time < time(9,30,00) or start_time > time(16,30,00):
            raise forms.ValidationError('Only choose times between 9am and 16:30pm')
        return start_time

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        start_time = self.clean_start_time()
        disabled_days = [4,5]
        date = appointment_date_validation(appointment_date, start_time, disabled_days)
        return date


class EditAppointmentResponseForm(forms.ModelForm):
    class Meta:
        model = AppointmentResponse
        exclude = ['user', 'is_approved', 'choice','original_request']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date'}),
            'start_time': forms.Select(choices=HOUR_CHOICES),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time < time(9,30,00) or start_time > time(16,30,00):
            raise forms.ValidationError('Only choose times between 9am and 16:30pm')
        return start_time

    def clean_appointment_date(self):
        start_time = self.clean_start_time()
        appointment_date = self.cleaned_data['appointment_date']
        disabled_days = [4,5]
        date = appointment_date_validation(appointment_date, start_time, disabled_days)
        return date

    
class EditAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['user', 'is_approved', 'choice']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date'}),
            'start_time': forms.Select(choices=HOUR_CHOICES),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time < time(9,30,00) or start_time > time(16,30,00):
            raise forms.ValidationError('Only choose times between 9am and 16:30pm')
        return start_time

    def clean_appointment_date(self):
        start_time = self.clean_start_time()
        appointment_date = self.cleaned_data['appointment_date']
        disabled_days = [4,5]
        date = appointment_date_validation(appointment_date, start_time, disabled_days)
        return date


class TherapistCreateAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['start_time','user', 'appointment_date']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date'}),
            'start_time': forms.Select(choices=HOUR_CHOICES),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time < time(9,30,00) or start_time > time(16,30,00):
            raise forms.ValidationError('Only choose times between 9am and 16:30pm')
        return start_time

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        start_time = self.clean_start_time()
        disabled_days = [4,5]
        date = appointment_date_validation(appointment_date, start_time, disabled_days)
        return date