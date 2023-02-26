import requests
import os
import dotenv
import datetime as dt

dotenv.load_dotenv()
APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
SHEETY_API = os.environ["SHEETY_API"]

date, time = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S").split()

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

url = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_url = f"https://api.sheety.co/{SHEETY_API}/myWorkouts/workouts"

exercise = input("Please tell us what exercise you did: ")
user_details = {
    "query":exercise,
    "gender": "male",
    "weight_kg": 64,
    "height_cm": 176,
    "age":20
}

data = requests.post(url=url, json=user_details, headers=headers)
data.raise_for_status()
workout_data = data.json()["exercises"]

for i in workout_data:
    activity = i["name"]
    calories = i['nf_calories']
    duration = i["duration_min"]
    sheet_json = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": activity.title(),
            "duration": duration,
            "calories": calories
        }
    }

    sheet_post = requests.post(url=sheety_url, json=sheet_json)
    sheet_post.raise_for_status()
    print(sheet_post.text)


