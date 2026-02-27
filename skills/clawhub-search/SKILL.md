# SKILL.md - clawhub-search

## Name
clawhub-search

## Description
Search ClawHub (clawhub.ai) for OpenClaw skills. Find and discover skills by keyword, tag, or category.

## Usage

```bash
# Search for skills
clawhub search "<query>" [--limit N]

# Examples
clawhub search "simulator"
clawhub search "arxiv" --limit 10
clawhub search "docker sandbox"
```

## Parameters

- `query` (required): Search term to find skills
- `limit` (optional): Maximum results to return (default: 20)

## Output

Returns a list of matching skills with:
- Skill name
- Description  
- Relevance score
- Install command

## Examples

**Search for simulator skills:**
```
clawhub search "simulator"
```

**Search for research skills:**
```
clawhub search "arxiv"
```

**Search with limit:**
```
clawhub search "sandbox" --limit 10
```

## Installation

```bash
clawdhub search "<query>"
```

To install a found skill:
```bash
clawdhub install <skill-slug>
```

## Notes

- ClawHub is the public skill registry for OpenClaw
- All skills are open source and community-contributed
- Requires clawdhub CLI installed (`npm install -g clawhub` aliased as clawdhub)
- Skills install to `./skills` directory by default

## Registry
https://clawhub.ai

## Author
Platform Engineer Kelsey Hightowel