# SKILL.md - skill-finder

## Name
skill-finder

## Description
Universal skill discovery tool. Search both ClawHub and skills.sh registries simultaneously to find the best OpenClaw and AI agent skills.

## Usage

```bash
# Search both registries
skill-finder "<query>" [--clawhub-limit N] [--skills-sh-limit N]

# Examples
skill-finder "simulator"
skill-finder "arxiv" --clawhub-limit 10
skill-finder "testing" --skills-sh-limit 5
```

## Parameters

- `query` (required): Search term to find skills across both registries
- `clawhub-limit` (optional): Max results from ClawHub (default: 10)
- `skills-sh-limit` (optional): Max results from skills.sh (default: 10)

## Output

**Combined results from both registries:**

### ClawHub Results
- Skill name and slug
- Relevance score
- Description
- Install command: `clawdhub install <slug>`

### skills.sh Results  
- Skill ranking
- Install count
- Owner/repo path
- Install command: `npx skills add <owner/repo>`

## Examples

**Find simulator skills:**
```
skill-finder "simulator"
```

**Find research/arxiv skills:**
```
skill-finder "arxiv"
```

**Limited results:**
```
skill-finder "sandbox" --clawhub-limit 5 --skills-sh-limit 5
```

## How It Works

1. Queries ClawHub: `clawdhub search "<query>" --limit N`
2. Queries skills.sh: `npx skills search "<query>"`
3. Combines and deduplicates results
4. Ranks by relevance and popularity
5. Returns unified list with install commands

## Installation Commands

**From ClawHub:**
```bash
clawdhub install <skill-slug>
```

**From skills.sh:**
```bash
npx skills add <owner/repo>
```

## Registry Comparison

| Feature | ClawHub | skills.sh |
|---------|---------|-----------|
| Ecosystem | OpenClaw | Vercel/AI SDK |
| CLI | `clawdhub` | `npx skills` |
| Focus | OpenClaw agents | General AI agents |
| Top Skills | arxiv, ios-simulator | find-skills, react-best-practices |
| Install Path | `./skills/` | `./skills/` |

## Notes

- Two different skill ecosystems with different strengths
- ClawHub: OpenClaw-specific skills (Discord, messaging, agent tools)
- skills.sh: General AI/dev skills (React, testing, webapp)
- Both registries are public and open source
- Use both to maximize skill discovery

## Registries
- ClawHub: https://clawhub.ai
- skills.sh: https://skills.sh

## Author
Platform Engineer Kelsey Hightowel