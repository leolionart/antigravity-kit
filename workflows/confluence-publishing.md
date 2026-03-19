---
name: confluence-publishing
description: >-
  Publish markdown deliverables to Confluence with compliant formatting, metadata syncing, and automation hooks.
  Use when the user wants to publish a document to Confluence, update an existing Confluence page, sync local markdown
  to Confluence, or mentions "push to Confluence", "đăng lên Confluence", or "cập nhật trang Confluence".
version: 1.1.0
category: delivery
updated: 2026-01-30
changelog: Added wiki format decision tree and bullet list rendering fix
---

# Confluence Publishing Skill

> ⚠️ **CRITICAL**: All Confluence operations (docs.vexere.com) MUST use MCP tools. Never use web fetch tools (FetchUrl, WebSearch, curl) as they will be blocked by authentication. Always use `mcp__MCP_DOCKER__confluence_*` tools for reading, updating, searching, or any Confluence interaction.

## Purpose
- Enforce the canonical workflow for turning repository Markdown into production-ready Confluence pages.
- Guard against metadata drift, broken checklists, and incorrect parent-page targeting.
- When harvesting content from Confluence pages (via MCP) that contain images/attachments, **download all images/attachments locally alongside the markdown mirror and update links to the local copies** to keep offline mirrors complete.

## Role Alignment
- Applies to every Codex CLI agent before invoking `mcp__MCP_DOCKER__confluence_update_page` or `mcp__MCP_DOCKER__confluence_create_page`.

## Execution Mode
- **Bắt buộc chạy trong sub-agent** theo AGENTS.md Section 4 vì Confluence API response rất nặng và sẽ làm đầy context window của luồng chat chính.
- **Ưu tiên** `subagent_type: confluence-agent`.
- **Fallback chính thức**: nếu runtime không nhận diện `confluence-agent`, delegate sang `subagent_type: general-purpose` và nhúng operator instructions từ `.claude/agents/confluence-agent.md` vào prompt để giữ nguyên format decision tree, conversion rules, và post-publish checks.
- **Ngoại lệ**: Chỉ được gọi MCP trực tiếp khi thao tác đơn lẻ (đọc 1 page hoặc update 1 field). Khi flow bao gồm prepare + convert + publish + post-publish → bắt buộc delegate.

## Prerequisites
- **MCP Configuration**: Ensure `mcp-configuration` skill has been run and validated
- Update `updated_at` in the source document (`date +%Y-%m-%d`) and keep `created_at` unchanged.
- Confirm the destination using `docs/confluence-ai-index.md` (space, parent page, title format).
- If mirroring an existing Confluence page locally, create an `assets/` (or `media/`) folder adjacent to the markdown file and plan to store all images/attachments there.

## Mermaid Diagrams & Visual Content

### When Your Document Contains Mermaid Diagrams

Mermaid diagrams require special handling for Confluence compatibility. Follow this integrated workflow:

#### 1. Validate Diagram Syntax
Before publishing, ensure your Mermaid diagram follows these standards:

**Diagram Structure:**
- Prefer `flowchart TD` for top-to-bottom flow
- Avoid `subgraph` unless already verified for compatibility
- Use flat layouts with prefixed labels to indicate swimlanes

**Node Naming Rules:**
- Rectangles: `nodeId["Label"]`
- Decisions: `Decision{"Yes/No?"}`
- Start/End: `Start((Start))`, `ProcessEnd((Done))`
- Notes: `note1["Note: ..."]`
- Escape special characters: wrap labels containing `()<>{}:,&"` in quotes
- Avoid reserved IDs like `end`

**Standard Color Palette:**
```mermaid
classDef startNode fill:#90EE90,stroke:#2E7D32,stroke-width:2px
classDef processNode fill:#87CEEB,stroke:#333333,stroke-width:1.5px
classDef decisionNode fill:#FFE4B5,stroke:#B26A00,stroke-width:1.5px
classDef handoffNode fill:#FFF5E1,stroke:#FF8C00,stroke-width:1.5px
classDef externalNode fill:#F5E6FF,stroke:#8E44AD,stroke-width:1.5px
classDef endPositive fill:#B2FFB2,stroke:#2E7D32,stroke-width:2px
classDef endNegative fill:#FFB2B2,stroke:#C62828,stroke-width:2px
```

