# MSAM (Multi-Stream Adaptive Memory)

A production-grade cognitive memory architecture for AI agents with 99.3% token savings, ACT-R activation scoring, and bi-temporal decay.

---

## What is MSAM?

MSAM gives AI agents persistent, structured memory that self-regulates what it stores, how it retrieves, and when it forgets. Knowledge lives as discrete atoms across **4 cognitive streams**:

| Stream | Contains | Decay Rate |
|---------|----------|------------|
| Semantic | Facts, preferences, decisions | Slow (stable knowledge) |
| Episodic | Events, conversations, experiences | Medium (consolidates over time) |
| Procedural | How-to knowledge, skills, patterns | Very slow (skills persist) |
| Working | Current session context | Session-scoped (deleted at end) |

---

## When to Use This Skill

Use MSAM when you need:
- **Persistent memory** across sessions for an agent
- **Token-efficient retrieval** (98.8% savings vs flat files)
- **Confidence-gated output** (honest "I don't know" responses)
- **Biological decay model** (memory fades over time, nothing is permanently deleted)
- **Multi-agent isolation** (multiple agents share one MSAM instance without interference)

---

## Installation

### Prerequisites
- Python 3.11+ (uses `tomllib` from stdlib)
- An embedding provider (choose one):
  - **NVIDIA NIM** (free tier, recommended): https://build.nvidia.com
  - **OpenAI** (`text-embedding-3-small`)
  - **ONNX Runtime** (local, no API key)
  - **sentence-transformers** (local, no API key)

### Quick Install

```bash
# Install MSAM
pip install msam

# Or install with extras for specific providers:
pip install "msam[anthropic,groq,google-genai]"

# Initialize databases
python -m msam.init_db
```

### Configure

```bash
# Copy example config
mkdir -p ~/.msam
cp /path/to/msam.example.toml ~/.msam/msam.toml

# Edit ~/.msam/msam.toml
# Key section is [embedding]:
[embedding]
provider = "nvidia-nim"  # or "openai", "onnx", "local"
model = "nvidia/nv-embedqa-e5-v5"

# Set env var for API keys
export NVIDIA_NIM_API_KEY="your-key"
# or
export OPENAI_API_KEY="your-key"
```

---

## Usage Patterns

### 1. Store Memory

```bash
# Store a semantic fact
msam store "The user prefers dark mode and concise responses"

# Store with explicit stream
msam store --stream semantic "User's email: ciao@openclaw.ai"

# Batch store
msam batch "atom1" "atom2" "atom3"

# Store negative knowledge
msam negative "X is NOT Y"
```

### 2. Retrieve Memory (Confidence-Gated)

```bash
# Query (returns atoms + confidence tier)
msam query "What are the user's preferences?"

# Output format:
# - HIGH (≥0.45): Full results, 140-176 tokens, ≤12 triples
# - MEDIUM (≥0.30): Top 3 atoms, 91-131 tokens, ≤8 triples
# - LOW (≥0.15): 1 atom, 0-33 tokens, no triples, advisory
# - NONE (<0.15): Empty, advisory only

# Hybrid search (atoms + triples)
msam hybrid "How does the user deploy code?"

# Diverse retrieval (optimizes for variety)
msam diverse "What projects is the user working on?"

# Explain scoring breakdown
msam explain "What is the user's email?"
```

### 3. Session Startup (Compressed Context)

```bash
# Get compressed startup context (51-90 tokens vs 7,327 baseline)
msam context

# Returns:
# - Delta encoding (changes since last session)
# - Subatom extraction (sentence-level)
# - Codebook compression (entity shortening)
# - Semantic deduplication
```

### 4. Lifecycle Management

```bash
# Run decay cycle (hourly recommended)
msam decay

# Preview forgetting candidates
msam forgetting --dry-run

# Sleep-inspired consolidation
msam consolidate

# Snapshot metrics
msam snapshot
```

### 5. Knowledge Graph Operations

```bash
# Detect contradictions
msam contradictions

# Analyze knowledge gaps
msam gaps "user"

# Traverse relationships
msam graph "Alex"

# View statistics
msam stats

# Retrieval analytics
msam analytics

# Metamemory coverage assessment
msam metamemory "trading"
```

### 6. REST API Server

