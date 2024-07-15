import requests, datetime
nutritionix_endpoint = "https://trackapi.nutritionix.com"
instant_endpoint = f"{nutritionix_endpoint}/v2/search/instant"
sheety_endpoint = "https://api.sheety.co/570089251c12aa4caaf1dce1bba9b271/calorieTracker/sheet1"

class CalorieTracker:
    
    def __init__(self, api_key, application_id, sheety_auth_token) -> None:
        self.api_key = api_key
        self.application_id = application_id
        self.sheety_auth_token = sheety_auth_token
        self.nutritionix_headers = {
            "x-app-id": self.application_id,
            "x-app-key": self.api_key,
        }

        self.sheety_headers = {
            "Authorization": f"Bearer {self.sheety_auth_token}"
        }


    def get_food_items(self):
        self.user_input = input("Enter the food you want to add. \n")
        self.food_items_amount = int(input("How many food items did you add? \n"))
        self.branded = input("Is this branded (fast food,restaurant,etc)? Yes/No \n").lower()
        self.get_food_items_parameters = {
            "query": self.user_input
        }
        self.food_items_response = requests.get(url=instant_endpoint, params=self.get_food_items_parameters, headers=self.nutritionix_headers)
        self.food_items_response.raise_for_status()
        self.food_data = self.food_items_response.json()
        print(self.food_data)
        if self.branded == "yes":
            self.category = "branded"
        else:
            self.category = "common"
        self.food_items = []
        for item in self.food_data[self.category][:self.food_items_amount]:
            self.food_items.append(item)

        #return self.food_items
    
    def check_food_correctness(self):
        while True:
            self.list_food_items()
            self.food_correctness_answer = input("Does this all look correct? Yes/No \n").lower()
            if self.food_correctness_answer == "yes":
                break

            #self.food_correctness_answer = input("Does this all look correct? Yes/No \n").lower()

            if self.food_correctness_answer == "no":
                self.user_option = input("\nOkay, here are some options.\n1. Restart\n2. Remove specific item\n")
                while self.user_option != "1" and self.user_option != "2":
                    print(type(self.user_option))
                    print(self.user_option)
                    self.user_option = input("Incorrect input Try again. The options are:\n1. Restart\n2. Remove specific item\n")
                if self.user_option == "1":
                    print("Restarting...")
                    self.get_food_items()
                elif self.user_option =="2":
                    self.list_food_items()
                    #Need to add error handling
                    self.removal_option = int(input("Which one do you want to remove? Please enter the number. \n"))
                    self.food_items.remove(self.food_items[self.removal_option - 1])
                    #self.check_food_correctness()
        print("Awesome! Since there are no issues, I'll add these to the spreadsheet.")
        if self.category == "branded":
            self.food_name_tag = "brand_name_item_name"
        else:
            self.food_name_tag = "food_name"
        self.today = datetime.datetime.now()
        self.date = self.today.strftime("%m/%d/%Y")
        for food_item in self.food_items:
            self.sheety_parameters = {
                
                "sheet1": {
                    "foodName": food_item[self.food_name_tag],
                    "calories": food_item["nf_calories"],
                    "amount": food_item["serving_qty"],
                    "date": self.date, 
                }
            }
            food_item_post = requests.post(url=sheety_endpoint, json=self.sheety_parameters, headers=self.sheety_headers)
            food_item_post.raise_for_status()
            print(food_item_post.text)


    def list_food_items(self):
        self.num = 1
        #if self.branded == "yes":
        #    self.category = "branded"
        #else:
        #    self.category = "common"
        print("Current Food Items:")
        for food_item in self.food_items:
            #print(food_item)
            #print(type(food_item))
            print(f"{self.num}. {food_item['food_name']} - Calories: {food_item['nf_calories']}")
            self.num += 1
            
