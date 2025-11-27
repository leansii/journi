import asyncio
import json
from google.genai import types
from nutrition.agent import nutrition_agent
from finance.agent import finance_agent
from health.agent import health_agent
from fitness.agent import fitness_agent

# Map of available agents
AGENTS = {
    "nutrition_specialist": nutrition_agent,
    "finance_specialist": finance_agent,
    "health_specialist": health_agent,
    "fitness_specialist": fitness_agent
}

async def run_parallel_agents(tasks: list[dict]) -> dict:
    """
    Executes multiple specialist agents in parallel and aggregates their results.
    
    Args:
        tasks: A list of dictionaries, where each dictionary has:
               - "agent_name": The name of the specialist agent (e.g., "nutrition_specialist")
               - "input": The text input for that agent.
               
    Returns:
        A dictionary containing the aggregated results from all agents.
        Keys are the agent names (shortened, e.g., "nutrition"), values are their JSON responses.
    """
    print(f"🚀 Starting parallel execution for {len(tasks)} tasks: {[t['agent_name'] for t in tasks]}")
    
    async def call_single_agent(agent_name: str, agent_input: str):
        agent = AGENTS.get(agent_name)
        if not agent:
            return agent_name, {"error": f"Agent '{agent_name}' not found."}
            
        print(f"▶️ Calling {agent_name}...")
        
        # We need to construct a proper user message for the agent
        # The ADK Runner usually handles this, but here we are calling the agent directly.
        # We'll use a simplified approach if possible, or we might need to create a temporary runner/session.
        # However, Agent.query() or similar might be available? 
        # Checking ADK docs/code implies we usually run via a Runner.
        # But we can also try to use the agent's model directly if we just want to pass the prompt + input.
        # WAIT: The agent object in ADK is high-level. 
        # Let's try to use the agent's internal logic if exposed, or create a mini-runner.
        
        # Actually, looking at main.py, we use `runner.run_async`.
        # We can instantiate a temporary runner for each sub-task.
        # This is expensive but safe.
        
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        
        session_service = InMemorySessionService()
        runner = Runner(agent=agent, app_name="journi", session_service=session_service)
        
        # Create a temp session
        session = await session_service.create_session(user_id="parallel_runner", app_name="journi")
        
        content = types.Content(role="user", parts=[types.Part(text=agent_input)])
        
        final_text = ""
        async for event in runner.run_async(
            user_id="parallel_runner", 
            session_id=session.id, 
            new_message=content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_text = event.content.parts[0].text
                break
                
        # Parse the JSON response
        try:
            # Clean markdown code blocks if present
            cleaned_text = final_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()
            
            return agent_name.replace("_specialist", ""), json.loads(cleaned_text)
        except Exception as e:
            print(f"⚠️ Failed to parse response from {agent_name}: {final_text}")
            return agent_name.replace("_specialist", ""), {"raw": final_text, "error": str(e)}

    # Create coroutines
    coroutines = []
    for task in tasks:
        agent_name = task.get("agent_name")
        agent_input = task.get("input")
        if agent_name and agent_input:
            coroutines.append(call_single_agent(agent_name, agent_input))
            
    # Run in parallel
    results = await asyncio.gather(*coroutines)
    
    # Aggregate results
    aggregated_data = {}
    for name, data in results:
        aggregated_data[name] = data
        
    print("✅ Parallel execution finished.")
    return aggregated_data
