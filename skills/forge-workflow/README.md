# Forge Workflow Skill

Structured development pipeline for agentic engineering.

---

## What It Is

The Forge Workflow is an open-standard skill that guides agents through a complete development pipeline:

```
Setting Foundations → Planning → Implementing → Self-Reviewing → Documenting
```

---

## Quick Start

Just follow the 5 phases - the skill guides you through each step:

1. **Setting Foundations** - Create project structure
2. **Planning** - Define requirements and architecture
3. **Implementing** - Write code following conventions
4. **Self-Reviewing** - Quality check before commit
5. **Documenting** - Generate docs automatically

---

## Why Use Forge Workflow

| Ad-hoc Coding | Forge Workflow |
|---------------|----------------|
| Fast but fragile | Fast and robust |
| Documentation skipped | Documentation automated |
| No quality gates | Quality checks at each phase |
| One-off solutions | Reusable patterns |
| Hard to maintain | Easy to extend |

---

## When to Use

### New Features
Use all 5 phases for new features or skills.

### Bug Fixes
Skip Phase 1 (foundations exist), use phases 2-5.

### Documentation Updates
Skip phases 1-3, use phases 4-5.

### Refactoring
Use phases 2-5 (plan, implement, review, document).

---

## Key Benefits

1. **Structure Amplifies Capability**
   - Well-documented patterns are more valuable than one-off solutions
   - Skills compound in value over time

2. **Process as a Tool**
   - Automate tickets, PR templates, changelogs
   - Focus human effort on architecture and orchestration

3. **Quality Gates**
   - Self-reviewing ensures nothing is skipped
   - PR review becomes quality gate, not bottleneck

4. **Team Knowledge**
   - Conventions encoded in TEAM_CONVENTIONS.md
   - Patterns become reusable across the workspace

---

## Integration

### Required Files

| File | Purpose |
|-------|----------|
| `TEAM_CONVENTIONS.md` | Coding and workflow standards |
| `SKILL.md` | Skill definition and metadata |
| `README.md` | Quick start guide |
| `EXAMPLES.md` | Usage examples |

### Git Integration

```bash
# Feature branch
git checkout -b feature/new-skill

# Work through phases
# ... coding ...

# Conventional commits
git commit -m "forge(implement): Add core functionality"

# Merge after review
git checkout main
git merge feature/new-skill
```

---

## Phase Checklist

Use this quick reference for each phase:

### Phase 1: Foundations
- [ ] Create directory structure
- [ ] Initialize Git (if needed)
- [ ] Create SKILL.md
- [ ] Set up logging

### Phase 2: Planning
- [ ] Define requirements
- [ ] Design architecture
- [ ] Identify dependencies
- [ ] Plan testing approach

### Phase 3: Implementing
- [ ] Follow code conventions
- [ ] Add error handling
- [ ] Write tests
- [ ] Commit frequently

### Phase 4: Self-Reviewing
- [ ] Code quality check
- [ ] Tests pass
- [ ] No TODOs left
- [ ] No secrets committed

### Phase 5: Documenting
- [ ] README.md complete
- [ ] SKILL.md updated
- [ ] EXAMPLES.md added
- [ ] Changelog updated

---

## Success Criteria

A Forge workflow is complete when:
- All 5 phases executed
- Code follows TEAM_CONVENTIONS.md
- Documentation is complete
- Ready for PR review

---

## Examples

See `EXAMPLES.md` for:
- Creating a new skill
- Adding a feature
- Fixing a bug

---

*Forge workflow - structure amplifies capability* 🔨
