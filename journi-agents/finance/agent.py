from google.adk import Agent
from utils import load_prompt, GEMINI_2_5_FLASH

FINANCE_INSTRUCTION = load_prompt("finance_prompt.txt")

''' Finance Specialist Agent: Gives financial advice and planning tips.'''
root_agent = Agent(
    name="finance_specialist",
    model=GEMINI_2_5_FLASH,
    instruction=FINANCE_INSTRUCTION
)

finance_agent = root_agent