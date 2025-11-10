from google.adk import Agent
from utils import load_prompt, GEMINI_2_5_FLASH
from tools.firestore_tool import save_workouts

FITNESS_INSTRUCTION = load_prompt("fitness_prompt.txt")

''' Fitness Specialist Agent: Delivers fitness and exercise recommendations.'''
root_agent = Agent(
    name="fitness_specialist",
    model=GEMINI_2_5_FLASH,
    instruction=FITNESS_INSTRUCTION,
    tools=[save_workouts]
)

fitness_agent = root_agent