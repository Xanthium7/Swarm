# Swarm Testing Project

This project demonstrates the use of the Swarm library to create agents that can interact with users and provide weather information using the OpenWeatherMap API.

## Prerequisites

- Python 3.x
- `requests` library
- `swarm` library
- `python-dotenv` library
- OpenWeatherMap API key

## Setup

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a `.env` file in the project directory and add your OpenWeatherMap API key:
    ```
    OPENWEATHER_API_KEY=your_api_key_here
    ```
4. Install the required libraries:
    ```bash
    pip install requests swarm python-dotenv
    ```

## Usage

Run the script to start the manager agent, which will direct you to the weather assistant for weather information.

```bash
python your_script_name.py
```

## Code Overview

The script initializes a Swarm client and defines two agents: a manager agent and a weather agent. The manager agent directs users to the weather agent, which fetches real-time weather data from the OpenWeatherMap API.

### Key Functions

- `get_weather(location)`: Fetches weather data for the specified location.
- `create_project_folder(folderName, prompt)`: Created a new folder at your system based on the instruction
- `transfer_to_weather_assistant()`: Transfers the user to the weather assistant.

### Example

```python
response = client.run(
    agent=manager_agent,
    messages=[{"role": "user", "content": "What's the weather in Kochi?"}],
)
print(response.messages[-1]["content"])
```

## Output
Running manager Assistant for Weather...
Transferring to Weather Assistant...
Running weather function for Kochi...
The current weather in Kochi is 25.99°C with overcast clouds.

## License

This project is licensed under the MIT License.
























































