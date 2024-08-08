from django.urls import path
from appointment_booking import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.doctors_list, name='doctor_list'),
    path('book_appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('my_appointment/', views.my_appointment, name='my_appointment'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)