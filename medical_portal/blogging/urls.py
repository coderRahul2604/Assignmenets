from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blogging import views

urlpatterns = [
    path('', views.blog_page, name='Blog_Page'),
    path('create_blog/', views.create_blog, name='Create_blog'),
]