```bash
# Start HTTP API (20 endpoints)
msam serve

# Available endpoints:
POST /store           # Store atoms
POST /query           # Retrieve atoms (confidence-gated)
POST /context         # Compressed startup context
POST /feedback        # Mark contribution to response
POST /decay           # Run decay cycle
POST /consolidate      # Sleep-inspired consolidation
POST /forget          # Intentional forgetting
POST /calibrate       # Cross-provider calibration
GET  /stats           # Database statistics
GET  /analytics       # Retrieval analytics
GET  /triples         # Knowledge graph triples
GET  /contradictions  # Detect conflicts
GET  /graph           # Traverse relationships
GET  /metrics         # Time-series metrics
GET  /export          # Export all atoms
POST /import          # Import atoms
GET  /agents          # Multi-agent operations
# ... + 7 more endpoints
```

---

## Core Concepts

### The Atom (Fundamental Unit)

Every memory is an **atom** with:

```python
{
    "id": "abc123...hash",           # content-derived hash
    "profile": "standard",              # lightweight (~50), standard (~150), full (~300)
    "stream": "semantic",             # semantic | episodic | procedural | working

    "content": "User prefers dark mode",
    "content_hash": "sha256...",

    "created_at": "2026-02-23T22:00:00Z",
    "last_accessed_at": "2026-02-23T22:30:00Z",
    "access_count": 47,

    "stability": 0.85,                # resistance to forgetting
    "retrievability": 0.42,          # probability of recall

    # Emotion-at-encoding (IMMUTABLE)
    "arousal": 0.2,                 # 0.0 calm → 1.0 intense
    "valence": 0.5,                  # -1.0 negative → 1.0 positive
    "encoding_confidence": 0.9,        # certainty at write-time
    "topics": ["preferences", "ui"],

    "state": "active",                # active | fading | dormant | tombstone
    "is_pinned": false,               # protect from decay

    "agent_id": "default"             # multi-agent isolation
}
```

### Hybrid Retrieval (3 Signals)

1. **Keyword Matching** (FTS5 full-text search) — Exact terms, IDs, technical names
2. **Vector Similarity** (1024-dim embeddings) — Semantic similarity, conceptual queries
3. **ACT-R Activation** (access count + recency + stability) — Cognitive plausibility

**Combined score:**
```python
combined = 0.3 × activation + 0.5 × similarity + 0.2 × keyword
```

### Confidence Gating

MSAM returns output proportional to confidence:

| Tier | Similarity | Output | Tokens | Behavior |
|-------|-------------|---------|----------|
| HIGH | ≥ 0.45 | Full results, ≤12 triples | 140-176 | Best effort, full context |
| MEDIUM | ≥ 0.30 | Top 3 atoms, ≤8 triples | 91-131 | Focused, minimal padding |
| LOW | ≥ 0.15 | 1 atom, no triples | 0-33 | Advisory only, "I'm not sure" |
| NONE | < 0.15 | Empty | 0 | Honest unknown: "I don't know" |

**Key innovation:** Agent admits when it doesn't know. No hallucinations.

### Lifecycle (No Permanent Deletion)

```
ACTIVE --(R < 0.3)--> FADING --(R < 0.1)--> DORMANT --(manual)--> TOMBSTONE
  ^                                                                    |
  +----------------------- (accessed: reactivate) ------------------------+
```

**Retrievability formula:**
```
R(t) = e^(-t/S)
```

Where:
- `t` = time since last access
- `S` = stability (resistance to forgetting)

**Design invariant:** TOMBSTONE is deepest state. Content preserved. Nothing is permanently deleted.

---

## Performance

### Benchmarks (100 atoms, 25 queries)

| Metric | MSAM | Raw Vector | Result |
|--------|--------|------------|---------|
| **Token Savings** | 98.8% | — | ✅ Validated |
| **Avg Tokens/Query** | 112 | 9301 | ✅ 98.8% reduction |
| **MRR** | 0.328 | 0.314 | ✅ +4.4% better |
| **Latency** | 2.1ms | 5.4ms | ✅ 2.5x faster |
| **Absent Detection** | 75% | — | ✅ Honest unknowns |

### Session Economics

| Metric | Flat Files | MSAM | Savings |
|--------|-------------|--------|----------|
| Tokens per session | ~12,000 | ~1,351 | 89% |
| Cost (Opus @ $15/MTok) | ~$0.18 | $0.02 | $0.16/session |
| Context window usage | 30% of 40K | 0.3% of 40K | 30% freed |

---

## Integration with OpenClaw

### Option A: REST API

