# OpenClaw Team Conventions

---

## Purpose

This document encodes our team conventions, patterns, and architectural decisions for AI agents to follow. This is the foundation of agentic engineering for OpenClaw.

---

## Core Principles

### 1. Structure Amplifies Capability
> An agent is only as effective as the workflow and codebase it's given to work within.

**Implication:**
- Well-documented patterns are more valuable than individual solutions
- Convention-driven development is faster than ad-hoc coding
- Reusable skills compound in value over time

### 2. Process as a Tool, Not a Tax
**Automate:**
- Tickets/Issue tracking
- PR templates
- Changelogs
- Documentation generation

**Human Focus:**
- High-level architecture
- Orchestration
- Quality gates (PR review)

### 3. Git-Based Workflow
All work flows through Git with Pull Requests for:
- Code review
- Knowledge capture
- Architectural alignment

---

## Coding Conventions

### File Naming

| Type | Pattern | Example |
|-------|---------|----------|
| Skills | `skills/{name}/SKILL.md` | `skills/browser-use/SKILL.md` |
| Documentation | `NAME.md` (uppercase) | `MEMORY.md`, `AGENTS.md` |
| Config | `*.config.json` | `openclaw.json` |
| Scripts | `{name}.sh` | `deploy.sh` |

### Code Style

**Python:**
- Use type hints where appropriate
- Docstrings for all functions
- Error handling with context
- Logging over print statements

**Markdown:**
- Headers start at H2 (`##`)
- Use tables for structured data
- Code blocks with language tags
- Bullet lists for readability

**Bash:**
- Set `-e` for error handling
- Use `set -euo pipefail`
- Comment non-obvious commands
- Use absolute paths when in doubt

---

## Project Structure

### Standard Layout

```
project/
├── SKILL.md              # Skill definition
├── README.md             # Quick start
├── EXAMPLES.md           # Usage examples
├── scripts/              # Helper scripts
├── templates/            # Code templates
└── tests/                # Tests (if applicable)
```

### Workspace Layout

```
~/pi-mono-workspace/
├── skills/               # All skills
├── AGENTS.md            # Agent instructions
├── SOUL.md              # Agent persona
├── USER.md              # User preferences
├── MEMORY.md             # Long-term memory
├── memory/              # Daily logs
└── .git/                # Version control
```

---

## Git Workflow

### Branch Strategy

- `main` - Production-ready code
- `feature/{name}` - Feature development
- `fix/{issue}` - Bug fixes
- `doc/{topic}` - Documentation updates

### Commit Messages

```
{type}({scope}): {message}

# Examples:
feat(browser-use): Add natural language browser automation skill
fix(gateway): Resolve connection timeout issue
docs(readme): Update installation instructions
refactor(trading): Extract signal logic into module
```

### Pull Request Template

```markdown
## Description
{What this PR does and why}

## Changes
- {Bullet list of changes}

## Type
- [ ] Feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation

## Checklist
- [ ] Code follows conventions
- [ ] Tests pass (if applicable)
- [ ] Documentation updated
- [ ] Ready for review
```

---

## Skill Conventions

### SKILL.md Format

```markdown
---
name: {skill-name}
description: "{What this skill does}"
metadata: {
  "openclaw": {
    "requires": {
      "tools": [{tools}],
      "runtime": "node|python"
    },
    "tags": [{relevant-tags}]
  }
}
---

# {Skill Name}

{Complete documentation}
```

### Required Sections

| Section | Description |
|----------|-------------|
| What It Is | High-level description |
| Why It Matters | Value proposition |
| Usage | How to use it |
| Examples | Code snippets or prompts |
| Best Practices | Guidelines for use |

---

## Documentation Conventions

### Memory Files

- `MEMORY.md` - Curated long-term memory (DM sessions only)
- `memory/YYYY-MM-DD.md` - Daily append-only logs
- `memory/daily/YYYY-MM-DD.md` - Organized daily logs

### Documentation Priority

1. **README.md** - First thing to read
2. **SKILL.md** - Skill documentation
3. **EXAMPLES.md** - Usage examples
4. **Memory** - Team knowledge and decisions

---

## Quality Gates

### Before Commit

- [ ] Code follows conventions
- [ ] Documentation is updated
- [ ] Tests pass (if applicable)
- [ ] No sensitive data committed
- [ ] Commit message follows format

### Before Merge

- [ ] Code review completed
- [ ] Architectural alignment verified
- [ ] No breaking changes without version bump
- [ ] Team knowledge captured

---

## Error Handling

### Python
```python
try:
    {operation}
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    # Handle gracefully
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Fallback behavior
```

### Bash
```bash
set -euo pipefail

{command} || {
    echo "Command failed: $?"
    # Cleanup or fallback
    exit 1
}
```

---

## Security Conventions

### Never Commit
- API keys
- Passwords
- Secrets
- Personal data
- `.env` files with secrets

### Use Environment Variables
```bash
export API_KEY="${API_KEY:-default}"
export DB_PASSWORD="${DB_PASSWORD:?DB_PASSWORD required}"
```

### Secrets Management
- Use `~/.openclaw/credentials/` for OpenClaw secrets
- Use `~/.aws/` for AWS credentials
- Use Docker secrets for containerized apps

---

## Testing Conventions

### When to Write Tests

- New strategy implementation
- Critical business logic
- Data processing functions
- API endpoints

### Test Structure

```python
def test_{function}_{scenario}():
    # Arrange
    input_data = {...}

    # Act
    result = function(input_data)

    # Assert
    assert result == expected
```

---

## Communication Conventions

### Slack/Discord

- Use code blocks for code
- Use tables for structured data
- Use emoji for status (✅, ❌, ⚠️)
- Keep messages concise

### Git Messages

- Past tense: "Added feature" not "Add feature"
- Imperative mood for PR titles
- Conventional Commits format

---

## Decision Log

### T013: Graceful Degradation
**Decision:** Always wrap critical init in try/except blocks
**Context:** Trading system high availability

### T014: RSI Veto Protocol
**Decision:** Add hard RSI filter for impulse strategies
**Context:** Preventing impulsive entries at local tops

### T015: Falling Knife Paradox
**Decision:** Veto buy if (RSI < 40) AND (Price < 200MA)
**Context:** Avoid catching falling knives in downtrends

---

## Evolution

This document evolves as we learn. Add decisions, patterns, and conventions here.

**Last Updated:** 2026-02-19

---

*Team conventions encoded for agentic engineering* 📋
