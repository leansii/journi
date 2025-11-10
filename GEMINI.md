# 🚀 Journi: The AI-Powered Agent Journal

"Journi" is an intelligent journal application built for the **Google Cloud Run Hackathon**. It uses a multi-agent AI system deployed on Cloud Run to automatically classify, process, and enrich journal entries in real-time.

A user writes a raw note (e.g., "Ate a salad (300 kcal) and need to go to the gym tomorrow"), and the "Journi" agents automatically categorize this as `nutrition` and `gtd`, extract the calories, and create a new task.

---

## 🛠️ Tech Stack

*   **Category:** 🤖 **AI Agents Category**
*   **Frontend:** **Vue.js**
*   **Backend API (Gateway):** **Python (FastAPI)**
*   **AI Agents:** **Python (FastAPI)** + **Google Agent Development Kit (ADK)**
*   **AI Model:** **Gemini Pro** (via Google AI)
*   **Database:** **Firestore** (for real-time updates)
*   **Authentication:** **Firebase Authentication**
*   **Deployment:**
    *   **Google Cloud Run** (for all 3 backend services)
    *   **Firebase Hosting** (for the Vue.js frontend)

---

## 🏗️ Architecture Diagrams

### 1. C4 Container Diagram

This diagram shows the main components of the system and their relationships.

```mermaid
%% C4 Container Diagram
C4Container
    title C4 Container Diagram for "Journi" (Full English)

    Person(user, "User", "Writes in the journal")

    System_Boundary(web, "Client Application") {
        Container(frontend, "Frontend (Vue.js)", "JavaScript", "Web UI for the journal. Deployed on Firebase Hosting.")
    }

    System_Boundary(gcp, "Google Cloud Platform (Serverless)") {
        Container(api_gw, "Backend API (FastAPI)", "Python", "Main API to receive entries. Deployed on Cloud Run.")
        Container(agent_router, "Agent: Router", "Python / ADK", "Classifies entries. Deployed on Cloud Run.")
        Container(agent_processor, "Agent: Processor", "Python / ADK", "Processes and enriches entries. Deployed on Cloud Run.")
        ContainerDb(db, "Database", "Firestore", "Stores journal entries,
        statuses, and processed data.")
    }

    System_Ext(auth, "Firebase Auth", "Manages user authentication.")
    System_Ext(gemini, "Gemini Pro API", "Model for classification and data extraction.")

    Rel(user, frontend, "Uses", "HTTPS")
    Rel(frontend, auth, "Authenticates via")
    Rel(frontend, api_gw, "Creates new entries", "HTTPS/JSON")
    Rel_Back(frontend, db, "Reads entries (real-time)", "Firestore SDK")
    
    Rel(api_gw, auth, "Validates token")
    Rel(api_gw, db, "Saves 'pending' entry")
    Rel(api_gw, agent_router, "Calls for classification", "HTTPS")
    
    Rel(agent_router, gemini, "Requests entry type")
    Rel(agent_router, agent_processor, "Passes task for processing", "HTTPS")
    Rel(agent_processor, gemini, "Requests data extraction")
    Rel(agent_processor, db, "Updates entry (status: 'processed')")
```

### 2. Sequence Diagram (Data Flow)

This diagram shows the real-time communication flow between the user, the API, and the AI agents.

