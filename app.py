import datetime

import requests
import pytz
import yaml

from smolagents import (
    CodeAgent,
    DuckDuckGoSearchTool,
    VisitWebpageTool,
    HfApiModel,
    load_tool,
    tool,
)

from tools.final_answer import FinalAnswerTool
from Gradio_UI import GradioUI


# Below is an example of a tool that does nothing. Amaze us with your creativity!
@tool
def my_custom_tool(arg1: str, arg2: int) -> str:  # it's important to specify the return type
    """A tool that does nothing yet.

    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build?"


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.

    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


@tool
def get_weather(latitude: float, longitude: float) -> str:
    """Get current weather at a coordinate.

    Args:
        latitude: Latitude in decimal degrees.
        longitude: Longitude in decimal degrees.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": latitude, "longitude": longitude, "current": "temperature_2m,wind_speed_10m"}
    r = requests.get(url, params=params, timeout=10)  # short timeout, agents are chatty
    r.raise_for_status()
    d = r.json()["current"]
    return f"{d['temperature_2m']}°C, wind {d['wind_speed_10m']} km/h"


final_answer = FinalAnswerTool()
search_tool = DuckDuckGoSearchTool()
visit_webpage_tool = VisitWebpageTool()

model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    custom_role_conversions=None,
)

image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", "r") as stream:
    prompt_templates = yaml.safe_load(stream)

agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        search_tool,
        visit_webpage_tool,
        get_current_time_in_timezone,
        get_weather,
        image_generation_tool,
        my_custom_tool,
    ],
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates,
)

GradioUI(agent).launch()
