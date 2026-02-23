# MSAM Skill for OpenClaw

**Production-grade cognitive memory architecture for AI agents.**

---

## Quick Start

### Install MSAM

```bash
# Install Python 3.11+ (required)
# Ubuntu/Debian:
sudo apt update && sudo apt install python3.11
# or use pyenv:
pyenv install 3.11

# Install MSAM
pip install msam

# Initialize database
python -m msam.init_db
```

### Configure

```bash
# Copy example config
mkdir -p ~/.msam
pip show msam | grep Location | xargs -I{} cp {}/msam.example.toml ~/.msam/msam.toml

# Set API key (choose one)
export NVIDIA_NIM_API_KEY="your-key"  # Get from https://build.nvidia.com
# or
export OPENAI_API_KEY="your-key"
```

---

## Usage Examples

### Store Memory

```bash
msam store "The user prefers dark mode"
msam store --stream semantic "User's email: ciao@openclaw.ai"
msam batch "atom1" "atom2" "atom3"
```

### Retrieve Memory

```bash
# Query (confidence-gated)
msam query "What are user's preferences?"

# Output:
# HIGH (≥0.45): 140-176 tokens, full results
# MEDIUM (≥0.30): 91-131 tokens, top 3 atoms
# LOW (≥0.15): 0-33 tokens, 1 atom, advisory
# NONE (<0.15): 0 tokens, "I don't know"
```

### Session Startup

```bash
# Get compressed context (51-90 tokens vs 7,327 baseline)
msam context
```

### Lifecycle

```bash
# Run decay cycle
msam decay

# Preview forgetting
msam forgetting --dry-run

# Statistics
msam stats
msam analytics
```

---

## Core Concepts

### 4 Memory Streams

| Stream | Contains | Decay |
|---------|----------|--------|
| Semantic | Facts, preferences | Slow |
| Episodic | Events, conversations | Medium |
| Procedural | How-to, skills | Very slow |
| Working | Current session | Deleted at end |

### Confidence Gating

| Tier | Similarity | Tokens |
|-------|-------------|---------|
| HIGH | ≥ 0.45 | 140-176 |
| MEDIUM | ≥ 0.30 | 91-131 |
| LOW | ≥ 0.15 | 0-33 |
| NONE | < 0.15 | 0 |

### Lifecycle

```
ACTIVE → FADING → DORMANT → TOMBSTONE
(No permanent deletion)
```

---

## Performance

| Metric | Result |
|--------|---------|
| Token Savings | 98.8% (112 vs 9301 tokens) |
| MRR | 0.328 (vs 0.314 raw, +4.4% better) |
| Latency | 2.1ms (vs 5.4ms raw, 2.5x faster) |
| Absent Detection | 75% (honest unknowns) |

---

## Resources

- **Full Documentation:** `SKILL.md`
- **GitHub:** https://github.com/jadenschwab/msam
- **Analysis:** `msam-analysis.md`
- **Benchmark:** `msam-benchmark-results.md`

---

## License

MIT
