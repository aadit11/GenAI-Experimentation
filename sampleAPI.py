from openai import AzureOpenAI
import requests
import os
import json

os.environ["AZURE_OPENAI_API_KEY"] = ''

client = AzureOpenAI(
    api_version="",
    azure_endpoint=""
)


def call_joke_api(joke_type):
    url = f"https://official-joke-api.appspot.com/random_joke?type={joke_type}"
    response = requests.get(url)
    return response.json()

def call_weather_api(location):
    return {"weather": "Sunny", "location": location}

def process_query(query):
    function_descriptions = [
        {
            "name": "get_joke",
            "description": "Get a random joke of a specified type",
            "parameters": {
                "type": "object",
                "properties": {
                    "joke_type": {
                        "type": "string",
                        "description": "Type of the joke, e.g., general, programming"
                    }
                }
            }
        },
        {
            "name": "get_weather",
            "description": "Get the weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location for the weather, e.g., Boston"
                    }
                }
            }
        }
    ]

    response = client.chat.completions.create(
        model="gpt4turboindia",
        messages=[{"role": "user", "content": query}],
        functions=function_descriptions
    )

    if response.choices[0].message.function_call:
        function_call = response.choices[0].message.function_call
        function_name = function_call.name  

        arguments = json.loads(function_call.arguments) if function_call.arguments else {}

        if function_name == 'get_joke':
            joke_type = arguments.get('joke_type', 'general')
            joke_data = call_joke_api(joke_type)
            return f"{joke_data['setup']} {joke_data['punchline']}"
        elif function_name == 'get_weather':
            location = arguments.get('location')
            if location:
                weather_data = call_weather_api(location)
                return f"The weather in {weather_data['location']} is {weather_data['weather']}."
            else:
                return "Location parameter missing for weather function."

    return "Could not process the query."

query = "Tell me a tech joke"
result = process_query(query)
print(result)