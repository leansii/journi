from google.adk import Agent
from utils import load_prompt, GEMINI_2_5_FLASH

HEALTH_INSTRUCTION = load_prompt("health_prompt.txt")

''' Health Specialist Agent: Provides advice on general health and wellness.'''
root_agent = Agent(
    name="health_specialist",
    model=GEMINI_2_5_FLASH,
    instruction=HEALTH_INSTRUCTION
)

health_agent = root_agent