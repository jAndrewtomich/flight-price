import json
from pprint import pprint
import requests

SHEETY_API_KEY = json.load(open("c:/users/johna/anaconda3/envs/FlightNotification/conda-meta/state"))["env_vars"]["SHEETY_API_KEY"]

SHEETY_ENDPOINT = "https://api.sheety.co/b5ed1fd769685ddab0e0c10421f060bf/flightDeals/prices"


class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.header = {
            "Authorization": f"Bearer {SHEETY_API_KEY}",
            "Content-Type": "application/json"
        }

    def get_destination_data(self):
        # 2. Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEETY_ENDPOINT, headers=self.header)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        # 3. Try importing pretty print and printing the data out again using pprint().
        # pprint(data)
        return self.destination_data

    # 6. In the DataManager Class make a PUT request and use the row id  from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=self.header
            )
            print(response.text)