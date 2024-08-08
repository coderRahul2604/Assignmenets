from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="I am a"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture', 
                  'address_line1', 'city', 'state', 'pincode', 'user_type']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")
        user_type = cleaned_data.get("user_type")

        if password != confirm_password:
            self.add_error('password2', "Passwords do not match")

        if user_type not in ['patient', 'doctor']:
            self.add_error('user_type', "Please select a valid user type")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data.get('user_type')
        
        if user_type == 'patient':
            user.is_patient = True
            user.is_doctor = False
        elif user_type == 'doctor':
            user.is_patient = False
            user.is_doctor = True

        if commit:
            user.save()
        return user