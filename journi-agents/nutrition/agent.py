from google.adk import Agent
from utils import load_prompt, GEMINI_2_5_FLASH

NUTRITION_INSTRUCTION = load_prompt("router_prompt.txt")

''' Nutrition Specialist Agent: Offers dietary and nutrition guidance.'''
root_agent = Agent(
    name="nutrition_specialist", 
    model=GEMINI_2_5_FLASH, 
    instruction=NUTRITION_INSTRUCTION
)

nutrition_agent = root_agent