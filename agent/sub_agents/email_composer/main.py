"""Email Composer Agent Definition."""

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .tools import generate_profile_pdf, send_email_with_attachment
from .prompts import get_email_composer_instructions


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


# Create the Email Composer agent
email_composer_agent = Agent(
    name="EmailComposer",
    model=model,
    description="Specialized agent for generating profile PDFs and sending emails",
    instruction=get_email_composer_instructions(),
    tools=[
        generate_profile_pdf,
        send_email_with_attachment
    ]
)
