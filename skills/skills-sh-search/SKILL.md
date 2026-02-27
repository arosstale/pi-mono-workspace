# SKILL.md - skills-sh-search

## Name
skills-sh-search

## Description
Search skills.sh (Vercel Labs) for AI agent skills. Discover capabilities from the Vercel ecosystem.

## Usage

```bash
# Search for skills
npx skills search "<query>"

# Examples
npx skills search "simulator"
npx skills search "testing"
npx skills search "webapp"
```

## Parameters

- `query` (required): Search term to find skills

## Output

Returns matching skills from the skills.sh leaderboard with:
- Skill ranking
- Install count
- Owner/repo path
- Description

## Examples

**Search for testing skills:**
```
npx skills search "test"
```

**Search for React skills:**
```
npx skills search "react"
```

**Add a found skill:**
```
npx skills add <owner/repo>
```

## Installation

```bash
# Install the skills CLI
npm install -g skills

# Or use npx (no install needed)
npx skills search "<query>"
```

To install a found skill:
```bash
npx skills add <owner/repo>
```

## Notes

- skills.sh is Vercel Labs' skill registry
- Skills ranked by anonymous telemetry (install counts)
- Top skills: find-skills (336K), vercel-react-best-practices (171K), web-design-guidelines (130K)
- Completely open source at github.com/vercel-labs/skills
- Different ecosystem from ClawHub

## Registry
https://skills.sh

## Author
Platform Engineer Kelsey Hightowel