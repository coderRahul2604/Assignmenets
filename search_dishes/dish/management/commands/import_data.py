# dish/management/commands/import_dishes.py
import csv
import json
import re
from json import JSONDecodeError

from django.core.management.base import BaseCommand
from dish.models import Restaurant, Dish

class Command(BaseCommand):
    help = 'Import dishes from CSV'

    def handle(self, *args, **kwargs):
        csv_file = 'dish/management/commands/restaurants_small.csv'  # Update with actual path

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row

            for row in reader:
                restaurant_name = row[1].strip()
                location = row[2].strip()

                # Parse restaurant JSON data
                try:
                    if row[5].strip():
                        json_data = json.loads(row[5].strip())
                    else:
                        raise ValueError("Empty JSON data")
                except (JSONDecodeError, ValueError) as e:
                    print(f"JSONDecodeError: Failed to parse JSON in row: {row}, Error: {e}")
                    continue

                cuisine = json_data.get('cuisines', '')
                price_range = json_data.get('price_range', 0)
                user_rating = json_data.get('user_rating', {}).get('aggregate_rating', 0)

                # Create or update the Restaurant instance
                restaurant, created = Restaurant.objects.get_or_create(
                    name=restaurant_name,
                    defaults={'location': location, 'cuisine': cuisine, 'price_range': price_range, 'user_rating': user_rating}
                )

                if not created:
                    restaurant.location = location
                    restaurant.cuisine = cuisine
                    restaurant.price_range = price_range
                    restaurant.user_rating = user_rating
                    restaurant.save()

                # Parse dishes JSON data
                try:
                    if row[3].strip():
                        dishes = json.loads(row[3].strip())
                    else:
                        dishes = {}
                except (JSONDecodeError, ValueError) as json_err:
                    print(f"Error decoding JSON for dishes in row: {row}: {json_err}")
                    continue

                for dish_name, dish_price in dishes.items():
                    price_match = re.search(r'(\d+(\.\d+)?)', dish_price)
                    if price_match:
                        dish_price_float = float(price_match.group(1))
                    else:
                        dish_price_float = 0.0

                    # Create or update the Dish instance
                    Dish.objects.update_or_create(
                        name=dish_name.strip(),
                        restaurant=restaurant,
                        defaults={'price': dish_price_float}
                    )