```python
import requests

# Store memory
resp = requests.post("http://localhost:8000/store", json={
    "content": "User prefers dark mode and concise responses",
    "stream": "semantic",
    "arousal": 0.2,
    "valence": 0.5,
    "encoding_confidence": 0.9
})

# Retrieve (confidence-gated)
resp = requests.post("http://localhost:8000/query", json={
    "query": "What are user's preferences?"
})
print(resp.json())
# Returns: atoms, triples, confidence_tier, shannon_ratio
```

### Option B: CLI Integration

```bash
# From shell or script
msam store "User wants dark mode"
result=$(msam query "What are user's preferences?")
echo "$result"
```

### Option C: Library Import

```python
from msam import MSAM

msam = MSAM(config_path="~/.msam/msam.toml")

# Store
msam.store("User prefers dark mode", stream="semantic")

# Retrieve
result = msam.query("What are user's preferences?")
print(result.confidence_tier)  # high | medium | low | none
print(result.atoms)
```

---

## Migration from Flat Files

### Export Current Memories

```python
# Parse MEMORY.md, USER.md, SOUL.md, etc.
# Extract atoms with appropriate streams

# For each memory:
atoms = [
    {
        "content": "User prefers dark mode",
        "stream": "semantic",
        "arousal": 0.2,
        "valence": 0.5,
        "encoding_confidence": 0.9
    },
    # ... more atoms
]

# Write to JSON
import json
with open("memories.json", "w") as f:
    json.dump(atoms, f, indent=2)
```

### Import to MSAM

```bash
# Import atoms
msam import < memories.json

# Validate
msam stats
msam query "User preferences"
```

---

## Architecture Summary

```
Query → Hybrid Retrieve (Keyword + Vector + ACT-R) → Confidence Gate → Output

Memory Streams:
├─ Semantic  → Facts, preferences (slow decay)
├─ Episodic  → Events, conversations (medium decay)
├─ Procedural → How-to, skills (very slow decay)
└─ Working    → Current session (deleted at end)

Lifecycle:
ACTIVE → FADING → DORMANT → TOMBSTONE
(No permanent deletion — full audit trail)
```

---

## Key Benefits

1. **Token Efficiency** — 98.8% savings vs flat files (112 vs 9301 tokens/query)
2. **Confidence Gating** — Honest "I don't know" responses, no hallucinations
3. **Biological Decay** — ACT-R activation scoring, exponential retrievability decay
4. **No Permanent Deletion** — Tombstone state, full audit trail, reversibility
5. **Observability** — 13 metric tables, Grafana-ready, 264 tests
6. **Multi-Agent** — Agent isolation, selective sharing, per-agent statistics
7. **Knowledge Graph** — Subject-predicate-object triples, contradiction detection
8. **REST API** — 20 endpoints, language-agnostic integration
9. **CLI** — 54 commands for full control
10. **Production-Tested** — 675+ atoms, 1,500+ triples, running in production

---

## Resources

- **GitHub:** https://github.com/jadenschwab/msam
- **README:** https://github.com/jadenschwab/msam/blob/main/README.md
- **Spec:** https://github.com/jadenschwab/msam/blob/main/SPEC.md
- **Benchmarks:** https://github.com/jadenschwab/msam/blob/main/BENCHMARKS.md
- **Analysis:** `msam-analysis.md` in workspace
- **Benchmark Results:** `msam-benchmark-results.md` in workspace

---

## FAQ

### Q: Why not just use RAG?

**A:** RAG retrieves by semantic similarity only. MSAM adds:
- ACT-R activation scoring (access patterns + recency)
- Confidence gating (honest unknowns)
- Bi-temporal decay (biological forgetting)
- 4 cognitive streams (different retrieval per stream type)

### Q: Is emotion-at-encoding mutable?

**A:** No. Emotional tags (`arousal`, `valence`) are **immutable** — they record what the agent felt when the memory was formed, not what it feels now. This enables tracking emotional drift over time.

### Q: Can memories be permanently deleted?

**A:** No. The deepest state is **TOMBSTONE**. Content, embeddings, and access history are preserved forever. This ensures auditability and reversibility.

### Q: What if I want to upgrade from SQLite to PostgreSQL?

**A:** MSAM has a migration system. When atom count exceeds 10,000, PostgreSQL + pgvector migration is recommended for concurrent access and native vector operations.

### Q: How much does it save?

**A:**
- Tokens: 98.8% savings (112 vs 9301 tokens/query)
- Cost: $0.16/session saved (@ Opus $15/MTok)
- Time: Faster retrieval (2.1ms vs 5.4ms raw vector)
- Break-even: ~50-100 sessions

---

## License

MIT — See LICENSE at https://github.com/jadenschwab/msam/blob/main/LICENSE
