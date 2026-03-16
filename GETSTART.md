# GETSTART — Antigravity Kit Setup Guide

> **Audience**: AI Agents (Claude Code, Gemini CLI, OpenClaw, any AI assistant)
> **Purpose**: Get from zero to fully operational working environment with all submodules connected.

---

## What Is This?

This repo (`antigravity-kit`) is the **public, reusable layer** of an AI-augmented workspace. It provides:

- **20 Specialist Agents** — Role-based personas (frontend, backend, security, etc.)
- **36 Skills** — Domain knowledge modules loaded on demand
- **11 Workflows** — Slash-command procedures (`/plan`, `/debug`, `/orchestrate`, ...)
- **MCP Config Template** — Connect external tools (Jira, Confluence, context servers)

Private context (company SOPs, system prompts, product knowledge) lives in **separate submodules** that extend this kit. This document teaches you how to wire everything together.

---

## Architecture Overview

```
your-workspace/
├── .agent/                    ← THIS REPO (public, shared AI kit)
│   ├── GETSTART.md            ← You are here
│   ├── agents/                ← 20 specialist agent personas
│   ├── skills/                ← 36 modular skill packs
│   ├── workflows/             ← 11 slash-command workflows
│   ├── rules/                 ← Global AI behavior rules
│   ├── scripts/               ← Validation & checklist scripts
│   └── mcp_config.json        ← MCP server config template
│
├── .claude/                   ← Claude Code-specific (private, project-scoped)
│   ├── CLAUDE.md              ← Claude operating instructions
│   └── skills/                ← Project-specific skills (not in this repo)
│
└── knowledge_base/            ← Domain submodules (private GitLab/GitHub)
    ├── omniagent/             ← OmniAgent SOPs, system prompts, references
    ├── product-kb/            ← Company-wide product standards, design systems
    └── n8n/                   ← n8n workflow templates
```

### Layer Responsibilities

| Layer | Who Maintains | Content Type | Visibility |
|-------|--------------|--------------|------------|
| `.agent/` | Open source | Generic AI capabilities | **Public** |
| `.claude/skills/` | Project team | Claude-specific project skills | Private |
| `knowledge_base/*` | Domain owners | Operational knowledge | Private |

---

## Step 1: Clone the Kit

```bash
# Option A: Start fresh workspace with antigravity-kit
git clone https://github.com/leolionart/antigravity-kit .agent

# Option B: Add as submodule to existing workspace
git submodule add https://github.com/leolionart/antigravity-kit .agent
git submodule update --init --recursive
```

---

## Step 2: Add Private Knowledge Submodules

If you have access to private knowledge bases, add them as submodules:

```bash
# Example: OmniAgent knowledge base (internal)
git submodule add git@your-gitlab.com:ai-context/product/omniagent.git knowledge_base/omniagent

# Example: Product standards
git submodule add git@your-gitlab.com:ai-context/product/product-kb.git knowledge_base/product-kb

# Initialize all submodules at once
git submodule update --init --recursive
```

**If you don't have private submodules**, skip this step — the kit works standalone.

---

## Step 3: Configure MCP Tools

Copy and customize the MCP config template:

```bash
# For Claude Code
cp .agent/mcp_config.json .mcp.json
# Then edit .mcp.json with your actual API keys

# For Gemini / other agents
cp .agent/mcp_config.json ~/.gemini/antigravity/mcp_config.json
```

**Edit the config** — replace placeholder values:

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "env": {
        "CONFLUENCE_URL": "https://your-confluence.net",
        "CONFLUENCE_PERSONAL_TOKEN": "YOUR_TOKEN_HERE",
        "JIRA_URL": "https://your-jira.net",
        "JIRA_PERSONAL_TOKEN": "YOUR_TOKEN_HERE"
      }
    }
  }
}
```

**Available MCP server integrations** (see `mcp_config.json` for full list):
- `mcp-atlassian` — Jira + Confluence
- `context7` — Upstash context store
- `shadcn` — shadcn/ui component library

---

## Step 4: Activate AI Rules

### For Claude Code

Create or update `.claude/CLAUDE.md` in your workspace root:

```markdown
# CLAUDE.md

## Primary Directive
Read `.agent/rules/GEMINI.md` for agent/skill protocols.

