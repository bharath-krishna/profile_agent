"""Conversation Tracker Agent Definition."""

import os
from typing import Optional
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .tools import save_recruiter_info
from .prompts import get_instructions
from agent.sub_agents.models.agent_inputs import RecruitAgentInput, RecruitAgentOutput

# Configure model
use_litellm = os.getenv("USE_LITELLM", "false").lower() == "true"
model_name = os.getenv("MODEL_NAME", "gemini-2.5-flash")

if use_litellm:
    if model_name.startswith("gemini") and not model_name.startswith("gemini/"):
        litellm_model = f"gemini/{model_name}"
    else:
        litellm_model = model_name
    model = LiteLlm(model=litellm_model)
else:
    model = model_name


# Create the Conversation Note agent
recruit_agent = Agent(
    name="RecruitAgent",
    model=model,
    description="Specialized agent for saving conversation notes",
    instruction=get_instructions(),
    input_schema=RecruitAgentInput,
    output_schema=RecruitAgentInput,
    tools=[
        save_recruiter_info
    ]
)
