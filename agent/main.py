"""Shared State feature."""

from __future__ import annotations

import json
import time
from typing import Dict, Optional

from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import litellm
from google.adk.agents import LlmAgent, Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import ToolContext
from google.genai import types
from pydantic import BaseModel, Field

from langfuse import get_client
from openinference.instrumentation.google_adk import GoogleADKInstrumentor

load_dotenv()


class ProfileState(BaseModel):
    """State for Bharath's personal assistant agent."""

    conversation_context: list[str] = Field(
        default_factory=list,
        description="Notes from conversations with recruiters",
    )
    last_thinking_content: Optional[str] = Field(
        default=None,
        description="Thinking content from the last agent response",
    )
    final_response: Optional[str] = Field(
        default=None,
        description="Final response text from the last agent response",
    )
    last_response_id: Optional[str] = Field(
        default=None,
        description="Message ID of the last response (for correlation)",
    )


def add_conversation_note(
    tool_context: ToolContext,
    note: str,
    source: str = "Unknown"
) -> Dict[str, str]:
    """
    Add a note about the current conversation for future reference.
    Writes to individual files with timestamp in agent/notes/ directory.

    Use this to track:
    - Key recruiter questions or concerns
    - Specific job requirements discussed
    - Follow-up items or next steps
    - Important discussion points

    Args:
        note: A concise note about the conversation
        source: The name of the person (e.g., recruiter) or source of the note

    Returns:
        Dict indicating success and the note added
    """
    try:
        from datetime import datetime
        import os
        
        # Ensure notes directory exists
        notes_dir = os.path.join(os.environ.get("NOTES_DIR", os.path.dirname(os.path.abspath(__file__))), "notes")
        os.makedirs(notes_dir, exist_ok=True)
        
        # Generate timestamp and filename
        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y-%m-%d")
        time_str = timestamp.strftime("%H-%M-%S")
        filename = f"{date_str}_{time_str}_note.md"
        filepath = os.path.join(notes_dir, filename)
        
        # Create note content with timestamp
        note_content = f"# Conversation Note\n\n## {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n{note}\n \n*Source: {source}*"
        
        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(note_content)
        
        # Also add to context list for the agent
        context_list = tool_context.state.get("conversation_context", [])
        if context_list is None:
            context_list = []
        
        timestamped_note = f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {note}"
        context_list.append(timestamped_note)
        
        tool_context.state["conversation_context"] = context_list
        
        return {
            "status": "success",
            "message": f"Note added: {note}",
            "filepath": filepath
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error adding note: {str(e)}"
        }


# def get_weather(tool_context: ToolContext, location: str) -> Dict[str, str]:
#     """Get the weather for a given location. Ensure location is fully spelled out."""
#     return {"status": "success", "message": f"The weather in {location} is sunny."}

# def get_person_card(
#     tool_context: ToolContext,
#     firstName: str,
#     lastName: str,
#     name: str,
#     age: int,
#     gender: str,
#     email: str,
#     relationship: str,
#     exploration_depth: int,
#     is_complete: bool,
#     last_updated: str,
# ) -> Dict:
#     """
#     Get details about a person from the family tree.

#     Args:
#         firstName: Person's first name
#         lastName: Person's last name
#         name: Full name of the person
#         age: Person's age
#         gender: Person's gender
#         email: Person's email address
#         relationship: Relationship type (e.g., FATHER_OF, MOTHER_OF)
#         exploration_depth: Depth of exploration in the family tree
#         is_complete: Whether the person's data is complete
#         last_updated: Last update timestamp

#     Returns:
#         Dictionary with person details
#     """
#     return {
#         "firstName": firstName,
#         "lastName": lastName,
#         "name": name,
#         "age": age,
#         "gender": gender,
#         "email": email,
#         "relationship": relationship,
#         "exploration_depth": exploration_depth,
#         "is_complete": is_complete,
#         "last_updated": last_updated,
#     }