```mermaid 
%% Sequence Diagram
sequenceDiagram
    participant User
    participant VueApp as Frontend (Vue.js)
    participant ApiGW as Backend API (FastAPI)
    participant AgentRouter as Agent: Router (ADK)
    participant AgentProc as Agent: Processor (ADK)
    participant Gemini as Gemini Pro API
    participant DB as Firestore

    User->>VueApp: 1. Enters text and clicks "Save"
    VueApp->>ApiGW: 2. POST /api/entries (text)
    ApiGW->>DB: 3. Save entry (status: 'pending')
    ApiGW->>AgentRouter: 4. POST /classify (entryId, text)
    
    activate AgentRouter
    AgentRouter->>Gemini: 5. Prompt: "Classify this"
    Gemini-->>AgentRouter: 6. Response: ['nutrition', 'gtd']
    AgentRouter->>AgentProc: 7. POST /process (entryId, text, types)
    deactivate AgentRouter
    
    activate AgentProc
    AgentProc->>Gemini: 8. Prompt: "Extract calories..."
    Gemini-->>AgentProc: 9. Response: {calories: 550}
    AgentProc->>Gemini: 10. Prompt: "Extract tasks..."
    Gemini-->>AgentProc: 11. Response: {tasks: [...]}
    AgentProc->>DB: 12. Update entry (status: 'processed', data)
    deactivate AgentProc
    
    DB-->>VueApp: 13. (Real-time update)
    VueApp->>User: 14. Display processed entry
```

---

## 📦 Services

### 1. `journi-client` (Frontend)

*   **Purpose:** The web interface for users to write and view journal entries.
*   **Framework:** Vue.js
*   **Key Dependencies:**
    *   `vue`: The core Vue.js framework.
    *   `vue-router`: For client-side routing.
    *   `pinia`: For state management.
    *   `vite`: For the build tooling.
    *   `tailwindcss`: For styling.

### 2. `journi-router` (Backend API)

*   **Purpose:** The main entry point for the backend. It receives new journal entries from the client, saves them to Firestore with a "pending" status, and triggers the agent workflow by calling `journi-agent-router`.
*   **Framework:** FastAPI (Python)
*   **Key Dependencies:**
    *   `fastapi`: The web framework.
    *   `uvicorn`: The ASGI server.
    *   `google-cloud-firestore`: To interact with the Firestore database.
    *   `httpx`: To make asynchronous requests to the agent services.
*   **Note:** This service appears to be missing from the project's file structure but is a critical part of the architecture. It is referred to as `journi-gateway` in other parts of the documentation.

### 3. `journi-agent-router` (AI Agent)

*   **Purpose:** This agent is responsible for classifying the incoming journal entry. It receives the text, calls the Gemini API to determine the categories (e.g., `nutrition`, `gtd`), and then forwards the request to the appropriate processing agent.
*   **Framework:** FastAPI (Python)
*   **Key Dependencies:**
    *   `fastapi`
    *   `uvicorn`
    *   `google-generativeai` (for Gemini)
    *   `httpx`

### 4. `journi-agent-processor` (AI Agent)

*   **Purpose:** This is the final agent in the chain. It receives the classified entry and performs the actual data extraction. Based on the categories, it calls the Gemini API with specific prompts to extract structured data (like calories, tasks, etc.). It then updates the entry in Firestore with the processed data and sets the status to "processed".
*   **Framework:** FastAPI (Python)
*   **Key Dependencies:**
    *   `fastapi`
    *   `uvicorn`
    *   `gunicorn`
    *   `google-generativeai` (for Gemini)
    *   `google-cloud-firestore`

---

## 🚀 Getting Started

### Prerequisites

*   Node.js (for the frontend)
*   Python 3.11+ (for the backend services)
*   `GEMINI_API_KEY` environment variable set with your Google AI API key.

### Frontend (`journi-client`)

```bash
# Navigate to the client directory
cd journi-client

# Install dependencies
npm install

# Run the development server
npm run dev
```

### Backend Services (`journi-gateway`, `journi-agent-processor`)

Each backend service is a standard FastAPI application and can be run locally using `uvicorn`.

```bash
# Navigate to the service directory (e.g., journi-gateway)
cd journi-gateway

# Install dependencies
pip install -r requirements.txt

# Run the service (example for gateway)
# You will need to set the AGENT_ROUTER_URL environment variable
export AGENT_ROUTER_URL="http://localhost:8081" # Or the deployed URL
uvicorn main:app --host 0.0.0.0 --port 8080
```

Deployment is handled via Docker and Google Cloud Run. Each service has its own `Dockerfile`.
