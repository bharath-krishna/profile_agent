# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CopilotKit + Google ADK (Agent Development Kit) integration project that implements "FamilyMan" - an AI-powered personal assistant for Bharath Krishna. The assistant helps recruiters and hiring managers learn about Bharath's 15 years of professional experience, skills, and background. It combines a Next.js frontend with a Python FastAPI backend agent powered by Google's Gemini model.

**Source of Truth:** `/home/bharath/workspace/familyman-ui/Bharath_CV_2025.pdf` is the definitive source for all profile data (experience, skills, education).

## Architecture

### Three-Layer Architecture

1. **Frontend Layer** ([src/app/page.tsx](src/app/page.tsx))
   - Next.js 16 with React 19
   - Interactive profile page with collapsible sections, skills filtering, and contact cards
   - CopilotKit sidebar interface for conversational interactions with FamilyMan agent
   - Shared state management via `useCoAgent` hook syncs conversation context with backend
   - Generative UI components rendered from backend tool calls via `useRenderToolCall`
   - Five frontend tools exposed to agent via `useFrontendTool` for UI control:
     - `updateProfessionalSummary`: Update the professional summary section with new text
     - `setThemeColor`: Change profile page theme color
     - `highlightSection`: Scroll to and highlight specific profile sections
     - `filterSkills`: Filter technical skills by category
     - `showExperienceDetails`: Expand specific work experience entries
   - Four custom interactive components:
     - [SectionHeader](src/components/section-header.tsx): Collapsible section headers with icons
     - [ContactCard](src/components/contact-card.tsx): Click-to-copy contacts with vCard download
     - [SkillsFilter](src/components/skills-filter.tsx): Searchable skills with category filtering
     - [ExperienceTimeline](src/components/experience-timeline.tsx): Expandable work history timeline

2. **Integration Layer** ([src/app/api/copilotkit/route.ts](src/app/api/copilotkit/route.ts))
   - CopilotKit Runtime bridges frontend and backend
   - Uses `@ag-ui/client` HttpAgent to connect to FastAPI agent on `http://localhost:8001/`
   - Agent is registered as `"BharathAssistant"` in the runtime (must match `useCoAgent` hook name)

3. **Agent Layer** ([agent/main.py](agent/main.py))
   - Google ADK `LlmAgent` named "FamilyManAgent" with Gemini 2.5 Flash model
   - FastAPI server on port 8001
   - Uses callbacks to inject Bharath's professional profile and manage state:
     - `on_before_agent`: Initialize empty conversation context
     - `before_model_modifier`: Load and inject Bharath's professional profile into system prompt
     - `after_model_modifier`: Control agent execution flow
   - Three agent tools:
     - `add_conversation_note`: Track important points from recruiter discussions
     - `get_weather`: Demonstrate generative UI rendering (example tool)
     - `get_person_card`: Future family tree features (reserved for future use)
   - **Profile data architecture:** Externalized to `data/bharath_profile.md` (see below)
   - Connects to remote familyman agent on port 8003 via `RemoteA2aAgent` (currently disabled)

### Key Patterns

**Shared State Pattern:**
- Frontend declares state shape in [src/lib/types.ts](src/lib/types.ts) (`AgentState`)
- Backend maintains the actual state via `callback_context.state`
- State syncs bidirectionally: frontend `setState()` → backend, backend tool calls → frontend
- Current state: `{ conversation_context: string[] }` - tracks timestamped recruiter conversation notes
- Agent tools must receive the COMPLETE state when updating

