from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import CustomUser
from blogging.models import Blog, Category
from appointment_booking.models import Appointment
from .forms import CustomUserCreationForm, CustomLoginForm


def home(request):
    signup_form = CustomUserCreationForm()
    login_form = CustomLoginForm()
    return render(request, 'index.html', {'signup_form': signup_form, 'login_form': login_form})
    
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('/')
    
    signup_form = CustomUserCreationForm()
    login_form = CustomLoginForm()
    messages.error(request, 'Something went wrong please try again.')
    return render(request, 'index.html', {'signup_form': signup_form, 'login_form': login_form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            messages.success(request, 'Loged In successfully.')
            if user is not None:
                login(request, user)
                if user.is_patient:
                    return redirect('dashboard')
                elif user.is_doctor:
                    return redirect('dashboard')
   
    signup_form = CustomUserCreationForm()
    login_form = CustomLoginForm()
    messages.error(request, 'Username or passwaord is incorrect. Please check it and try again.')
    return render(request, 'index.html', {'signup_form': signup_form, 'login_form': login_form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Logout successfully.')
        return redirect('home')
    return redirect('home')

@login_required
def dashboard(request):
    user_info = CustomUser.objects.get(username=request.user.username)
    my_blogs = Blog.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'user_info': user_info, 'my_blogs': my_blogs})

def contact(request):
    return render(request, 'contact.html')
