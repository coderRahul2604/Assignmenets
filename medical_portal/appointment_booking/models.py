from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

class Appointment(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_appointments')
    speciality = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def save(self, *args, **kwargs):
        self.end_time = (datetime.combine(datetime.min, self.start_time) + timedelta(minutes=45)).time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Appointment with {self.doctor} on {self.date} at {self.start_time}'
