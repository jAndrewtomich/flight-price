from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager


def main():

    data_manager = DataManager()
    sheet_data = data_manager.get_destination_data()
    flight_search = FlightSearch()
    notification_manager = NotificationManager()

    origin_iata = input("Enter origin IATA Code: ")

    if sheet_data[0]["iataCode"] == "":
        for row in sheet_data:
            row["iataCode"] = flight_search.get_destination_code(row["city"])
        print(sheet_data)

        data_manager.destination_data = sheet_data
        data_manager.update_destination_codes()

    tomorrow = datetime.now() + timedelta(1)
    six_months_from_today = datetime.now() + timedelta(180)

    for destination in sheet_data:
        flight = flight_search.check_flights(
            origin_iata,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_months_from_today
        )
        if flight and flight.price < destination["lowestPrice"]:
            notification_manager.send_sms(
                message=f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}.\n"
            )


if __name__ == "__main__":
    main()
