import os
import requests
from swarm import Swarm, Agent
from dotenv import load_dotenv
import subprocess

load_dotenv()

# Initialize Swarm client
client = Swarm()

# Load OpenWeatherMap API key from environment variable
API_KEY = os.getenv('OPENWEATHER_API_KEY')
if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY environment variable not set")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to create Folders

# Global arrays to store paths
paths = {
    "react_project": "C:\\Users\\ASUS\\OneDrive\\Desktop\\reactjs_prots",
    "python_project": "C:\\Users\\ASUS\\OneDrive\\Desktop\\Python_projects",
}


def create_project_folder(folder_name, prompt):
    # Determine the project type based on the folder name
    if 'react' in prompt.lower():
        project_type = 'react_project'
    elif 'python' in prompt.lower():
        project_type = 'python_project'
    else:
        raise ValueError(
            f"Unsupported project type for folder name: {folder_name}")

    # Create the new folder path
    location = paths[project_type]
    new_folder_path = os.path.join(location, folder_name)

    # Create the folder if it doesn't exist
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        return f"Created folder: {new_folder_path}"
    else:
        return f"Folder already exists: {new_folder_path}"

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


def open_youtube(search_query):
    print(f"Running YouTube function for {search_query}...")

    try:
        opera_path = "C:\\Users\\ASUS\\AppData\\Local\\Programs\\Opera GX\\opera.exe"
        url = f"https://www.youtube.com/results?search_query={'+'.join(search_query.split())}"
        subprocess.Popen([opera_path, url])
        return "Opened YouTube in Opera GX."
    except Exception as e:
        return f"Failed to open YouTube: {str(e)}"


def transfer_to_youtube_assistant():
    print("Transferring to YouTube Assistant...")
    return youtube_agent


def transfer_to_weather_assistant():
    print("Transferring to Weather Assistant...")
    return weather_agent


def transfer_to_folder_assistant():
    print("Transferring to Folder Assistant...")
    return folder_agent


# Manager Agent
manager_agent = Agent(
    name="manager Assistant",
    instructions="You help users by directing them to the right assistant.",
    functions=[transfer_to_weather_assistant,
               transfer_to_folder_assistant, transfer_to_youtube_assistant],
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

# YouTube Agent
youtube_agent = Agent(
    name="YouTube Assistant",
    instructions="You open YouTube and search for the user's query using Opera GX.",
    functions=[open_youtube],
)

query = input("Enter your query: ")
response = client.run(
    model_override="gpt-4o-mini",
    agent=manager_agent,
    messages=[{"role": "user",
               "content": query}],

)
print(response.messages[-1]["content"])
