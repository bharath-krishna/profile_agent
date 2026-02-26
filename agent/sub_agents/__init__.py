"""FamilyMan Sub-Agents Module.

Provides specialized agents for specific tasks:
- email_composer: PDF generation and email sending
- conversation_tracker: Conversation note management
"""

from .recruit_agent import recruit_agent

__all__ = ["recruit_agent"]
