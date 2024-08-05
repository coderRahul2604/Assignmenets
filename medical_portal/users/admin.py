from django.contrib import admin
from users.models import CustomUser

# Register your models here.

class CustomUserForm(admin.ModelAdmin):
    class Meta:
        model = CustomUser
        fields = ['is_patient', 'is_doctor', 'city', 'state']

admin.site.register(CustomUser)