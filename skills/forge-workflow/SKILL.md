---
name: forge-workflow
description: "Forge-style workflow skill for agentic development - setting foundations, planning, implementing, self-reviewing, and documenting"
metadata: {
  "openclaw": {
    "requires": {
      "tools": ["write", "read", "exec", "git"],
      "runtime": "node"
    },
    "tags": ["workflow", "agentic", "forge", "development"]
  }
}
---

# Forge Workflow Skill

## What It Is

The Forge Workflow is an open-standard skill for the complete development pipeline: **Setting Foundations → Planning → Implementing → Self-Reviewing → Documenting**.

This skill guides agents through a structured development process, ensuring high-quality, documented code that follows team conventions.

---

## Why It Matters

### The Problem
- Ad-hoc coding is fast but fragile
- One-off prompts don't build reusable skills
- Documentation is often skipped under pressure

### The Solution
- Structured workflow ensures quality at each stage
- Team conventions are encoded and followed
- Documentation is automated, not skipped
- Skills compound in value over time

---

## Phase 1: Setting Foundations

### Purpose
Establish project structure and conventions before writing any code.

### Checklist

- [ ] Create project directory structure
- [ ] Initialize Git repository (if needed)
- [ ] Review TEAM_CONVENTIONS.md
- [ ] Create SKILL.md with required metadata
- [ ] Set up logging/config structure
- [ ] Define code style and patterns

### Output
```
project/
├── SKILL.md
├── README.md
├── src/
├── tests/
└── scripts/
```

---

## Phase 2: Planning

### Purpose
Define requirements, architecture, and approach before implementation.

### Checklist

- [ ] Define clear requirements
- [ ] Identify dependencies and constraints
- [ ] Design architecture/components
- [ ] Plan testing approach
- [ ] Document edge cases to handle

### Output
```markdown
## Requirements
{What needs to be built}

## Architecture
{How components fit together}

## Approach
{Step-by-step implementation plan}
```

---

## Phase 3: Implementing

### Purpose
Write code following conventions and patterns.

### Checklist

- [ ] Follow TEAM_CONVENTIONS.md style guide
- [ ] Use appropriate error handling
- [ ] Add type hints (Python) or types (TypeScript)
- [ ] Include logging/debugging output
- [ ] Handle edge cases identified in planning
- [ ] Write tests for critical functions
- [ ] Commit frequently with conventional messages

### Code Template

```python
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class Feature:
    """{Brief description}"""

    def __init__(self):
        """Initialize with required config."""
        logger.info(f"Initializing {self.__class__.__name__}")

    def execute(self):
        """Main execution logic."""
        try:
            # Implementation
            pass
        except Exception as e:
            logger.error(f"Execution failed: {e}")
            raise
```

---

## Phase 4: Self-Reviewing

### Purpose
Quality check before committing to main.

### Checklist

- [ ] Code follows TEAM_CONVENTIONS.md
- [ ] Error handling is comprehensive
- [ ] Logging is appropriate (not over/under-logging)
- [ ] Tests cover critical paths
- [ ] No hardcoded secrets or paths
- [ ] Documentation is complete
- [ ] No TODO comments left in production code

### Review Questions

- Does this solve the original requirement?
- Are there edge cases not handled?
- Is error handling graceful?
- Is the code readable and maintainable?

---

## Phase 5: Documenting

### Purpose
Auto-generate documentation as part of development, not as an afterthought.

### Checklist

- [ ] README.md is complete
- [ ] SKILL.md has required sections
- [ ] EXAMPLES.md has usage examples
- [ ] CHANGELOG.md is updated
- [ ] Code has docstrings
- [ ] Complex functions have inline comments

### Documentation Template

```markdown
# Feature Name

## What It Is
{Brief description}

## How It Works
{Technical details}

## Usage
```bash
# Example command
{command}
```

## Requirements
{Dependencies and setup}
```

---

## Forge Workflow Example

### Task: Create a new trading strategy

#### Phase 1: Setting Foundations
```
✅ Created directory: src/strategies/new_strategy/
✅ Created SKILL.md with metadata
✅ Review TEAM_CONVENTIONS.md for patterns
```

#### Phase 2: Planning
```
✅ Requirements: EMA crossover with RSI filter
✅ Architecture: SignalGenerator → Strategy → Backtest
✅ Approach: Use backtesting.py library, add unit tests
```

#### Phase 3: Implementing
```
✅ Implemented SignalGenerator class with type hints
✅ Added error handling for data loading
✅ Wrote tests for signal logic
✅ Committed: feat(strategy): Add SignalGenerator
```

#### Phase 4: Self-Reviewing
```
✅ Code follows conventions
✅ Error handling comprehensive
✅ Tests pass
✅ No TODOs left
```

#### Phase 5: Documenting
```
✅ README.md complete
✅ SKILL.md updated with usage
✅ EXAMPLES.md added
```

---

## Quick Reference

| Phase | Key Action | Artifact |
|--------|-------------|-----------|
| Setting Foundations | Create structure | Directory layout, SKILL.md |
| Planning | Design approach | Plan document |
| Implementing | Write code | Source files, tests |
| Self-Reviewing | Quality check | Review checklist |
| Documenting | Write docs | README, EXAMPLES.md |

---

## Integration with Git

### Branch Strategy
- `feature/{name}` for implementation
- Merge to `main` after self-reviewing

### Commit Messages
```
forge(foundations): Create project structure
forge(planning): Design architecture
forge(implement): Implement core logic
forge(review): Self-review complete
forge(document): Update documentation
```

---

## Use Cases

### New Skill Development
Follow all 5 phases to build a complete, documented skill.

### Feature Addition
Skip Phase 1 (foundations exist), implement phases 2-5.

### Bug Fix
Skip Phase 1, implement fix, review, document.

---

## Common Patterns

### Error Handling
```python
try:
    result = operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    # Graceful fallback
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

### Logging
```python
logger.debug("Detailed info for debugging")
logger.info("Normal flow information")
logger.warning("Potential issue detected")
logger.error("Error requiring attention")
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-skill

# Work through phases
# ... coding ...

# Commit each phase
git add .
git commit -m "forge(implement): Add core functionality"

# Review and merge
git checkout main
git merge feature/new-skill
```

---

## Success Criteria

A Forge workflow is complete when:

- [ ] All 5 phases executed
- [ ] Code follows TEAM_CONVENTIONS.md
- [ ] Documentation is complete (README, SKILL.md, EXAMPLES.md)
- [ ] Tests pass (if applicable)
- [ ] Git history shows conventional commits
- [ ] Ready for PR review

---

## Notes

- This skill works with TEAM_CONVENTIONS.md
- Use the workflow for all non-trivial features
- Adapt phases based on task complexity
- Quality gates ensure nothing is skipped

---

*Forge workflow - structured development for agentic engineering* ⚒️
