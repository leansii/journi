from journi.agent import root_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio

APP_NAME = 'agents'

async def call_agent_async(query: str, runner: Runner, user_id, session_id):
    """Sends a query to the agent and prints the final response."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    """ default response """
    final_response_text = "Agent didn't produce a final response."
    
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent chose to escalate the query. {event.error_message or 'No error message provided.'}"
            break    
        
async def run_conversation():
    user_id = "user_123"
    query = "Spent $50 on groceries and $20 on lunch. Had chicken breast for lunch. Felt nauseous in the evening."
    session_service = InMemorySessionService()
    session = await session_service.create_session(user_id=user_id, app_name=APP_NAME)
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    
    await call_agent_async(query, runner, user_id, session_id=session.id)
    
if __name__ == "__main__":
    try:
        asyncio.run(run_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")