**Compatibility Rules (Mermaid v9/v11):**
- ❌ Avoid: `[[Subroutine]]`, `{{Hexagon}}`, `[/Trapezoid/]` (unsupported in v9)
- ❌ Avoid: Inline attribute syntax `nodeId@{ label: "..." }`
- ❌ Avoid: Quoted edge labels `-- "Không" -->`
- ✅ Use: `classDef` + `class` for coloring
- ✅ Use: Standard arrows, unquoted edge labels: `-- Không -->`
- ✅ Use: `nodeId["Label"]` declarations
- Escape HTML-sensitive characters: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`

#### 2. Wrap for Confluence (Use MCP or manual formatting)
Instead of using python scripts, ensure your mermaid macro is formatted as:
```xml
<ac:structured-macro ac:name="mermaid-macro">
  <ac:plain-text-body><![CDATA[...diagram...]]></ac:plain-text-body>
</ac:structured-macro>
```

#### 3. Embed and Publish
- Embed the wrapped macro into your document body **before** publishing
- Use `content_format='storage'` when publishing

### Documents Without Mermaid
If your document contains only text, tasks, and lists—proceed directly to "Execution Checklist" step 1.

## Execution Checklist

### 1. Prepare the Markdown Source
1. Read the newest version of the file from the repo (never rely on cached copies).
2. Refresh metadata:
   - `updated_at` → current date.
   - `public_confluence_url` → existing Confluence URL or `not_public` for drafts.
   - `published_at` → keep `null` before publish (set after successful publish).
3. Review the content for placeholder text, broken links, or legacy notes that should be pruned pre-publish.
4. If the source Confluence page has images/attachments:
   - Use MCP to list/download attachments; save them under `assets/<slug>/` (relative to the markdown).
   - Update image links in the markdown to point to the local copies (no remote-only links in the mirror).

### 2. Convert Markdown to Confluence-Friendly Content

#### Format Selection Strategy (CRITICAL)

**⚠️ IMPORTANT: Confluence markdown converter has inconsistent bullet list rendering.**

Use this decision tree to select the correct format:

```
Does content have bullet lists?
├─ YES → Use wiki format (REQUIRED)
│   ├─ Simple bullets → wiki format
│   └─ Nested bullets → wiki format (MANDATORY)
│
└─ NO → Check other complexity
    ├─ Has tables with line breaks? → wiki format
    ├─ Has complex nested structures? → wiki format
    ├─ Has tasks/checklists/Mermaid? → storage format
    └─ Simple text and headings only? → markdown OK
```

**Known Issue**: Markdown format (`content_format='markdown'`) with bullet lists (`- item` or `* item`) often fails to render as proper bullet points in Confluence—content appears as continuous text instead. This affects both simple and nested lists.

**Solution**: When content contains bullet lists, **always use wiki format** (`content_format='wiki'`).

#### Wiki Format Syntax Reference

When using wiki format, convert markdown syntax to Confluence wiki markup:

**Headers:**
- `# Title` → `h1. Title`
- `## Section` → `h2. Section`
- `### Subsection` → `h3. Subsection`

**Text Formatting:**
- `**bold**` → `*bold*` (single asterisk)
- `*italic*` → `_italic_`
- `` `code` `` → `{{code}}` (double braces)

**Lists:**
- `- bullet` → `* bullet`
- `  - nested` → `** nested` (double asterisk)
- `    - level 3` → `*** level 3` (triple asterisk)
- Numbered lists: `# item` → `# item` (same)

**Code Blocks:**
- ` ```json` → `{code:json}`
- ` ``` ` (closing fence) → `{code}` (closing tag)

**Tables:**
- `| Header |` → `||Header||` (double pipes for headers)
- `| Cell |` → `|Cell|` (single pipes for cells)
- Line breaks in cells: use `\\` instead of `\n`

**Links:**
- `[text](url)` → `[text|url]`

#### Content Preparation Steps

