import os
import requests
from swarm import Swarm, Agent
from dotenv import load_dotenv

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

# stream = client.run(
#     agent=manager_agent,
#     messages=[{"role": "user",
#                "content": "can u create me a python project folder with the name COOOLSHIT"}],
#     stream=True,
# )
# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")
response = client.run(
    agent=manager_agent,
    messages=[{"role": "user",
               "content": "can u create me a python project folder with the name COOOLSHIT"}],

)
print(response.messages[-1]["content"])