## Skill Discovery
Skills in `.agent/skills/` are available via semantic matching.
Project-specific skills in `.claude/skills/` take priority over generic skills.
```

### For Gemini CLI

The `.agent/rules/GEMINI.md` file auto-activates via `trigger: always_on` frontmatter.

### For Other AI Assistants

Copy the relevant sections from `.agent/rules/GEMINI.md` into your assistant's system prompt or instruction file.

---

## Step 5: Verify Setup

Run the validation checklist:

```bash
# Quick check (development)
python .agent/scripts/checklist.py .

# Full verification (pre-deployment)
python .agent/scripts/verify_all.py . --url http://localhost:3000
```

Expected output for a clean setup:
```
✅ Agent rules loaded
✅ Skills directory found (36 skills)
✅ Workflows directory found (11 workflows)
✅ MCP config present
```

---

## How Skills Work

Skills are **loaded on demand** through semantic matching — the AI reads your request, finds the closest skill description, and loads that skill's knowledge.

```
User Request → Skill Description Match → Load SKILL.md → Apply Instructions
```

### Example: Requesting a frontend task

```
User: "Build a login page with React"
AI: Matches → frontend-specialist agent + react-best-practices skill
    → Loads .agent/agents/frontend-specialist.md
    → Loads .agent/skills/react-best-practices/SKILL.md
    → Applies all rules from both files
```

### Adding Custom Skills

Create a new skill folder:

```bash
mkdir .agent/skills/my-custom-skill
cat > .agent/skills/my-custom-skill/SKILL.md << 'EOF'
---
name: my-custom-skill
description: What this skill does and when to use it
version: 1.0.0
---

# My Custom Skill

## When to Use
...

## Instructions
...
EOF
```

---

## Submodule-Scoped Skills

When a submodule has its own operational context, skills can live inside the submodule:

```
knowledge_base/omniagent/
├── AGENTS.md              ← Submodule-specific operating contract
├── system-prompts/        ← Content files
├── sops/                  ← SOP articles
└── skills/                ← OmniAgent-specific skills (symlinked to .claude/skills/)
    ├── omniagent-config/
    └── omniagent-sop/
```

**Pattern**: Generic skills → `.agent/skills/`  |  Domain skills → `knowledge_base/<domain>/skills/`

Symlink domain skills into `.claude/skills/` to make them discoverable by Claude Code:

```bash
ln -s ../../knowledge_base/omniagent/skills/omniagent-config .claude/skills/omniagent-config
```

---

## Slash Commands Reference

| Command | What It Does |
|---------|-------------|
| `/plan` | Break task into structured plan |
| `/brainstorm` | Socratic discovery questions |
| `/create` | Scaffold new feature/component |
| `/debug` | Root cause analysis workflow |
| `/enhance` | Improve existing code |
| `/deploy` | Deployment checklist |
| `/orchestrate` | Coordinate multiple agents |
| `/test` | Run test suite |
| `/status` | Project health check |
| `/preview` | Preview changes before commit |
| `/ui-ux-pro-max` | Design with 50 styles × 21 palettes |

---

## Troubleshooting

### Submodule not initialized
```bash
git submodule update --init --recursive
# If stuck on iCloud sync:
./scripts/fix_git_sync.sh
```

### MCP tools not connecting
1. Check API keys in `.mcp.json` (not committed to git)
2. Run `mcp-atlassian` manually to test connection
3. Ensure `.mcp.json` is in `.gitignore`

### Skill not triggering
- Skills match by **description semantics**, not keywords
- Try rephrasing: "help me debug" → "do root cause analysis on this error"
- Check `.agent/skills/<skill-name>/SKILL.md` for exact trigger context

---

## Contributing

This kit is intentionally **generic** — improvements should work for any AI assistant, not just one.

- `agents/` — Add new specialist personas for uncovered domains
- `skills/` — Add knowledge packs for new tech stacks
- `workflows/` — Add new slash commands
- Keep private/company-specific content **out** of this repo

PRs welcome at: https://github.com/leolionart/antigravity-kit

---

## Quick Reference Card

```
Need to...                          Use...
────────────────────────────────────────────────────────
Start a complex task                /plan or /orchestrate
Debug something broken              /debug
Build UI component                  frontend-specialist agent
Write backend API                   backend-specialist agent
Check security                      security-auditor agent
Write tests                         test-engineer agent
Document code                       documentation-writer agent
Deploy to production                /deploy + devops-engineer agent
Search for patterns in code         code-archaeologist agent
Research competitors                product-manager agent
Connect Jira/Confluence             MCP → mcp-atlassian config
Add domain knowledge                knowledge_base/ submodule
Add company-specific skills         .claude/skills/ (private)
```
