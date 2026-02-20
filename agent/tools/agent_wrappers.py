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

from ..sub_agents.email_composer import email_composer_agent
from ..sub_agents.conversation_tracker import conversation_note_agent

logger = logging.getLogger(__name__)


async def compose_and_send_profile(
    tool_context: ToolContext,
    recipient_email: str,
    format: str = "resume",
    custom_message: Optional[str] = None
) -> Dict[str, str]:
    """Generate profile PDF and email it to a recipient.

    Uses the EmailComposer sub-agent to:
    - Generate a professional PDF of Bharath's profile
    - Send it via email to the specified recipient
    - Handle PDF generation failures gracefully

    Args:
        tool_context: Tool execution context with shared state
        recipient_email: Email address to send the profile to
        format: PDF format (resume, full_profile, etc.)
        custom_message: Optional custom email message body

    Returns:
        Dict with status, message, PDF path, and email details
    """
    logger.debug("compose_and_send_profile: %s", recipient_email)

    # Create AgentTool wrapper for EmailComposer sub-agent
    agent_tool = AgentTool(agent=email_composer_agent)

    # Build request for sub-agent
    request = f"""Generate a {format} PDF of Bharath's profile and email it to {recipient_email}.
    {"Include this message: " + custom_message if custom_message else "Use the standard professional introduction."}
    """

    # Execute sub-agent asynchronously
    output = await agent_tool.run_async(
        args={"request": request},
        tool_context=tool_context
    )

    # Update parent state with email action
    context_list = tool_context.state.get("conversation_context", [])
    if context_list is None:
        context_list = []

    # Record the email action in conversation context
    if isinstance(output, dict):
        status = output.get("status", "unknown")
        context_list.append(f"[EMAIL] Attempted to send {format} profile to {recipient_email} - Status: {status}")
    else:
        context_list.append(f"[EMAIL] Sent {format} profile to {recipient_email}")

    tool_context.state["conversation_context"] = context_list

    return output


async def track_conversation_note(
    tool_context: ToolContext,
    task: str,
) -> Dict[str, str]:
    """Track a conversation note using the ConversationTracker sub-agent.

    Uses the ConversationNoteAgent sub-agent to:
    - Save timestamped notes to file

    Args:
        tool_context: Tool execution context with shared state
        task: The conversation task to save as a note

    Returns:
        Dict with status, message, and file path
    """
    logger.debug("track_conversation_note: %s", task)

    # Create AgentTool wrapper for ConversationNoteAgent sub-agent
    agent_tool = AgentTool(agent=conversation_note_agent)

    # Build request for sub-agent
    request = f"""Save this conversation: {task}."""

    # Execute sub-agent asynchronously
    output = await agent_tool.run_async(
        args={"request": request},
        tool_context=tool_context
    )

    logger.debug("conversation note saved: %s", output)

    return output
