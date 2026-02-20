"""FamilyMan Sub-Agents Module.

Provides specialized agents for specific tasks:
- email_composer: PDF generation and email sending
- conversation_tracker: Conversation note management
"""

from .email_composer import email_composer_agent
from .conversation_tracker import conversation_note_agent

__all__ = ["email_composer_agent", "conversation_note_agent"]
