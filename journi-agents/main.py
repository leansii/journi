import asyncio
import json
import re
from fastapi import FastAPI
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from journi.agent import root_agent

from tools.firestore_tool import create_initial_note, update_note_with_results



APP_NAME = "agents"



# Initialize FastAPI app

app = FastAPI(

    title="Journi Agents API",

    description="API for processing journal entries with AI agents.",

    version="0.1.0",

)



# --- Agent Setup ---

# Re-usable services for the agent runner

session_service = InMemorySessionService()

runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)





# --- Pydantic Models ---

class ProcessRequest(BaseModel):

    text: str

    user_id: str = "demo_user_123"  # Default user for now

    session_id: str | None = None





class ProcessResponse(BaseModel):

    session_id: str

    note_id: str

    agent_response: dict | str





# --- Helper Functions ---

def clean_json_string(s: str) -> str:

    """Removes markdown code blocks and trims whitespace from a string."""

    if isinstance(s, str):

        match = re.search(r"```(json)?\s*(\{.*\}|\[.*\])\s*```", s, re.DOTALL)

        if match:

            return match.group(2).strip()

    return s



async def call_agent_async(query: str, runner: Runner, user_id: str, session_id: str) -> str:

    """Sends a query to the agent and returns the final response text."""

    content = types.Content(role="user", parts=[types.Part(text=query)])



    final_response_text = "Agent did not produce a final response."



    async for event in runner.run_async(

        user_id=user_id, session_id=session_id, new_message=content

    ):

        if event.is_final_response():

            if event.content and event.content.parts:

                final_response_text = event.content.parts[0].text

            elif event.actions and event.actions.escalate:

                final_response_text = (

                    f"Agent escalated: {event.error_message or 'No details.'}"

                )

            break

    return final_response_text





# --- API Endpoints ---

@app.post("/process", response_model=ProcessResponse)

async def process_note(request: ProcessRequest):

    """

    Processes a user's journal entry by routing it to the appropriate AI agent.

    """

    session_id = request.session_id

    if not session_id:

        # Create a new session if one isn't provided

        session = await session_service.create_session(

            user_id=request.user_id, app_name=APP_NAME

        )

        session_id = session.id



    # 1. Create initial note to get an ID

    note_id = create_initial_note(request.text, request.user_id)



    # 2. Format the query for the agent, including the note_id

    agent_query = f"note_id: {note_id}\ntext: {request.text}"



    # 3. Call the root agent to orchestrate processing

    response_text = await call_agent_async(

        query=agent_query,

        runner=runner,

        user_id=request.user_id,

        session_id=session_id,

    )



    # 4. Clean and parse the agent's final response

    cleaned_response = clean_json_string(response_text)

    try:

        response_data = json.loads(cleaned_response)

        category = response_data.get("category", "UNKNOWN")

        # 5. Update the note with the final aggregated data

        update_note_with_results(note_id, category, response_data)

    except (json.JSONDecodeError, TypeError):

        response_data = cleaned_response

        print(f"⚠️ Could not parse agent response for note {note_id}. Saving raw response.")

        update_note_with_results(note_id, "ERROR", {"raw_response": response_data})





    return {

        "session_id": session_id, 

        "note_id": note_id,

        "agent_response": response_data,

    }





@app.get("/")

def read_root():

    """A simple endpoint to confirm the server is running."""

    return {"message": "Journi Agents API is running."}
