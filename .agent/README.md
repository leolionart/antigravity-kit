# Antigravity Kit

> Modular AI Agent Capability Expansion Toolkit — for non-coders using agentic AI to optimize work workflows.

Works with **Claude Code**, **Gemini CLI**, and any AI assistant that supports agent/skill loading.

---

## What's Inside

```
.agent/
├── GETSTART.md        ← Setup guide (start here)
├── agents/            ← 7 specialist agents
├── skills/            ← Knowledge packs loaded on demand
├── workflows/         ← Slash command procedures
├── rules/             ← AI behavior rules (auto-loaded)
└── mcp_config.json    ← MCP server config template
```

---

## Agents (7)

Role-based AI personas for different types of work.

| Agent | What It Does |
|-------|-------------|
| `orchestrator` | Coordinates multiple agents for complex multi-domain tasks |
| `explorer-agent` | Researches and maps context before planning |
| `project-planner` | Breaks goals into structured tasks and milestones |
| `product-manager` | Writes requirements, user stories, feature specs |
| `product-owner` | Strategic prioritization, backlog decisions, MVP scoping |
| `documentation-writer` | Guides, SOPs, meeting notes, knowledge base articles |
| `seo-specialist` | Content optimization, keyword strategy, visibility |

---

## Skills (5)

Knowledge modules loaded on demand based on task context.

| Skill | When It Loads |
|-------|--------------|
| `behavioral-modes` | Adjusting AI tone and interaction style |
| `brainstorming` | Open-ended discovery, generating ideas |
| `plan-writing` | Structuring tasks, writing action plans |
| `documentation-templates` | Writing guides, SOPs, structured docs |
| `seo-fundamentals` | Improving content visibility and ranking |

---

## Workflows (6)

Slash commands that trigger structured procedures.

| Command | What It Does |
|---------|-------------|
| `/plan` | Break any goal into a structured action plan |
| `/brainstorm` | Socratic discovery — explore a problem space |
| `/orchestrate` | Coordinate multiple agents for complex tasks |
| `/status` | Get a snapshot of what's in progress |
| `/confluence-publishing` | Publish content to Confluence |
| `/jira-task-manager` | Create and manage Jira tasks |

---

## Quick Start

**Option A — Clone standalone** (dùng khi workspace chưa là git repo):
```bash
git clone https://github.com/leolionart/antigravity-kit .agent
```

**Option B — Add as git submodule** (dùng khi workspace đã là git repo):
```bash
git submodule add https://github.com/leolionart/antigravity-kit .agent
git submodule update --init --recursive
```

> ⚠️ Tên folder **`.agent`** là bắt buộc — Google Gemini CLI (Antigravity) tự động load từ đường dẫn này.

Then read **[GETSTART.md](GETSTART.md)** for the full setup guide.

---

## How Agents Are Triggered

Agents activate through **semantic matching** — the AI reads your request and selects the most relevant agent automatically. No keywords needed.

```
"Help me plan the Q3 roadmap"
→ Matches: project-planner + product-owner

"Research what we already know about customer churn"
→ Matches: explorer-agent

"Write a user guide for the new feature"
→ Matches: documentation-writer
```

---

## Philosophy

This kit is built for **workflow thinkers, not coders**.

- No code review, no test runners, no deployment scripts
- Focus: planning, documenting, researching, communicating
- Generic enough to reuse across projects and teams
- Private context (SOPs, product knowledge) lives in your own submodules

**Public** = this repo (generic capabilities)
**Private** = your `knowledge_base/` submodules (company/project-specific content)

---

## Contributing

Improvements should work for **any AI assistant and any team**, not just one tool or one company.

- Add agents for uncovered workflow domains
- Add skills for new knowledge areas
- Keep code-specific content out of this repo

Issues and PRs: [github.com/leolionart/antigravity-kit](https://github.com/leolionart/antigravity-kit)