def on_before_agent(callback_context: CallbackContext):
    """Initialize conversation context and thinking fields if they don't exist."""

    if "conversation_context" not in callback_context.state:
        callback_context.state["conversation_context"] = []

    # Initialize thinking fields
    if "last_thinking_content" not in callback_context.state:
        callback_context.state["last_thinking_content"] = None

    if "final_response" not in callback_context.state:
        callback_context.state["final_response"] = None

    if "last_response_id" not in callback_context.state:
        callback_context.state["last_response_id"] = None

    return None


# --- Define the Callback Function ---
#  modifying the agent's system prompt to include Bharath's complete profile
def before_model_modifier(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Inspects/modifies the LLM request or skips the call."""
    agent_name = callback_context.agent_name
    if agent_name == "BharathAssistant":
        # Build conversation notes
        conversation_notes = "No conversation notes yet"
        if (
            "conversation_context" in callback_context.state
            and callback_context.state["conversation_context"] is not None
        ):
            try:
                conversation_notes = json.dumps(callback_context.state["conversation_context"], indent=2)
            except Exception as e:
                conversation_notes = f"Error serializing notes: {str(e)}"

        # Build comprehensive profile context
        profile_context = f"""# BHARATH KRISHNA - PROFESSIONAL PROFILE

## Contact Information
- Phones: +1 8574379316, +91 7760779000
- Email: bharath.chakravarthi@gmail.com
- Website: https://profile.krishb.in

## Professional Summary
Full-stack engineer with 15 years of professional experience (2010-2025). Proven expertise in building scalable AI/ML platforms, high-availability services, and DevOps pipelines. Strong background in designing LLM inference pipelines, managing Kubernetes clusters, and automating infrastructure with Terraform & Ansible. Deep knowledge of Python (15 years) and Go (7 years).

## Work Experience (Detailed Timeline)

### 1. Senior Software Engineer – Rakuten USA, California (May 2022 – Present)
- Build AgenticAI solutions for internal services
- Manage LLM deployments for peak usage
- Develop UI, API & CLI tools for submitting training jobs on HPC clusters
- Setup MLOps pipeline for model development & deployment
- Maintain high-performance Kubernetes cluster
- Implemented model inference platform using BentoML
- Configured IAM via Keycloak
- Automated infrastructure with Terraform & Ansible
- Configured DNS & Load Balancer for HPC services
- Developed custom K8s operators
- Led UI developers & infrastructure engineers
- Tech Stack: Golang, Python, Kubernetes, Ansible, Terraform, Graph DBs, AgenticAI

### 2. Application Engineer – Rakuten, Inc., Tokyo (Jan 2018 – May 2022)
- Built Infrastructure as Code with Terraform & Ansible
- Extended Terraform with custom plugins & Go SDKs
- Wrote pytest & Locust tests for service stability
- Created toolkit for building/testing/deploying REST APIs (FastAPI, Gin)
- Implemented auth services using Keycloak & Kong
- Tech Stack: Golang, Python, Kubernetes, Ansible, Terraform, Graph DBs, AgenticAI

### 3. Application Engineer – Rakuten India Enterprise Pvt. Ltd., Bengaluru (Sep 2014 – Dec 2018)
- Built APIs for IaaS (VMware vSphere), DNS (Nominum, Infoblox) & Load Balancer (BigIP)
- Developed batch scripts & daily Airflow jobs for auth data collection
- Led a team of 3; acted as Scrum Master
- Collaborated across teams for requirement gathering & service improvement
- Tech Stack: Python, Ansible

### 4. Associate IT Consultant – ITC Infotech & Robert Bosch, Bengaluru (Jan 2014 – Sep 2014)
- Supported source-code management hotline (MKS, ClearQuest)
- Automated support tasks with Perl scripts
- Tech Stack: Perl

### 5. Software Engineer – eHover Systems India Pvt. Ltd. (Apr 2011 – Apr 2013)
- Developed secure cloud-based personal surveillance system (EC2, S3)
- Created web interface (PHP, CodeIgniter) for CCTV data access
- Tech Stack: Perl, PHP, AWS (S3, Route53, EC2), ZoneMinder

### 6. Project Assistant – Kuvempu University (Sep 2010 – Feb 2011)
- Developed Perl modules for automated molecular-dynamic simulations
- Built web app (Python, libSBML) to analyze SBML files
- Tech Stack: BioPython, BioPerl, LibSBML, Gromacs

### 7. Intern – Software Developer – IBAB, Bengaluru (Apr 2010 – Feb 2011)
- Built "Mammalian Gene Expression Database"
- Developed web app (PERL, MySQL, JavaScript) for bio-curator data maintenance
- Tech Stack: Perl, MySQL, JavaScript

## Technical Skills (8 Categories)

### Languages & Web
- Python (15 years experience)
- Go (7 years experience)

### Frontend
- React
- NextJS
- Chakra UI

### ML Frameworks
- ONNX
- PyTorch
- TensorRT
- NVIDIA Triton
- DeepSpeed
- Accelerate

### Infrastructure
- Ansible
- Terraform

### Frameworks
- FastAPI
- Gin Gonic

### Databases
- PostgreSQL
- MongoDB
- Couchbase

### CI/CD & Build
- Jenkins
- GitHub Actions

### Cloud & Orchestration
- Kubernetes (7 years experience)
- GCP

## Certifications & Recognitions
- Certified Kubernetes Administrator (CKA) – Linux Foundation

## Education
- Bachelor's degree in Biotechnology – Kuvempu University, Karnataka (Majors: Biotechnology, Botany, Computer Science)
- Master's in Bioinformatics – Kuvempu University, Karnataka (Focus: Genomics, Drug Discovery, Protein Engineering)

## Personal Profile
- Age: 38 years
- Date of Birth: 28/10/1987
- Gender: Male
- Nationality: Indian
- Languages Known: Kannada, English, Hindi, Telugu
- Hobbies & Interests: Gardening and movies

## Key Strengths
- DevOps & LLM-Ops engineering
- Deep knowledge of Python (15 years) & Go (7 years)
- Backend service development (RESTful APIs)
- Front-end development with React, NextJS, Chakra UI
- Cloud services (GCP) & container orchestration
- Agile-Scrum methodology
- Quick learner, self-starter, team player

## Conversation Notes
{conversation_notes}

---
You are Bharath's Personal Assistant. Use this profile information to answer questions about Bharath's background, experience, and skills. When discussing with recruiters, advocate on his behalf by highlighting relevant achievements and experience."""

        # Add profile context to system instruction
        original_instruction = llm_request.config.system_instruction or types.Content(
            role="system", parts=[]
        )

        # Ensure system_instruction is Content and parts list exists
        if not isinstance(original_instruction, types.Content):
            original_instruction = types.Content(
                role="system", parts=[types.Part(text=str(original_instruction))]
            )
        if not original_instruction.parts:
            original_instruction.parts = [types.Part(text="")]

        # Modify the text of the first part
        if original_instruction.parts and len(original_instruction.parts) > 0:
            modified_text = profile_context + "\n\n" + (original_instruction.parts[0].text or "")
            original_instruction.parts[0].text = modified_text

        # TODO: Check model type to set system_instruction appropriately

        # For litellm models, we need to set it as string
        llm_request.config.system_instruction = original_instruction.parts[0].text
        # for Gemini models, we need to set it as Content
        # llm_request.config.system_instruction = original_instruction

    # Store start time for metrics
    callback_context.state["_last_request_start"] = time.time()

    return None

FINAL_RESPONSE = []

# --- Define the Callback Function ---
def simple_after_model_modifier(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """Stop the consecutive tool calling of the agent"""
    agent_name = callback_context.agent_name
    # --- Inspection ---
    if agent_name == "BharathAssistant":
        if llm_response.content and llm_response.content.parts:
            # Assuming simple text response for this example
            # print("LLM Response Text in after model modifier:", llm_response.content)
            if llm_response.finish_reason and llm_response.finish_reason.name == "STOP":
                callback_context._invocation_context.end_invocation = True
                
                # Calculate metrics
                start_time = callback_context.state.get("_last_request_start", 0)
                end_time = time.time()
                duration = end_time - start_time
                
                # if "</think>" in llm_response.content.parts[-1].text:
                #     thinking = llm_response.content.parts[-1].text.split("</think>")[0]
                #     text = llm_response.content.parts[-1].text.split("</think>")[-1]
                # else:
                #     text = llm_response.content.parts[-1].text
                # print("Final extracted text:", text)
                # llm_response.content.parts[-1].text = text
                # callback_context.state['last_thinking_content'] = thinking if 'thinking' in locals() else None
                # callback_context.state['final_response'] = text

                usage = llm_response.usage_metadata
                prompt_tokens = usage.prompt_token_count if usage else 0
                response_tokens = usage.candidates_token_count if usage else 0
                total_turn_tokens = usage.total_token_count if usage else 0
                
                tps = 0.0
                if duration > 0 and response_tokens > 0:
                    tps = response_tokens / duration

                # Update state
                total_token_count = callback_context.state.get('total_token_count', 0)
                callback_context.state['total_token_count'] = total_token_count + total_turn_tokens
                callback_context.state['last_context_tokens'] = prompt_tokens
                callback_context.state['last_response_tokens'] = response_tokens
                callback_context.state['tokens_per_second'] = round(tps, 2)

                # final_response = "".join(FINAL_RESPONSE)
                # FINAL_RESPONSE = []
                # llm_response.content.parts[0].text = final_response
            else:
                llm_response.content.parts[0].text = ""  # Clear intermediate responses
                return None

            # if (
            #     llm_response.content.role == "model"
            #     and llm_response.content.parts[0].text
            # ):
            #     callback_context._invocation_context.end_invocation = True

        elif llm_response.error_message:
            return None
        else:
            return None  # Nothing to modify
    return None

# from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
# from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH

# familyman_agent = RemoteA2aAgent(
#     name="familyman",
#     description="Familyman AI agent for managing family tasks and other activities. Has many sub agents and tools for different tasks.",
#     agent_card=(
#         f"http://localhost:8003/{AGENT_CARD_WELL_KNOWN_PATH}"
#     ),
# )
# from google.adk.tools import google_search, agent_tool


import os

# Configure model based on USE_LITELLM setting
use_litellm = os.getenv("USE_LITELLM", "false").lower() == "true"
model_name = os.getenv("MODEL_NAME", "gemini-2.5-pro")

if use_litellm:
    # Use LiteLLM for multi-model support (google_search won't work)
    if model_name.startswith("gemini") and not model_name.startswith("gemini/"):
        litellm_model = f"gemini/{model_name}"
    else:
        litellm_model = model_name
    model = LiteLlm(model=litellm_model)
    print(f"Using LiteLLM with model: {litellm_model}")
else:
    # Use native Gemini model (required for google_search tool)
    model = model_name
    print(f"Using native Gemini model: {model_name}")




from google.adk.planners import BuiltInPlanner



familyman_agent = Agent(
    name="BharathAssistant",
    # model="gemini-2.5-flash",
    model=model,
    description="Bharath's Personal Assistant Agent",
    instruction="""You are Bharath's Personal Assistant.

Your role:
- Answer questions about Bharath's professional background, experience, and skills
- Advocate on his behalf to recruiters and hiring managers
- Be professional, accurate, and conversational
- Highlight relevant experience based on context
- Provide specific details (dates, company names, technologies, achievements)

When asked about something not in the profile, politely indicate it's not available.

Use the add_conversation_note tool to track important points from discussions with recruiters, such as:
- Key questions or concerns raised
- Specific job requirements discussed
- Follow-up items or next steps
- Areas of particular interest

IMPORTANT RULES ABOUT WEATHER AND THE GET_WEATHER TOOL:
1. Only call the get_weather tool if the user asks you for the weather in a given location.
2. If the user does not specify a location, you can use the location "Everywhere ever in the whole wide world"

Examples of when to use the get_weather tool:
- "What's the weather today in Tokyo?" → Use the tool with the location "Tokyo"
- "Whats the weather right now" → Use the location "Everywhere ever in the whole wide world"
- "Is it raining in London?" → Use the tool with the location "London"
Keep your responses short and professional, likve a conversation. With in three sentences maximum.
""",
    tools=[
        add_conversation_note,
        # get_weather,
        # get_person_card
    ],
    before_agent_callback=on_before_agent,
    before_model_callback=before_model_modifier,
    after_model_callback=simple_after_model_modifier,
    # sub_agents=[familyman_agent],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=False,  # capture intermediate reasoning
            thinking_budget=0        # tokens allocated for planning
        )
    )
)

# Create ADK middleware agent instance
adk_familyman_agent = ADKAgent(
    adk_agent=familyman_agent,
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True,
)

# Create FastAPI app
app = FastAPI(title="FamilyMan Agent API")


# --- Exception Handlers ---
@app.exception_handler(litellm.exceptions.ServiceUnavailableError)
async def litellm_service_unavailable_handler(request: Request, exc: litellm.exceptions.ServiceUnavailableError):
    """Handle LLM service unavailable errors."""
    return JSONResponse(
        status_code=503,
        content={
            "error": "LLM Service Unavailable",
            "message": "The AI model service is currently unavailable. Please try again in a few moments.",
            "details": "The backend LLM server (vLLM) may be down or restarting.",
            "retry": True
        }
    )


@app.exception_handler(litellm.exceptions.APIConnectionError)
async def litellm_connection_error_handler(request: Request, exc: litellm.exceptions.APIConnectionError):
    """Handle LLM connection errors."""
    return JSONResponse(
        status_code=503,
        content={
            "error": "LLM Connection Error",
            "message": "Cannot connect to the AI model service. Please try again later.",
            "details": str(exc),
            "retry": True
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle any unhandled exceptions gracefully."""
    error_type = type(exc).__name__
    # Check if it's a LiteLLM-related error
    if "litellm" in str(type(exc).__module__).lower() or "ServiceUnavailable" in error_type:
        return JSONResponse(
            status_code=503,
            content={
                "error": "AI Service Error",
                "message": "The AI service encountered an error. Please try again.",
                "details": str(exc)[:200],  # Truncate for safety
                "retry": True
            }
        )
    # Re-raise other exceptions
    raise exc


# --- Health Check Endpoint ---
@app.get("/health")
async def health_check():
    """Check if the agent and LLM service are healthy."""
    health_status = {
        "agent": "ok",
        "llm": "unknown"
    }
    
    # Quick LLM connectivity check
    try:
        if use_litellm:
            # Try a minimal completion to check connectivity
            response = await litellm.acompletion(
                model=litellm_model if 'litellm_model' in dir() else model_name,
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=1,
                timeout=5
            )
            health_status["llm"] = "ok"
        else:
            health_status["llm"] = "native_gemini"
    except Exception as e:
        health_status["llm"] = f"error: {str(e)[:100]}"
        
    return health_status


# Add the ADK endpoint
add_adk_fastapi_endpoint(app, adk_familyman_agent, path="/")


# Initialize Langfuse
langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

# Instrument with Google ADK
GoogleADKInstrumentor().instrument()


# make sure to start opik
# cd /home/bharath/workspace/opik
# ./opik.sh
# http://localhost:5173

from opik.integrations.adk import OpikTracer, track_adk_agent_recursive

# Configure Opik tracer
opik_tracer = OpikTracer(
    name="profile_agent_tracing",
    tags=["ProfileAgent", "agent", "google-adk"],
    metadata={
        "environment": "development",
        "model": os.environ.get("MODEL_NAME", "gemini-2.5-pro"),
        "framework": "google-adk",
        "example": "basic"
    },
    project_name="PrfileAgentTracing"
)
# Instrument the agent with a single function call - this is the recommended approach   
track_adk_agent_recursive(familyman_agent, opik_tracer)


if __name__ == "__main__":
    import os

    import uvicorn

    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY environment variable not set!")
        print("   Set it with: export GOOGLE_API_KEY='your-key-here'")
        print("   Get a key from: https://makersuite.google.com/app/apikey")
        print()

    port = int(os.getenv("PYTHON_PORT", os.getenv("PORT", 8001)))
    uvicorn.run(app, host="0.0.0.0", port=port)
