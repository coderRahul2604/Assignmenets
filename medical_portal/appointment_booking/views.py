from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import CustomUser
from .models import Appointment
from .forms import AppointmentForm
import requests  
from datetime import datetime, timedelta

# Create your views here.

def doctors_list(request):
    doctors = CustomUser.objects.filter(is_doctor=True)
    for doctor in doctors:
        print(doctor.username)
    return render(request, 'appointment_booking/doctors_list.html', {'doctors': doctors})

MOCK_API_URL = 'https://run.mocky.io/v3/656e5f3e-212f-417d-99ea-989963436286'  

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(CustomUser, id=doctor_id, is_doctor=True)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = request.user

            # Check for conflicts
            appointment_start = datetime.combine(appointment.date, appointment.start_time)
            appointment_end = appointment_start + timedelta(minutes=45)
            
            conflicting_appointments = Appointment.objects.filter(
                doctor=doctor,
                date=appointment.date,
                start_time__lt=appointment_end.time(),
                end_time__gt=appointment.start_time
            )
            
            if conflicting_appointments.exists():
                messages.warning(request, "This time slot is already booked. Please choose another time.")
            else:
                appointment.end_time = (datetime.combine(appointment.date, appointment.start_time) + timedelta(minutes=45)).time()
                appointment.save()
                return redirect('my_appointment')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointment_booking/book_appointment.html', {'form': form, 'doctor': doctor})
def my_appointment(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('-date')
    return render(request, 'appointment_booking/appointment_details.html', {'appointments':appointments})
