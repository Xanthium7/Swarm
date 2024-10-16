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


# Fucntion to create Folders

# Global arrays to store paths
paths = {
    "react_project": "C:\\Users\\ASUS\\OneDrive\\Desktop\\reactjs_prots",
    "python_project": "C:\\Users\\ASUS\\OneDrive\\Desktop\\Python_projects",
}


def create_project_folder(folder_name):
    # Determine the project type based on the folder name
    if 'react' in folder_name.lower():
        project_type = 'react_project'
    elif 'python' in folder_name.lower():
        project_type = 'python_project'
    else:
        raise ValueError("Unsupported project type")

    # Create the new folder path
    location = paths[project_type]
    new_folder_path = os.path.join(location, folder_name)

    # Create the folder if it doesn't exist
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        return (f"Created folder: {new_folder_path}")
    else:
        return (f"Folder already exists: {new_folder_path}")


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


def transfer_to_folder_assistant():
    print("Transferring to Folder Assistant...")
    return folder_agent


# manager Agent
manager_agent = Agent(
    name="manager Assistant",
    instructions="You help users by directing them to the right assistant.",
    functions=[transfer_to_weather_assistant, transfer_to_folder_assistant],
)

# Weather Agent
weather_agent = Agent(
    name="Weather Assistant",
    instructions="You provide weather information for a given location using the provided tool",
    functions=[get_weather],
)

# Folder Agent
folder_agent = Agent(
    name="Folder Assistant",
    instructions="You create a new folder for the user based on the provided project name",
    functions=[create_project_folder],
)

print("Running manager Assistant for Weather...")

response = client.run(
    agent=manager_agent,
    messages=[{"role": "user",
               "content": "can u create me a react project folder with the name COOOLSHIT"}],
)
print(response.messages[-1]["content"])
