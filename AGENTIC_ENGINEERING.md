# Agentic Engineering in Practice

---

## Source
Martin Gratzer - "Forging a Workflow: Agentic Engineering in Practice"

---

## Core Thesis

Software engineering is shifting from manual coding to "agentic engineering"—a workflow where AI agents don't just write functions but execute an entire development process.

---

## Key Takeaways

### 1. From Assistant to Agent

**The Real Shift:**
> Stop using AI for one-off prompts → Start encoding team conventions into reusable "skills"

**Why It Matters:**
- Agent is only as effective as the workflow and codebase it's given to work within
- Structure amplifies capability

### 2. The "Colorburst" Experiment

**What:**
AI-powered coloring page generator built from planning to production.

**Finding:**
> Agents excel when a project has a well-defined structure and clear documentation to ground them.

### 3. Process as a Tool, Not a Tax

**Traditional Overhead:**
- Tickets
- PR templates
- Changelogs

**Agentic Engineering:**
Automates these tasks, ensuring high-quality documentation and testing are maintained effortlessly.

### 4. The "Forge" Workflow

Gratzer introduced **Forge**—a set of open-standard skills that handle a project pipeline:

1. **Setting Foundations**
   - Project structure
   - Conventions
   - Tooling

2. **Planning**
   - Requirements gathering
   - Architecture decisions
   - Dependencies

3. **Implementing**
   - Coding with patterns
   - Following conventions
   - Self-documentation

4. **Self-Reviewing**
   - Code quality checks
   - Testing
   - Performance analysis

5. **Documenting**
   - Auto-generated docs
   - API documentation
   - Changelogs

### 5. The Human's Evolving Role

**From:**
- Writing code manually
- Managing tickets
- Creating templates

**To:**
- High-level architecture
- Orchestration
- Acting as final quality gate

### 6. Why Pull Requests Remain Essential

Human review is still needed to catch:
- ✅ Cross-cutting concerns (security, performance)
- ✅ Shared team knowledge
- ✅ Architectural alignment

**The PR becomes the quality gate**, not a bottleneck.

---

## Core Principle

> While AI increases speed, **structure amplifies capability**.

An agent is only as effective as:
1. The workflow it follows
2. The codebase it operates within
3. The conventions it understands

---

## Application to OpenClaw

### What We Already Have

| Component | Status |
|-----------|--------|
| Skills system | ✅ SKILL.md files |
| Multiple agents | ✅ Rayan, trading, etc. |
| Clear conventions | ✅ AGENTS.md, SOUL.md, USER.md, MEMORY.md |
| Git-based workflow | ✅ PR-based development |

### What We Need

1. **Encode Team Conventions into Skills**
   - Document coding patterns
   - Create skill templates
   - Define workflows

2. **Define Project Structure for Agents**
   - Standard layouts
   - Configuration patterns
   - Entry points

3. **Create Forge-Style Workflow Skills**
   - Setting Foundations skill
   - Planning skill
   - Implementing skill
   - Self-Reviewing skill
   - Documenting skill

4. **Use PR Review as Quality Gate**
   - Security review
   - Architecture alignment
   - Team knowledge capture

---

## Next Steps

### Phase 1: Foundation
- [ ] Define OpenClaw coding conventions
- [ ] Create skill template structure
- [ ] Document project layout patterns

### Phase 2: Skills
- [ ] Create "Forge" workflow skills
- [ ] Encode team patterns
- [ ] Test agent capabilities

### Phase 3: Workflow
- [ ] Integrate skills into agents
- [ ] Automate documentation generation
- [ ] Set up PR review process

---

## Summary

**Agentic Engineering** is about:
1. Moving from prompts to skills
2. Building structure that amplifies AI capability
3. Automating traditional overhead
4. Human as orchestrator, not coder
5. PR review as quality gate

> AI increases speed. Structure amplifies capability.

---

*Inspired by Martin Gratzer's article*
