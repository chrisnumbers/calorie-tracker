import requests
import calorietracker
import os
APPLICATION_ID = os.environ["NUTRITIONIX_APPLICATION_ID"]
API_KEY = os.environ["NUTRITIONIX_API_KEY"]


calorietracker = calorietracker.CalorieTracker(api_key=API_KEY,application_id=APPLICATION_ID)

calorietracker.get_food_items()
calorietracker.check_food_correctness()
