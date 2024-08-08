
from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.doctor = kwargs.pop('doctor', None)
        self.patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Appointment
        fields = ['speciality', 'date', 'start_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def save(self, commit=True):
        appointment = super().save(commit=False)
        if self.doctor:
            appointment.doctor = self.doctor
        if self.patient:
            appointment.patient = self.patient
        if commit:
            appointment.save()
        return appointment
