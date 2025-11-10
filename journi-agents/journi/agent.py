from google.adk import Agent
from utils import load_prompt, GEMINI_2_5_FLASH
from health.agent import health_agent
from nutrition.agent import nutrition_agent
from fitness.agent import fitness_agent
from finance.agent import finance_agent

JOURNI_INSTRUCTION = load_prompt("router_prompt.txt")

''' Root Agent: Routes user queries to specialized agents based on content.'''
root_agent = Agent(
    name="journi_manager",
    model=GEMINI_2_5_FLASH,
    instruction=JOURNI_INSTRUCTION,
    sub_agents=[health_agent, nutrition_agent, fitness_agent, finance_agent]
)
