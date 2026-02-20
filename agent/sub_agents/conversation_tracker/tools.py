"""Conversation Tracker Tools for managing notes and conversation state."""

import logging
from typing import Dict
from google.adk.tools import ToolContext
    
logger = logging.getLogger(__name__)


def save_conversation_note(
    tool_context: ToolContext,
    note: str,
    source: str = "Unknown"
) -> Dict[str, str]:
    """Save a timestamped conversation note to file and state.

    Use this to track:
    - Key recruiter questions or concerns
    - Specific job requirements discussed
    - Follow-up items or next steps
    - Important discussion points

    Args:
        tool_context: Tool execution context
        note: A concise note about the conversation
        source: The name of the person (e.g., recruiter) or source of the note

    Returns:
        Dict indicating success and the note added
    """
    try:
        from datetime import datetime
        import os


        # Ensure notes directory exists
        notes_dir = os.path.join(
            os.environ.get("NOTES_DIR", os.path.dirname(os.path.abspath(__file__))),
            "notes"
        )
        os.makedirs(notes_dir, exist_ok=True)

        logger.info(f"Saving conversation note: {note} (source: {source}) to {notes_dir}")

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
            "filepath": filepath,
            "timestamp": timestamp.isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error adding note: {str(e)}",
            "error_details": str(e)
        }
