from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    cuisine = models.CharField(max_length=255)
    price_range = models.IntegerField()
    user_rating = models.FloatField()

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='dishes')

    def __str__(self):
        return self.name