import os
import requests
# import yfinance as yf
from swarm import Swarm, Agent
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# Initialize Swarm client

client = Swarm()

# Load OpenWeatherMap API key from environment variable
API_KEY = os.getenv('OPENWEATHER_API_KEY')
if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY environment variable not set")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to fetch real weather data


def get_weather(location):
    print(f"Running weather function for {location}...")

    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"  # Change to 'imperial' for Fahrenheit
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        city_name = data['name']
        return f"The weather in {city_name} is {temperature}°C with {weather_description}."
    else:
        return f"Could not get the weather for {location}. Please try again."


def transfer_to_weather_assistant():
    print("Transferring to Weather Assistant...")
    return weather_agent


# manager Agent
manager_agent = Agent(
    name="manager Assistant",
    instructions="You help users by directing them to the right assistant.",
    functions=[transfer_to_weather_assistant],
)

# Weather Agent
weather_agent = Agent(
    name="Weather Assistant",
    instructions="You provide weather information for a given location using the provided tool",
    functions=[get_weather],
)

print("Running manager Assistant for Weather...")

response = client.run(
    agent=manager_agent,
    messages=[{"role": "user", "content": "What's the weather in Kochi?"}],
)
print(response.messages[-1]["content"])
