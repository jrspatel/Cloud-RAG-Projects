import json
import os
import requests 
from openai import AzureOpenAI 

def main():
    # defining the azure api client 
    
    api_key = '#'

    client = AzureOpenAI(
        # model specific api_key and endpoint
        api_key= api_key,
        azure_endpoint = '#',
        api_version= '2024-05-01-preview'

    )

    functions=[
        {
            "name":"getWeather",
            "description":"Retrieve real-time weather information/data about a particular location/place",
            "parameters":{
                "type":"object",
                "properties":{
                    "location":{
                        "type":"string",
                        "description":"the exact location whose real-time weather is to be determined",
                    },
                    
                },
                "required":["location"]
            },
        }
    ] 

    # openweather api - current weather fetching
    def get_weather(location):
        location_url = '#'

        response = requests.get(location_url) 
        get_response = response.json()
        latitude = get_response['coord']['lat']
        longitude = get_response['coord']['lon']

        print(f'latitude: {latitude}')
        print(f'longitude: {longitude}')

        weather_url = '#'
        final_response = requests.get(weather_url) 
        final_response_json = final_response.json()
        print(final_response_json)
        weather = final_response_json['weather']

        print(f'weather condition: {weather}')

    # define the api - chat_completion 
    first_response = client.chat.completions.create(
        model= 'test2-gpt',
        messages=[
            {"role":"system", "content":"you are a weather assistant helping people on real-time weather data/analytics"},
            {'role':'user', 'content':'what is the weather for tomorrow in boston?'}
        ],
        functions= functions
    ) 

    print(first_response.choices[0])

    # from the initial respomse which is of json form
    function_argument = json.loads(first_response.choices[0].message.function_call.arguments)
    location = function_argument['location'] 

    if location:
        print(f'city: {location}') 
        get_weather(location) 

    

    





if __name__=="__main__":
    main()

   