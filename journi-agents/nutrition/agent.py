from google.adk import Agent
from utils import load_prompt, GEMINI_2_5_FLASH
from tools.firestore_tool import save_meals

NUTRITION_INSTRUCTION = load_prompt("nutrition_prompt.txt")

''' Nutrition Specialist Agent: Offers dietary and nutrition guidance.'''
root_agent = Agent(
    name="nutrition_specialist", 
    model=GEMINI_2_5_FLASH, 
    instruction=NUTRITION_INSTRUCTION,
    tools=[save_meals]
)

nutrition_agent = root_agent