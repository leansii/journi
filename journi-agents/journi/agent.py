from google.adk import Agent
from utils import load_prompt, GEMINI_2_5_FLASH
from journi.tools import run_parallel_agents

JOURNI_INSTRUCTION = load_prompt("router_prompt.txt")

''' Root Agent: Routes user queries to specialized agents based on content.'''
root_agent = Agent(
    name="journi_manager",
    model=GEMINI_2_5_FLASH,
    instruction=JOURNI_INSTRUCTION,
    tools=[run_parallel_agents]
)
