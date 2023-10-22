from flask import Blueprint, render_template, request
import requests 

from . import creds

mapsKey = creds.google_key

calc = Blueprint('calculator', __name__)

def configure():
    load_dotenv

#add get/post request code here 
@calc.route('/calculator', methods=['GET','POST'])
def calculator():
    #add code to get data from form here
    carbon_equiv = 0 
    price = 0
    place1 = request.form.get('origin')
    if isinstance(place1, str):
        
        place1 = place1.split(', USA')
        place1 = [part.strip() for part in place1 if part.strip()]
        place1 = ', '.join(place1)
        print(place1)
    #place1 = place1.split(', ')[0]
    #city_state_country = place1.split(', ')[0]
    


    
    #place2 = place2.split(', ')[0]
    #city_state_country2 = place2.split(', ')[0]
    place2 = request.form.get('destination')
    if isinstance(place2, str):
        
        place2= place2.split(', USA')
        place2 = [part2.strip() for part2 in place2 if part2.strip()]
        place2 = ', '.join(place2)
        print(place2)
        

    transport = request.form.get('transportmode')
    print(transport)
    if request.method == 'POST':
        carbon_equiv = round(distanceCalc(place1, place2, transport),2)
        price = round(total(carbon_equiv),2)
    print("Total Carbon Emissions: ", carbon_equiv)
    print("Cost to Counterbalance:", price)
   
        
    return render_template("calculator.html", carbon_equiv=carbon_equiv, price=price, mapsKey=mapsKey)


def distanceCalc(origin, destination,modeOfTransport):
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
    
        print(f"Request to the Distance Matrix API failed with status code: {distance_matrix_response.status_code}")

    return carbonCalc(distance_int,modeOfTransport)



def carbonCalc(distance_int, transportation):
    #CarTravel, FromFlight, FromMotorBike, FromPublicTransit
    #transportation = "FromFlight"
    #distance = parseFloat(document.getElementById("distance").value)
    #selectedTransport = 'input[name="transportmode"]:checked'.value
    #print(selectedTransport)
    #public = "SmallDieselCar"

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
    elif transportation == "ClassicBus":
        carbon_footprint_url = "https://carbonfootprint1.p.rapidapi.com/CarbonFootprintFromPublicTransit"
        carbon_footprint_params = {
                "distance": distance_int,
                "type": transportation
            }

    elif transportation == "NationalTrain":
        carbon_footprint_url = "https://carbonfootprint1.p.rapidapi.com/CarbonFootprintFromPublicTransit"
        carbon_footprint_params = {
                "distance": distance_int,
                "type": transportation
            }

    elif transportation == "Subway":
        carbon_footprint_url = "https://carbonfootprint1.p.rapidapi.com/CarbonFootprintFromPublicTransit"
        carbon_footprint_params = {
                "distance": distance_int,
                "type": transportation
            }

    ''' if public == "Bus":
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
            '''
    # Define the query parameters for the carbon footprint API
       # print(public)

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

    return carbon_equivalent

def total(carbon_equivalent):
    companyCost = 20
    total = ((carbon_equivalent * companyCost)/1000)
    return total 
