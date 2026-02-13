# AGENTS.md - FamilyMan UI Project Context

This file provides context for OpenClaw and other AI agents working on the `familyman-ui` project.

## Project Overview

**"Bharath's Assistant" (formerly FamilyMan)** is an AI-powered personal assistant designed to represent Bharath Krishna to recruiters and hiring managers. It combines an interactive Next.js profile page with a Python backend agent (Google ADK + CopilotKit).

- **Goal:** Showcase Bharath's 15+ years of experience via a conversational interface that can control the UI.
- **Source of Truth:** `/home/bharath/workspace/familyman-ui/Bharath_CV_2025.pdf` is the definitive source for experience, skills, and education data.

## Architecture

### 1. Frontend (Next.js 16 + React 19)
- **Path:** `src/app/page.tsx`
- **UI:** Single-page "ATS-compliant" dashboard layout (Sidebar + Main Content).
- **Interactive Components:** `CopilotSidebar`, `ExperienceTimeline`, `SkillsFilter`.
- **Frontend Tools:** The agent can control the UI via these tools defined in `page.tsx`:
    - `setThemeColor`: Change the primary theme color.
    - `highlightSection`: Scroll to and flash a specific section (e.g., "experience", "skills").
    - `filterSkills`: Scroll to the skills section (filtering visual logic simplified).
    - `showExperienceDetails`: Scroll to a specific job entry (`exp-1` to `exp-7`).

### 2. Backend Agent (Python FastAPI + Google ADK)
- **Path:** `agent/main.py`
- **Framework:** Google Agent Development Kit (ADK) + CopilotKit.
- **Model:** Gemini 2.5 Flash.
- **Agent Name:** `BharathAssistant` (must match frontend `useCoAgent`).
- **State Management:** Tracks conversation notes in `conversation_context`.
- **System Prompt:** Injects Bharath's full professional profile into the model context via `before_model_modifier`.

### 3. Integration Layer
- **Path:** `src/app/api/copilotkit/route.ts`
- **Role:** Bridges the Next.js frontend and the Python agent running on port 8000.

## Development Commands

Run these from the project root (`~/workspace/familyman-ui/`):

```bash
# Start both Frontend (3000) and Agent (8000)
pnpm dev

# Install dependencies
pnpm install
pnpm install:agent  # Sets up Python venv in agent/

# Linting
pnpm lint
```

## Key Guidelines for Agents

1.  **Profile Accuracy:** Always refer to `Bharath_CV_2025.pdf` (or the content injected in `agent/main.py`) when updating profile data. Do not hallucinate experience.
2.  **UI Consistency:** The UI is designed to be a dense, single-view dashboard. Avoid adding excessive scrolling or hiding content behind clicks unless necessary.
3.  **Agent Persona:** The internal agent (`BharathAssistant`) acts as a professional representative. Its system prompt is in `agent/main.py`.
4.  **Environment:**
    - `GOOGLE_API_KEY` is required for the backend agent.
    - `node_modules`, `.next`, and `.venv` are gitignored.
5.  **Tools:**
    - **Backend Tools:** Use for data persistence (e.g., `add_conversation_note`).
    - **Frontend Tools:** Use for UI manipulation (scrolling, highlighting).

## Recent Changes (Log)

- **Renaming:** Agent renamed from "FamilyMan" to "Bharath's Assistant".
- **Layout:** Switched to an ATS-friendly Sidebar + Main Content layout.
- **Education:** Moved above Experience, compacted to a 2-column grid.
- **Skills:** Removed "AI/ML" category (PyTorch/ONNX) per user request.
