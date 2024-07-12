from django.shortcuts import render
from .models import Dish

def search(request):
    query = request.GET.get('q')
    if query:
        dishes = Dish.objects.filter(name__icontains=query)
    else:
        dishes = Dish.objects.none()
    return render(request, 'index.html', {'dishes': dishes})