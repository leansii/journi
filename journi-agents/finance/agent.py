from google.adk import Agent
from utils import load_prompt, GEMINI_2_5_FLASH
from tools.firestore_tool import save_transactions

FINANCE_INSTRUCTION = load_prompt("finance_prompt.txt")

''' Finance Specialist Agent: Gives financial advice and planning tips.'''
root_agent = Agent(
    name="finance_specialist",
    model=GEMINI_2_5_FLASH,
    instruction=FINANCE_INSTRUCTION,
    tools=[save_transactions]
)

finance_agent = root_agent