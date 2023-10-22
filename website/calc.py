from flask import Blueprint, render_template, request
import requests 

from . import creds

calc = Blueprint('calculator', __name__)

def configure():
    load_dotenv

#add get/post request code here 
@calc.route('/calculator', methods=['GET','POST'])
def calculator():
    #add code to get data from form here
    place1 = request.form.get('origin')
    place2 = request.form.get('destination')
    if request.method == 'POST':
        distanceCalc(place1, place2)
    return render_template("calculator.html")


def distanceCalc(origin, destination):
    # Define the places
    #origin = "Atlanta, GA"
    #destination = "Chicago, IL"


    # Define the Google Maps API endpoint URL
    distance_matrix_url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    # Define the query parameters for the Distance Matrix API
    distance_matrix_params = {
        
        "destinations": destination,
        "origins": origin,
        "units": "imperial",
        "key": creds.google_key
    }

    # Make an HTTP GET request to the Google Maps Distance Matrix API
    distance_matrix_response = requests.get(distance_matrix_url, params=distance_matrix_params)

    # Check if the request to the Distance Matrix API was successful (status code 200)
    if distance_matrix_response.status_code == 200:
        # Parse the response as JSON
        distance_data = distance_matrix_response.json()

        print(distance_data)

        # Extract the distance text
        distance_text = distance_data["rows"][0]["elements"][0]["distance"]["text"]
        distance_int = int(''.join(filter(str.isdigit, distance_text)))
        print(f"From: {origin} to {destination}: {distance_int} miles")

    else:
        print("before")
        print(f"Request to the Distance Matrix API failed with status code: {distance_matrix_response.status_code}")

    return carbonCalc(distance_int)



def carbonCalc(distance_int):
    #CarTravel, FromFlight, FromMotorBike, FromPublicTransit
    transportation = "FromFlight"
    public = "SmallDieselCar"


    # Define the carbon footprint API endpoint URL
    if transportation == "FromFlight":
        carbon_footprint_url = "https://carbonfootprint1.p.rapidapi.com/CarbonFootprintFromFlight"
        carbon_footprint_params = {
        "distance": distance_int,
        "type": "DomesticFlight"
        }

    elif transportation == "FromCarTravel":
        carbon_footprint_url = "https://carbonfootprint1.p.rapidapi.com/CarbonFootprintFromCarTravel"
        carbon_footprint_params = {
            "distance": distance_int,
            "vehicle": "SmallDieselCar"
        }
        
    elif transportation == "FromMotorBike":
        carbon_footprint_url = "https://carbonfootprint1.p.rapidapi.com/CarbonFootprintFromMotorBike"
        carbon_footprint_params = {
            "type": "SmallMotorBike",
            "distance": distance_int
        }
    elif transportation == "FromPublicTransit":
        carbon_footprint_url = "https://carbonfootprint1.p.rapidapi.com/CarbonFootprintFromPublicTransit"
        if public == "ClassicBus":
            carbon_footprint_params = {
                "distance": distance_int,
                "type": "ClassicBus"
            }
        elif public == "NationalTrain":
            carbon_footprint_params = {
                "distance": distance_int,
                "type": "NationalTrain"
            }
        elif public == "Subway":
            carbon_footprint_params = {
                "distance": distance_int,
                "type": "Subway"
            }
    # Define the query parameters for the carbon footprint API


    # Define the headers for the RapidAPI
    carbon_footprint_headers = {
        "X-RapidAPI-Key": creds.rapid_key,
        "X-RapidAPI-Host": "carbonfootprint1.p.rapidapi.com"
    }

    # Make an HTTP GET request to the carbon footprint API
    carbon_footprint_response = requests.get(carbon_footprint_url, headers=carbon_footprint_headers, params=carbon_footprint_params)

    # Check if the request to the carbon footprint API was successful (status code 200)
    if carbon_footprint_response.status_code == 200:
        # Parse the response as JSON
        carbon_footprint_data = carbon_footprint_response.json()
        carbon_equivalent = carbon_footprint_data['carbonEquivalent']
        
        print(f'Carbon Equivalent: {carbon_equivalent}')

    else:
        print(f"Request to the Carbon Footprint API failed with status code: {carbon_footprint_response.status_code}")



    companyCost = 20
    total = ((carbon_equivalent * companyCost)/1000)
    print("This is carbon offset to donate: $", total)