- **Frontmatter & H1**: Exclude the YAML block and top-level `# Title` from the payload. The MCP call will set the page title explicitly.
- **Mermaid Diagrams**: Manually wrap as described above if needed.
- **Bullet Lists**:
  - If using **wiki format**: Convert `-` to `*`, nested indentation to `**`/`***`
  - If using **markdown format**: Avoid if possible (known rendering issues)
- **Checklists**: Markdown tasks (`- [ ]`, `- [x]`) should be converted to Confluence task macros if possible, or use `content_format='storage'` for high fidelity.
  - If high fidelity is needed (checklists, macros), construct the `storage` format XML manually or via internal logic.
  - **Strike-through text**: Render as `<span style="text-decoration: line-through;">…</span>` when using storage format.
  - **Code blocks**: In wiki format use `{code:lang}...{code}`; in storage mode inline code becomes `<code>`.


### 3. Publish via MCP
1.  **Choose Publishing Tool**:
    *   **Default**: Use `mcp__MCP_DOCKER__confluence_update_page` (for existing pages) or `mcp__MCP_DOCKER__confluence_create_page` (for new pages).
2.  **Execute Publishing**:
    *   Call the appropriate MCP tool with the prepared content.
    *   Ensure `content_format` is set correctly (`markdown` for simple text, `storage` for complex formatting/macros).
3.  **Verify**: Open the Confluence page to ensure rendering is correct.


### 4. Post-Publish Actions
1. Open the Confluence page to ensure headings, lists, macros, and tasks render correctly.
2. Update `public_confluence_url` with the live page link and set `published_at` to `YYYY-MM-DD`.
3. Commit the changes and push so the repo mirrors the published state.

## Managing Internal Link Mentions (STRICT)
- Use wikilinks `[[...]]` **only** inside frontmatter (e.g., `related_docs`).
- In document body, **never** use wikilinks. Always use full Confluence URLs for cross-doc references.
- Example frontmatter snippet:
  ```yaml
  related_docs:
    - "[[docs/confluence-ai-index.md]]"
    - "[[skills/sprint-goal-prep/SKILL.md]]"
  ```
- When publishing, remove frontmatter from payload; body must already contain only Confluence URLs (no `[[]]`).

## MCP Tooling
- `mcp__MCP_DOCKER__confluence_get_page`
- `mcp__MCP_DOCKER__confluence_update_page`
- `mcp__MCP_DOCKER__confluence_create_page`

## Quality Gates

### Pre-Publish Validation
- Payload excludes YAML frontmatter and H1 title
- Page `title` parameter is set explicitly in MCP call
- **Format Selection Validated**:
  - If content has bullet lists → `content_format='wiki'` (REQUIRED)
  - If content has nested bullets → `content_format='wiki'` (MANDATORY)
  - If content has tasks/checklists/Mermaid → `content_format='storage'`
  - If simple text only → `content_format='markdown'` acceptable
- **Wiki Format Conversion** (if using wiki format):
  - Headers converted: `##` → `h2.`, `###` → `h3.`
  - Bullets converted: `-` → `*`, nested → `**`/`***`
  - Bold converted: `**text**` → `*text*`
  - Code converted: `` `code` `` → `{{code}}`
  - Code blocks converted: ` ```lang` → `{code:lang}...{code}`
  - Tables converted: `|Header|` → `||Header||`
- Internal links converted to Confluence URLs or marked "(nội bộ)"

### Post-Publish Validation
- Open Confluence page and verify rendering (especially bullet points)
- `public_confluence_url` updated with live page link
- `published_at` set to `YYYY-MM-DD`
- Changes committed to repo

### Common Errors Reference

**"Bullet points render as continuous text"**
- **Cause**: Using `content_format='markdown'` with bullet lists
- **Fix**: Switch to `content_format='wiki'` and convert bullets to `*` syntax

**"Error calling tool 'update_page'" (no details)**
- **Likely causes**: Storage format with invalid HTML, encoding issues, schema violations
- **Fix**: Switch to wiki format, validate content for special characters

**"Nested lists not rendering"**
- **Cause**: Markdown nested list syntax not supported
- **Fix**: Use wiki format with `**` for level 2, `***` for level 3