**Profile Injection Pattern (AG-UI Best Practice):**
- Static reference data (Bharath's professional profile) is injected into system prompt via `before_model_modifier`
- Dynamic data (conversation notes) is stored in state for persistence across sessions
- Profile includes: contact info, 15-year work history, technical skills, education, certifications
- Agent answers questions directly from profile context without needing query tools

**Generative UI Pattern:**
- Backend tools can trigger frontend UI rendering in the chat interface
- Frontend registers render handlers via `useRenderToolCall` matching tool names
- Active examples:
  - `add_conversation_note` renders a green success card when notes are added
  - `get_weather` renders [WeatherCard](src/components/weather.tsx) component
  - `get_person_card` renders [PersonDetails](src/components/person-details.tsx) component

**Frontend Actions Pattern:**
- Frontend exposes UI control capabilities to agent via `useFrontendTool`
- FamilyMan agent can control the profile page interface through five tools:
  - `updateProfessionalSummary`: Update the professional summary section with new text
  - `setThemeColor`: Change the theme color (hex color code)
  - `highlightSection`: Scroll to and temporarily highlight a section (contact, summary, strengths, education, experience, skills, certifications, personal)
  - `filterSkills`: Filter skills by category (all, Languages & Web, Frontend, ML Frameworks, Infrastructure, Frameworks, Databases, CI/CD & Build, Cloud & Orchestration)
  - `showExperienceDetails`: Expand specific work experience entry by ID (exp-1 through exp-7)

## Development Commands

### Setup
```bash
# Install dependencies (any package manager works: pnpm, npm, yarn, bun)
pnpm install

# Set up Python agent (creates .venv in agent/ directory)
pnpm install:agent

# Set Google API key (required)
export GOOGLE_API_KEY="your-key-here"
```

### Development
```bash
# Run both UI and agent servers concurrently
pnpm dev

# Run with debug logging
pnpm dev:debug

# Run only the Next.js UI server (port 3000)
pnpm dev:ui

# Run only the Python agent server (port 8000)
pnpm dev:agent
```

### Build & Lint
```bash
# Build Next.js for production
pnpm build

# Start production server
pnpm start

# Run ESLint
pnpm lint
```

### Python Agent
```bash
# Activate Python virtual environment manually
source agent/.venv/bin/activate

# Run agent directly (from project root)
python agent/main.py
```

## Important Implementation Notes

### Adding New Agent Tools

**Backend Tools (Python):**
1. Define the tool function in [agent/main.py](agent/main.py) with `tool_context: ToolContext` parameter
2. Add to the `tools` list in the `LlmAgent` initialization (currently: `add_conversation_note`, `get_weather`, `get_person_card`)
3. For Generative UI tools, register a render handler in [src/app/page.tsx](src/app/page.tsx) using `useRenderToolCall`
4. Update types in [src/lib/types.ts](src/lib/types.ts) if state shape changes

**Frontend Tools (React):**
1. Define the tool using `useFrontendTool` in [src/app/page.tsx](src/app/page.tsx)
2. Specify tool name, description, and parameters
3. Implement the handler function that manipulates UI state or DOM
4. Agent can automatically discover and use frontend tools without backend changes

**Best Practice:** Backend tools should be for ACTIONS (add note, send email), not data retrieval. Profile data stays in system prompt, not in tools.

### Modifying Agent State

- State shape is defined in [src/lib/types.ts](src/lib/types.ts) as `AgentState`
- Current state: `{ conversation_context: string[] }` - minimal state for conversation tracking
- Backend state lives in `callback_context.state` (Python dict)
- When updating state via tools, always pass the COMPLETE state (see `add_conversation_note` implementation)
- State is injected into agent's system prompt via `before_model_modifier` callback
- Profile data is NOT in state - it's injected directly into system prompt for better performance

### Profile Data Management

**Location:** `data/bharath_profile.md`

The profile is externalized from Python code for easy updates without code changes:

**Loading Strategy (`load_profile_from_file()`):**
1. K8s path: `/profiles/bharath_profile.md` (mounted ConfigMap in production)
2. Dev path: `../data/bharath_profile.md` (relative to `agent/main.py`)
3. Fallback: Embedded default profile if no file found

**To Update Profile:**
- Development: Edit `data/bharath_profile.md`, restart agent
- Kubernetes: Edit `k8s/base/profile-config-map.yaml`, apply, restart pod

**Profile Contents:**
- Contact information (phone, email, website)
- Professional summary (15 years experience)
- Work experience (7 positions from 2010-present)
- Technical skills (8 categories)
- Education and certifications
- Personal profile and strengths

See `PROFILE_MIGRATION_SUMMARY.md` for detailed migration notes and troubleshooting.

### Agent Name Consistency

The agent name **must match** between:
- Frontend: `useCoAgent({ name: "BharathAssistant" })` in [src/app/page.tsx](src/app/page.tsx)
- Backend: `agents: { "BharathAssistant": new HttpAgent(...) }` in [src/app/api/copilotkit/route.ts](src/app/api/copilotkit/route.ts)

### Environment Variables

- `GOOGLE_API_KEY`: Required for Gemini model access (get from https://makersuite.google.com/app/apikey)
- `PORT`: Optional, defaults to 8001 for agent server
- `LOG_LEVEL`: Set to "debug" for verbose logging
- `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_BASE_URL`: Optional, for Langfuse tracing/observability

### Package Manager Notes

- Lock files are gitignored to support multiple package managers
- After initial startup, remove your lock file from .gitignore to track it
- The `postinstall` script automatically runs `install:agent`

### Dependency Pinning (CRITICAL)

**Langfuse:**
- Must use `langfuse==3.10.5` in `agent/pyproject.toml`.
- **Reason:** Newer versions (3.12+) require the `organization` field in API responses, which causes crashes with older self-hosted Langfuse servers.
- **Do not upgrade** unless the self-hosted server is also upgraded.

## Troubleshooting

**"I'm having trouble connecting to my tools":**
- Ensure agent server is running on port 8001
- Check GOOGLE_API_KEY is set correctly
- Verify both servers started without errors
- Check agent name consistency between frontend (`useCoAgent`) and backend route (`agents` config)

**Python import errors:**
```bash
cd agent
pip install -r requirements.txt
```

**Agent not receiving state updates:**
- Verify agent name matches between frontend and backend
- Check that tool functions pass complete state, not partial updates

## FamilyMan Agent Implementation

### Agent Purpose
FamilyMan is Bharath Krishna's personal AI assistant designed to:
- Answer questions about Bharath's 15 years of professional experience (2010-2025)
- Advocate on his behalf to recruiters and hiring managers
- Provide specific details about skills, projects, and achievements
- Track conversation context for follow-up discussions

### Profile Data Structure
The complete profile injected into the system prompt includes:

**Contact Information:**
- Phones: +1 8574379316, +91 7760779000
- Email: bharath.chakravarthi@gmail.com
- Website: https://profile.krishb.in

**Work Experience:** 7 positions from Intern at IBAB (2010) to Senior Software Engineer at Rakuten USA (Feb 2026)

**Technical Skills:** 8 categories including Languages (Python, Go), Frontend (React, NextJS), ML/LLM Frameworks (PyTorch, Huggingface Transformers), Infrastructure (Ansible, Terraform), Databases, CI/CD, and Cloud

**Education:**
- Master of Science in Bioinformatics - Kuvempu University (Focus: Genomics, Drug Discovery, Protein Engineering)
- Bachelor of Science in Biotechnology - Kuvempu University (Majors: Biotechnology, Botany, Computer Science)

**Certifications:** Certified Kubernetes Administrator (CKA)

### Interactive Profile Page
The profile page is fully responsive and interactive with:
- Collapsible sections (Strengths, Personal Profile)
- Expandable work experience timeline (click to see details)
- Skills filter with search functionality
- Click-to-copy contact information
- Download vCard button
- Mobile-friendly design (min 44x44px touch targets)

### Agent UI Control
The agent can manipulate the profile page UI through frontend tools:
- Update the professional summary dynamically
- Highlight and scroll to specific sections when answering questions
- Filter skills by category when discussing technical expertise
- Expand specific work experience entries when discussing past roles
- Change theme color for visual customization

### Testing the Agent
Sample queries to test FamilyMan:
- "How many years of experience does Bharath have?"
- "What is Bharath's current role?"
- "Does Bharath have Kubernetes experience?"
- "Tell me about Bharath's education"
- "Highlight the skills section" (tests frontend tool)
- "Show me Bharath's experience at Rakuten Tokyo" (tests experience expansion)
