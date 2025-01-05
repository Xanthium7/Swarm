import os
import requests
from swarm import Swarm, Agent
from dotenv import load_dotenv
import subprocess
import time
import pyautogui

load_dotenv()

# Initialize Swarm client
client = Swarm()

# Load OpenWeatherMap API key from environment variable
API_KEY = os.getenv('OPENWEATHER_API_KEY')
if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY environment variable not set")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


APP_PATHS = {
    "opera": "C:\\Users\\ASUS\\AppData\\Local\\Programs\\Opera GX\\opera.exe",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "spotify": "C:\\Users\\ASUS\\AppData\\Roaming\\Spotify\\Spotify.exe",
    "vscode": "C:\\Users\\ASUS\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "notepad": "C:\\Windows\\System32\\notepad.exe",
    "whatsapp": "C:\\Program Files\\WindowsApps\\5319275A.WhatsAppDesktop_2.2450.6.0_x64__cv1g1gvanyjgm\\WhatsApp.exe",
    "appflowy": "C:\\Program Files (x86)\\AppFlowy\\AppFlowy.exe",
    "discord": "C:\\Users\\ASUS\\AppData\\Local\\Discord\\Update.exe",
}

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


def openApp(appName):
    print(f"Opening {appName}...")
    try:
        subprocess.Popen(APP_PATHS[appName])
        return f"Opened {appName}."
    except Exception as e:
        return f"Failed to open {appName}: {str(e)}"


def look_up_information(query):
    print(f"Looking up information for {query}...")
    try:

        opera_path = "C:\\Users\\ASUS\\AppData\\Local\\Programs\\Opera GX\\opera.exe"
        url = "https://www.perplexity.ai"
        subprocess.Popen([opera_path, url])

        # Wait for the page to load
        time.sleep(3)

        pyautogui.write(query)
        pyautogui.press('enter')
        print("Typed the query in Perplexity search bar.")

    except Exception as e:
        return f"Failed to open Perplexity: {str(e)}"


def transfer_to_youtube_assistant():
    print("Transferring to YouTube Assistant...")
    return youtube_agent


def transfer_to_weather_assistant():
    print("Transferring to Weather Assistant...")
    return weather_agent


def transfer_to_folder_assistant():
    print("Transferring to Folder Assistant...")
    return folder_agent


def transfer_to_app_assistant():
    print("Transferring to App Assistant...")
    return app_agent


def transfer_to_look_up_information_assistant():
    print("Transferring to Look Up Information Assistant...")
    return look_up_information_agent


# Manager Agent
manager_agent = Agent(
    name="manager Assistant",
    instructions="You help users by directing them to the right assistant.",
    functions=[transfer_to_weather_assistant,
               transfer_to_folder_assistant, transfer_to_youtube_assistant, transfer_to_app_assistant, transfer_to_look_up_information_assistant],
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

app_agent = Agent(
    name="App Assistant",
    instructions='''
    You are the App Assistant. Your role is to open applications based on the user's request.
    
    - When the user mentions "Opera GX", "Opera Browser", or "Opera", interpret the app name as "opera".
    - When the user mentions "Google Chrome", "Chrome", or "Google", interpret the app name as "chrome".
    - When the user mentions "Spotify", interpret the app name as "spotify".
    - When the user mentions "Visual Studio Code", "VSCode", or "Code", interpret the app name as "vscode".
    - When the user mentions "Notepad", interpret the app name as "notepad".
    - When the user mentions "WhatsApp", interpret the app name as "whatsapp".
    - When the user mentions "AppFlowy", interpret the app name as "appflowy".
    
    After standardizing the app name, use the openApp function to open the corresponding application.
    
    If the app name does not match any known applications, respond with "Unsupported app name."
    ''',
    functions=[openApp],
)


look_up_information_agent = Agent(
    name="Look Up Information Assistant",
    instructions='''
    You are the Look Up Information Assistant. Your role is to assist users by searching for information on Perplexity AI based on their queries.
    You must identify the user's query from the message they give you. If the query is unclear u may assume user said ' '.
    You are also capable of opening Perplexity AI in Opera GX. (in this case user query is ' ')

    - When a user requests information or asks a question related to a topic, use the `look_up_information` function to perform the search on Perplexity AI.
    - Ensure that the search query is accurately captured and passed to the `look_up_information` function.
    - After initiating the search, inform the user that the search has been performed.
    
    Example Interactions:
    - User: "Can you find information about machine learning ?"
      Assistant: "Looking up information on Perplexity AI for 'machine learning'..."
    - User: "Search for the latest news on artificial intelligence."
      Assistant: "Looking up information on Perplexity AI for 'the latest news on artificial intelligence'..."
    ''',
    functions=[look_up_information],
)

while True:

    query = input("Enter your query: ")
    if query.lower() == "exit":
        break
    response = client.run(
        model_override="gpt-4o-mini",
        agent=manager_agent,
        messages=[{"role": "user",
                   "content": query}],

    )
    print(response.messages[-1]["content"])
