"""AgentTool Wrappers for FamilyMan Sub-Agents.

This module provides async wrapper functions that delegate tasks to specialized
sub-agents using the ADK AgentTool pattern. Each wrapper:
1. Creates an AgentTool instance for the target sub-agent
2. Executes the sub-agent asynchronously
3. Updates the parent agent's state with results
4. Handles errors gracefully

Pattern reference:
https://github.com/googleapis/python-adk/blob/main/samples/agents/data-science/data_science/tools.py
"""

import logging
from typing import Dict, Optional

from google.adk.tools import ToolContext, AgentTool

from agent.sub_agents.recruit_agent import recruit_agent

logger = logging.getLogger(__name__)

async def gather_job_details(
    tool_context: ToolContext,
    message: str,
    email: str,
    company: Optional[str] = None,
    phone: Optional[str] = None,
    notes: Optional[str] = "No additional notes",
) -> Dict[str, str]:
    """Save gathered detailed job information using the RecruitAgent sub-agent.

    Uses the RecruitAgent sub-agent to:
    - Extract detailed job requirements and preferences from recruiter conversations

    Args:
        tool_context: Tool execution context with shared state
        message: The recruiter conversation message
        email: Recruiter's email address
        company: Company name
        phone: Recruiter's phone number
        notes: Additional notes from the conversation

    Returns:
        Dict with status, message, and extracted job details
    """
    args = {"message": message, "email": email, "company": company, "phone": phone, "notes": notes}
    logger.debug("Gathering job details with input: %s", args)

    # Create AgentTool wrapper for RecruitAgent sub-agent
    agent_tool = AgentTool(agent=recruit_agent)

    # Execute sub-agent asynchronously
    output = await agent_tool.run_async(
        args=args,
        tool_context=tool_context
    )

    context_list = tool_context.state.get("conversation_context", [])
    if context_list is None:
        context_list = []

    # Add tool output to conversation context
    context_entry = f"[TOOL] {output}"
    context_list.append(context_entry)
    tool_context.state["conversation_context"] = context_list

    logger.debug("conversation note saved: %s", output)

    logger.debug("Job details gathered: %s", output)

    output.update(**args)
    import ipdb; ipdb.set_trace()
    if output.get("status") == "success":
        output["status"] = "confirmed"
    else:
        output["status"] = "rejected"

    return output

async def save_recruiter_info(
    tool_context: ToolContext,
    message: str,
    email: str,
    company: Optional[str] = None,
    phone: Optional[str] = None,
    notes: Optional[str] = "No additional notes",
) -> Dict[str, str]:
    """Track a conversation note using the ConversationTracker sub-agent.

    Uses the ConversationNoteAgent sub-agent to:
    - Save timestamped notes to file

    Args:
        tool_context: Tool execution context with shared state
        message: The conversation message to save as a note
        email: The email address associated with the conversation
        company: The company associated with the conversation
        phone: The phone number associated with the conversation
        notes: Optional additional notes for the conversation

    Returns:
        Dict with status, message, and file path
    """
    args = {"message": message, "email": email, "company": company, "phone": phone, "notes": notes}
    logger.debug("Recruiter info to save: %s", args)

    # Create AgentTool wrapper for ConversationNoteAgent sub-agent
    agent_tool = AgentTool(agent=recruit_agent)

    # Execute sub-agent asynchronously
    output = await agent_tool.run_async(
        args=args,
        tool_context=tool_context
    )

    context_list = tool_context.state.get("conversation_context", [])
    if context_list is None:
        context_list = []

    # Add tool output to conversation context
    context_entry = f"[TOOL] {output}"
    context_list.append(context_entry)
    tool_context.state["conversation_context"] = context_list

    logger.debug("conversation note saved: %s", output)

    output.update(**args)
    if output.get("status") == "success":
        output["status"] = "confirmed"
    else:
        output["status"] = "rejected"

    return output
    # if output.get("status") == "success":
    #     return output.get("response", "Saved recruiter info successfully.")
    # else:
    #     return "Failed to save recruiter info."
