# Bharath's Assistant Project Guide

## Project Overview
Bharath's Assistant is an AI-powered personal assistant designed to represent Bharath Krishna to recruiters and hiring managers. Combines:
- Interactive Next.js 16+ React 19 profile page
- Python backend agent (Google ADK + CopilotKit)
- Conversational interface showcasing 15+ years of experience

Key features:
- ATS-compliant single-view dashboard layout
- Professional persona representation
- Experience timeline with filtering capabilities

## Getting Started
### Prerequisites
- Node.js v18+
- pnpm package manager
- Python 3.10+
- Google API key (for backend agent)

### Installation
```bash
pnpm install
pnpm install:agent
```

### Basic Operation
```bash
pnpm dev  # Starts frontend (3000) and agent (8000)
pnpm lint # Runs code quality checks
```

### Testing
- UI consistency checks
- Agent behavior validation
- Integration testing between frontend/backend

## Project Structure
### Frontend (Next.js)
- **Primary file**: `src/app/page.tsx`
- **Key components**: 
  - `CopilotSidebar` (interactive UI controls)
  - `ExperienceTimeline` (work history display)
  - `SkillsFilter` (visual filtering system)
- **Integration**: `/api/copilotkit/route.ts` (frontend-backend bridge)

### Backend Agent (Python)
- **Primary file**: `agent/main.py`
- **Framework**: Google ADK + CopilotKit
- **Agent name**: `BharathAssistant` (must match frontend `useCoAgent`)
- **State management**: `conversation_context` for notes

### Directory Structure
```
/src
  /app
    page.tsx          # Main UI entry point
  /components
    ExperienceTimeline.tsx
    SkillsFilter.tsx
    person-details.tsx
    
/agent
  main.py             # Python backend agent
  pyproject.toml      # Python dependencies
  uv.lock             # Virtual environment lock
```

## Development Workflow
### Coding Standards
- Adhere to ATS dashboard design principles
- Maintain consistent UI patterns
- Profile data must reference `Bharath_CV_2025.pdf`
- Backend agent behavior must match system prompt in `agent/main.py`

### Build & Deployment
- Development: `pnpm dev`
- Linting: `pnpm lint`
- Build preparation: `pnpm build` (not explicitly documented but implied)
- API endpoint: REST service at `localhost:8000`

## Key Concepts
- **BharathAssistant**: Internal agent persona (matches frontend `useCoAgent`)
- **conversation_context**: Manages real-time conversation notes
- **before_model_modifier**: Injects professional profile into model context
- **UI Control Tools**:
  - `setThemeColor`: Change primary theme color
  - `highlightSection`: Scroll to and flash sections
  - `filterSkills`: Scroll to skills section
  - `showExperienceDetails`: Target specific experience entries (exp-1 to exp-7)

## Common Tasks
### Profile Data Updates
1. Reference `Bharath_CV_2025.pdf` for experience details
2. Never hallucinate experience metrics
3. Update `conversation_context` when adding new notes

### UI Interaction Examples
```tsx
// Change theme color
setThemeColor('primary', '#10b981');

// Highlight skills section
highlightSection('skills');

// Scroll to experience entry

// Show specific experience details
showExperienceDetails('exp-3');
```

### Agent Management
- Restart agent: `pkill python` then `pnpm dev`
- View agent logs: `tail -f agent/logs/app.log` (requires setup)

## Troubleshooting
| Issue | Solution |
|-------|----------|
| Agent not responding | Verify Python process is running, check port 8000 |
| UI components misaligned | Run `pnpm lint` and check layout constraints |
| Profile data mismatch | Compare against `Bharath_CV_2025.pdf` |
| Dependency issues | Run `pnpm install:agent` to refresh Python environment |

## References
- [Google ADK Documentation](https://cloud.google.com/vertex-ai)
- [Next.js 16 Documentation](https://nextjs.org/docs)
- [CopilotKit Integration Guide](https://copilotkit.dev)
- `AGENTS.md`: Full architecture details
- `CLAUDE.md`: Project-specific conventions and standards
- `Bharath_CV_2025.pdf`: Source of truth for professional experience

> **Note**: Verify all sections against current project state before use. Some development workflows require customization based on team environment.