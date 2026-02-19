# Forge Workflow Examples

Copy and adapt these examples for your development tasks.

---

## Example 1: Creating a New Skill

### Task
Create a browser automation skill for scraping LinkedIn job postings.

### Phase 1: Setting Foundations

```bash
# Create directory structure
mkdir -p skills/linkedin-scraper/{src,tests,scripts}

# Create SKILL.md with metadata
cat > skills/linkedin-scraper/SKILL.md << 'EOF'
---
name: linkedin-scraper
description: "Scrape LinkedIn job postings using browser automation"
metadata: { "openclaw": { "requires": { "tools": ["browser"] } }
---
EOF

# Create README.md
touch skills/linkedin-scraper/README.md
```

**Output:** ✅ Structure created, metadata defined

### Phase 2: Planning

```markdown
## Requirements
- Navigate to LinkedIn Jobs
- Search for given job title and location
- Extract first 10 results
- Return: title, company, location, link

## Architecture
```
Scraper
├── BrowserClient (using browser tool)
├── Parser (extract data from HTML)
└── Exporter (save to CSV)
```

## Approach
1. Use browser tool to navigate to LinkedIn
2. Fill search form with job title and location
3. Extract job listings from results page
4. Parse to extract title, company, location, link
5. Save to CSV
```

**Output:** ✅ Requirements defined, architecture planned

### Phase 3: Implementing

```python
# src/scraper.py
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class LinkedInScraper:
    """Scrape LinkedIn job postings."""

    def __init__(self, job_title: str, location: str):
        self.job_title = job_title
        self.location = location

    async def search(self) -> list[dict]:
        """Search and extract job postings."""
        logger.info(f"Searching for: {self.job_title} in {self.location}")
        # Implementation using browser tool
        jobs = await self._extract_jobs()
        logger.info(f"Found {len(jobs)} jobs")
        return jobs
```

**Output:** ✅ Code written following TEAM_CONVENTIONS.md

### Phase 4: Self-Reviewing

**Review Checklist:**
- ✅ Code follows TEAM_CONVENTIONS.md style
- ✅ Type hints included
- ✅ Error handling with logging
- ✅ No TODOs left
- ✅ Ready for testing

**Output:** ✅ Quality verified

### Phase 5: Documenting

```markdown
# LinkedIn Scraper

## What It Is
Scrape LinkedIn job postings using OpenClaw's browser tool.

## Usage
> "Search LinkedIn for AI Engineer jobs in San Francisco and extract the first 10 results"

## Requirements
- OpenClaw browser tool access
- LinkedIn account (for full results)
```

**Output:** ✅ Documentation complete

---

## Example 2: Adding a Feature

### Task
Add email notification to RBI optimization agent.

### Phase 1: Setting Foundations
**Skip** - Foundations exist for RBI agent.

### Phase 2: Planning

```markdown
## Requirements
- Send email when optimization completes
- Include strategy name, version, and performance delta
- Handle email sending errors gracefully

## Architecture
```
OptimizationAgent
└── NotificationService (new)
    └── EmailClient
```

## Approach
1. Create NotificationService class
2. Add send_optimization_email() method
3. Integrate into optimization workflow
4. Add error handling for email failures
```

### Phase 3: Implementing

```python
# notification_service.py
class NotificationService:
    """Send email notifications."""

    def __init__(self, smtp_config: dict):
        self.smtp_config = smtp_config
        self.client = smtplib.SMTP(**smtp_config)

    def send_optimization_email(self, result: OptimizationResult):
        """Send optimization completion email."""
        try:
            message = self._build_message(result)
            self.client.send_message(message)
            logger.info(f"Email sent: {result.strategy_name}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            # Continue execution - don't fail optimization
```

### Phase 4: Self-Reviewing

**Review:**
- ✅ Error handling graceful (doesn't fail optimization)
- ✅ Logging for debugging
- ✅ Email template clear
- ✅ No SMTP secrets hardcoded

### Phase 5: Documenting

Update SKILL.md with new notification feature.

---

## Example 3: Fixing a Bug

### Task
Fix RBI execution agent timeout handling.

### Phase 1: Setting Foundations
**Skip** - File exists.

### Phase 2: Planning

```markdown
## Requirements
- Timeout should actually kill the subprocess
- Process cleanup should be guaranteed
- Resources should be released

## Approach
1. Use `subprocess.Popen()` with explicit cleanup
2. Add `timeout` parameter
3. Ensure `kill()` is called in finally block
4. Log timeout events
```

### Phase 3: Implementing

```python
# Fix timeout handling
def execute_backtest(self, code_path: Path):
    """Execute with proper timeout and cleanup."""
    process = None
    try:
        process = subprocess.Popen(
            ["python", str(code_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate(timeout=self.timeout)
        return self._parse_result(stdout)

    except subprocess.TimeoutExpired:
        if process:
            process.kill()
            process.wait()
        logger.error(f"Timeout after {self.timeout}s")
        return ExecutionResult(success=False, error="Timeout")
    finally:
        # Ensure cleanup
        if process and process.poll() is None:
            process.kill()
```

### Phase 4: Self-Reviewing

**Review:**
- ✅ Process cleanup in finally block
- ✅ Timeout properly handled
- ✅ Error logging
- ✅ Resources released

### Phase 5: Documenting

Update CHANGELOG.md with bug fix entry.

---

## Example 4: Quick One-Liner Changes

For trivial changes, compress phases:

```bash
# All phases in one commit
git add .
git commit -m "fix(readme): Typo in installation section"
```

---

## Phase Summaries

### When to Skip Phases

| Task | Phases |
|-------|---------|
| New skill | 1-5 (all phases) |
| New feature | 2-5 (skip foundations) |
| Bug fix | 2-5 (skip foundations) |
| Documentation only | 4-5 (skip foundations, planning, implementation) |
| Refactoring | 2-5 (skip foundations) |

---

## Common Patterns

### Error Handling Template

```python
try:
    result = operation()
except SpecificError as e:
    logger.error(f"Specific error: {e}")
    # Handle specifically
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

### Git Commit Template

```bash
# Phase-specific commits
git add .
git commit -m "forge({phase}): {description}"

# Examples:
git commit -m "forge(planning): Design scraper architecture"
git commit -m "forge(implement): Add core scraper logic"
git commit -m "forge(review): Quality check complete"
```

---

## Tips

1. **Start with Phase 1** for new projects - it saves time
2. **Write planning in markdown** - easy to convert to docs
3. **Review code before committing** - catch issues early
4. **Document as you code** - not as an afterthought
5. **Follow TEAM_CONVENTIONS.md** - ensures consistency

---

## Checklist for Each Phase

Copy this for quick reference:

### Phase 1: Foundations
- [ ] Directory created
- [ ] SKILL.md with metadata
- [ ] README.md created

### Phase 2: Planning
- [ ] Requirements defined
- [ ] Architecture designed
- [ ] Dependencies identified

### Phase 3: Implementing
- [ ] Code follows conventions
- [ ] Error handling added
- [ ] Tests written

### Phase 4: Self-Reviewing
- [ ] Quality checklist passed
- [ ] No TODOs left
- [ ] No secrets committed

### Phase 5: Documenting
- [ ] README.md updated
- [ ] SKILL.md complete
- [ ] Examples added

---

*Follow Forge workflow for structured, high-quality development* 🔨
