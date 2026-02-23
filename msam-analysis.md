# MSAM (Multi-Stream Adaptive Memory) Analysis

**Repository:** https://github.com/jadenschwab/msam
**Analyzed:** 2026-02-23
**For:** OpenClaw Agent Memory Integration

---

## 🎯 What is MSAM?

**Multi-Stream Adaptive Memory** — a production-grade cognitive memory architecture for AI agents.

MSAM gives agents persistent, structured memory that **self-regulates** what it stores, how it retrieves, and when it forgets. Knowledge lives as discrete atoms across **4 cognitive streams**:

| Stream | Contains | Retrieval Pattern | Decay Rate |
|---------|----------|------------------|------------|
| **Semantic** | Facts, preferences, decisions | Keyword + vector hybrid | Slow (stable knowledge) |
| **Episodic** | Events, conversations, experiences | Temporal + emotional + associative | Medium (consolidates over time) |
| **Procedural** | How-to knowledge, skills, patterns | Pattern matching | Very slow (skills persist) |
| **Working** | Current session context | Direct access (always in context) | Session-scoped (deleted at end) |

---

## 💡 Core Innovation: 99.3% Token Savings

### The Problem It Solves

**Traditional approach:** Load everything into context every session

```
SOUL.md: 2,000 tokens
USER.md: 1,500 tokens
MEMORY.md: 3,827 tokens
Daily files: Variable
= ~7,327 tokens before first thought!
```

**MSAM approach:** Retrieve only what's relevant

```
msam context
= 51 tokens (delta) / 90 tokens (first-run)
= 99.3% token reduction
```

---

## 📊 Production Benchmarks

**Hardware:** Hetzner CAX11 (2 vCPU ARM64, 4GB RAM, 40GB SSD)

### Startup Performance

| Scenario | MD Baseline | MSAM Output | Token Savings |
|-----------|--------------|--------------|---------------|
| Cold-start (delta) | 7,327 tokens | 51 tokens | **99.3%** |
| Known query | 7,327 tokens | 91 tokens | **98.8%** |
| Unknown query | 7,327 tokens | 33 tokens | **99.5%** |
| No data | 7,327 tokens | 0 tokens | **100%** |

### Query Performance

| Query Type | Output | Confidence | Latency |
|------------|---------|------------|----------|
| Known | 91-176 tokens | Medium/High | ~870ms |
| Unknown | 33 tokens | Low | ~870ms |
| None | 0 tokens | None | ~1,064ms |

### Session Economics (startup + 10 queries)

| Metric | Flat Files (selective) | MSAM | Savings |
|--------|------------------------|-------|----------|
| Tokens per session | ~12,000 tokens | ~1,351 tokens | **89%** |
| Cost (Opus @ $15/MTok) | ~$0.18 | $0.02 | **$0.16** |
| Context window usage | ~30% of 40K | 0.3% of 40K | **~30% freed** |

---

## 🧪 Theoretical Foundation

### 1. ACT-R Activation Theory

MSAM adapts **Anderson's ACT-R (Adaptive Control of Thought -- Rational)** architecture:

```
activation = base_level + spreading_activation + recency_boost
```

- **Base level:** Logarithmic function of access count and time since creation
- **Spreading activation:** Embedding similarity between query and atom
- **Recency boost:** Exponential decay favoring recent access

**Result:** Retrieval that is cognitively plausible — frequently accessed, recently relevant, and semantically connected memories surface first. Not just "closest vector."

### 2. Emotion-at-Encoding

**Immutable emotional annotations** at write-time:

```python
arousal    # 0.0 (calm) → 1.0 (intense)
valence     # -1.0 (negative) → 1.0 (positive)
encoding_confidence  # Certainty at write-time
```

**Why it matters:**

- **Immutable:** Records what the agent felt when memory was formed, not what it feels now
- **Auditable:** Can track emotional drift over time ("User was angry in Jan, but how do they feel in Feb?")
- **Scientific:** Based on neuroscience (Richter-Levin 2003, Damasio 1994, McGaugh 2004, Sharot 2007)

**Distinction from other systems:**
- ❌ Other systems: Sentiment analysis at retrieval (recomputes mood)
- ✅ MSAM: Emotional tags at encoding (immutable evidence)

### 3. The Inverted Stack

**Most systems:** Emotion drives retrieval (mood-congruent recall)

**MSAM:** Facts are primary; emotion is metadata

**Rationale:**
```
Mood-congruent retrieval in humans = bias (depressed people recall sad memories)
AI systems can break this loop structurally → Precision by default, emotional weighting explicit
```

---

## 🏗️ Architecture

### The Atom (Fundamental Unit)

```sql
atoms (
    id TEXT PRIMARY KEY,                  -- content-derived hash
    profile TEXT,                        -- lightweight | standard | full
    stream TEXT,                         -- semantic | episodic | procedural | working

    content TEXT NOT NULL,
    content_hash TEXT NOT NULL,

    created_at TEXT NOT NULL,
    last_accessed_at TEXT,
    access_count INTEGER,

    stability REAL,                       -- spaced repetition resistance
    retrievability REAL,                  -- probability of recall

    arousal REAL,                         # emotional intensity (immutable)
    valence REAL,                         # emotional polarity (immutable)
    topics TEXT,                          # JSON array of topics
    encoding_confidence REAL,             # certainty at write-time

    state TEXT,                          # active | fading | dormant | tombstone
    embedding BLOB,                      # 1024-dim float32 vector
    metadata TEXT,                       # JSON extensible fields

    agent_id TEXT,                        # multi-agent isolation
    embedding_provider TEXT,               # tracking provenance

    is_pinned INTEGER,                    # protect from decay
    session_id TEXT,                      # working memory tracking
    working_expires_at REAL                # TTL for working memory
)
```

### Hybrid Retrieval (3 Signals)

| Signal | Implementation | Use Case |
|---------|---------------|-----------|
| **Keyword** | FTS5 full-text search | Exact terms, IDs, technical names |
| **Vector** | 1024-dim embeddings (NVIDIA NIM, OpenAI, ONNX) | Semantic similarity, conceptual queries |
| **ACT-R** | Access count + recency + stability | Cognitive plausibility, frequent items |

**Combined score:**
```python
combined = (activation_weight * activation) +
           (similarity_weight * similarity) +
           (keyword_weight * keyword_score)
```

### Confidence Gating

| Tier | Similarity | Output | Token Volume |
|-------|-------------|---------|---------------|
| **High** | >= 0.45 | Full results, zero-sim pruned, <=12 triples | 140-176 tokens |
| **Medium** | >= 0.30 | Top 3 atoms (sim > 0.15), <=8 triples | 91-131 tokens |
| **Low** | >= 0.15 | 1 atom for context, no triples, advisory | 0-33 tokens |
| **None** | < 0.15 | Empty, advisory only | 0 tokens |

**Key innovation:** Agent admits when it doesn't know (honest unknown pattern). No hallucinations.

---

## 💾 Lifecycle: The Decay System

### State Transitions

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

### State Behaviors

| State | Visibility | Decay | Retrieval |
|-------|------------|--------|-----------|
| **ACTIVE** | Full | Normal | Included in default retrieval |
| **FADING** | Full | Profile compacted (full → standard → lightweight) | Included in default retrieval |
| **DORMANT** | Full | Minimal | Excluded from default, searchable manually |
| **TOMBSTONE** | Full | None | Final state. Content preserved, not retrieved |

**Design invariant: NO PERMANENT DELETION**

All atoms retain full content, annotations, embeddings, and access history regardless of lifecycle state.

**Rationale:**
1. **Reversibility:** Any decay decision can be reversed
2. **Audit trail:** Full history of what agent knew
3. **Research data:** Forgetting curve is empirical data
4. **Trust:** Agent promises "everything is still there"

---

## 🔌 REST API (20 Endpoints)

```bash
# Start server
msam serve

# Available endpoints:
- POST /store                    # Store atoms
- POST /batch                    # Batch store
- POST /query                    # Retrieve atoms
- POST /context                  # Compressed startup context
- POST /feedback                 # Mark contribution
- POST /decay                    # Run decay cycle
- POST /consolidate              # Sleep-inspired consolidation
- POST /forget                   # Intentional forgetting
- POST /calibrate                # Cross-provider calibration
- POST /re-embed                 # Re-embed all atoms
- POST /predict                  # Predictive prefetch
- GET  /stats                    # Database statistics
- GET  /analytics                # Retrieval analytics
- GET  /triples                  # Knowledge graph triples
- GET  /contradictions           # Detect conflicts
- GET  /graph                    # Traverse relationships
- GET  /metrics                  # Time-series metrics
- GET  /export                   # Export all atoms
- POST /import                   # Import atoms
- GET  /agents                   # Multi-agent operations
```

---

## 📝 CLI (54 Commands)

```bash
# Storage
msam store "Your memory content"
msam batch "atom1" "atom2" "atom3"
msam negative "X is NOT Y"

# Retrieval (confidence-gated)
msam query "search query"
msam hybrid "search query"         # atoms + triples
msam explain "query"               # detailed scoring breakdown
msam diverse "query"               # diversity-optimized

# Session startup
msam context                       # 51-90 tokens vs thousands

# Feedback
msam feedback-mark <atom_ids> <response_text>
msam contribute <atom_id>

# Lifecycle
msam decay                         # run decay cycle
msam forgetting --dry-run          # preview forgetting
msam consolidate                   # sleep-inspired consolidation
msam snapshot                      # log metrics

# Knowledge graph
msam contradictions                # detect conflicts
msam gaps <entity>                 # knowledge gap analysis
msam graph <entity>                # traverse relationships

# Analysis
msam metamemory "topic"            # coverage assessment
msam stats                         # database statistics
msam analytics                     # retrieval analytics
msam predict                       # predictive prefetch

# Admin
msam serve                         # start REST API
msam calibrate                     # cross-provider calibration
msam re-embed                      # re-embed all atoms
msam export > backup.json
msam import < backup.json>
msam pin <atom_id>                 # protect from decay
```

---

## 📊 Observability

### Metrics Infrastructure (13 Tables)

| Table | Tracks | Frequency |
|-------|--------|-----------|
| **system_metrics** | Atom count, tokens, budget, DB size | Every 30s |
| **access_events** | Every MSAM operation with full detail | Per access |
| **retrieval_metrics** | Activation distributions, latency | Per retrieval |
| **store_metrics** | New atoms, stream distribution | Per store |
| **decay_metrics** | Tokens freed, atoms transitioned | Hourly |
| **emotional_metrics** | Arousal, valence, intensity | Every 30s |
| **topic_timeseries** | Topic frequency | Per access |
| **continuity_metrics** | Cross-session overlap | Per session |
| **cache_metrics** | Embedding cache hit rate | On demand |

### Canary Monitoring

Fixed identity query runs every 5 minutes:
- Retrival latency stability
- Top activation score drift
- Atom count consistency
- Startup context composition

### Grafana Dashboard

25 panels covering:
- System health
- Retrieval performance
- Activation distributions
- Token economics
- Emotional state
- Memory age
- Embedding latency
- Retrieval quality
- Continuity
- Decay lifecycle

---

## 🔬 Comparison: MSAM vs. Traditional Approaches

| Aspect | Naive RAG | Framework Memory | Letta/MemGPT | **MSAM** |
|---------|-------------|------------------|----------------|-----------|
| **Architecture** | Vector DB only | Bolt-on store | 3-tier with paging | **4-stream atomic** |
| **Scoring** | Similarity only | Tag-based | Access frequency | **ACT-R activation** |
| **Emotion** | Sentiment at retrieval | None | None | **Immutable at encoding** |
| **Decay** | TTL only | None | Auto-summarization | **Biological decay** |
| **Observability** | Basic | None | Dashboard | **13 metric tables** |
| **Confidence** | None | None | None | **4-tier gating** |
| **Compression** | None | None | Auto-summary | **99.3% startup** |
| **API** | None | Varied | Limited | **20 REST endpoints** |

---

## 💡 How MSAM Improves OpenClaw Memory

### Current OpenClaw Approach

```
MEMORY.md           # Long-term curated memories
memory/YYYY-MM-DD.md # Daily logs
USER.md              # User preferences
SOUL.md              # Agent identity
= ~7,327 tokens loaded every session
= No retrieval quality metrics
= No decay system
= Flat file management
```

### MSAM-Enhanced Approach

```
Atoms (675+):
  - Semantic: "User prefers dark mode" (stability: high)
  - Episodic: "Deployed to Vercel on Feb 21" (arousal: 0.8)
  - Procedural: "Deploy to Netlify: git commit && push" (stability: very high)
  - Working: "Current task: deploy wrappers site"

Startup context:
  - 51 tokens (delta) vs 7,327 baseline
  - 99.3% token savings
  - $0.16 savings per session

Retrieval:
  - Confidence-gated (high/medium/low/none)
  - Hybrid search (keyword + vector + ACT-R)
  - No hallucinations when low confidence
```

### Integration Options

#### Option A: Direct Replacement

```bash
# Install MSAM
pip install msam

# Migrate existing memories
msam import < memory-backup.json >

# Use in OpenClaw
python3 << 'EOF'
import requests

# Store memory
resp = requests.post("http://localhost:3001/store", json={
    "content": "User prefers dark mode and concise responses",
    "stream": "semantic",
    "arousal": 0.2,
    "valence": 0.5,
    "encoding_confidence": 0.9
})

# Retrieve (confidence-gated)
resp = requests.post("http://localhost:3001/query", json={
    "query": "What are user's preferences?"
})
print(resp.json())
# Returns: atoms, triples, confidence_tier, shannon metrics
EOF
```

#### Option B: MCP Server Integration

```python
# Use MSAM as MCP server
from mcp import ClientSession

# In OpenClaw agent config
mcp_servers:
  - msam:
      command: ["msam", "serve"]
      env:
        MSAM_DATA_DIR: "/path/to/msam/data"
```

#### Option C: Library Integration

```python
# Import MSAM directly in Python
from msam import MSAM

msam = MSAM(config_path="~/.msam/msam.toml")

# Store memory
msam.store("User prefers dark mode", stream="semantic")

# Retrieve (confidence-gated)
result = msam.query("What are user's preferences?")
print(result.confidence_tier)  # high | medium | low | none
print(result.atoms)           # Retrieved atoms
print(result.shannon_ratio)    # % of Shannon minimum
```

---

## 🚫 Limitations & Considerations

### 1. Python Version Requirement

```
Requires: Python 3.11+ (uses tomllib from stdlib)
Current system: Python 3.10.12
```

**Fix:**
```bash
# Option A: Upgrade system Python
sudo apt update && sudo apt install python3.11

# Option B: Use pyenv
pyenv install 3.11
pyenv local 3.11

# Option C: Use Docker
docker run -p 8000:8000 msam-server:latest
```

### 2. Embedding Provider

**Default:** NVIDIA NIM (free tier available)

**Alternatives:**
```toml
# Option A: NVIDIA NIM (free, recommended)
[embedding]
provider = "nvidia-nim"
model = "nvidia/nv-embedqa-e5-v5"

# Option B: OpenAI
[embedding]
provider = "openai"
model = "text-embedding-3-small"

# Option C: ONNX (local, no API key)
[embedding]
provider = "onnx"
model = "BAAI/bge-small-en-v1.5"  # 33MB download

# Option D: Local (sentence-transformers)
[embedding]
provider = "local"
model = "all-MiniLM-L6-v2"
```

### 3. Data Scale

**Current:** SQLite (scales to ~10,000 atoms)

**Beyond 10K atoms:** PostgreSQL + pgvector migration needed

**Reason:** SQLite is single-threaded; PostgreSQL provides concurrent access and native vector operations

---

## 📚 Resources

### Documentation
- **GitHub:** https://github.com/jadenschwab/msam
- **README:** https://github.com/jadenschwab/msam/blob/main/README.md
- **Spec:** https://github.com/jadenschwab/msam/blob/main/SPEC.md
- **Benchmarks:** https://github.com/jadenschwab/msam/blob/main/BENCHMARKS.md
- **Control Flow:** https://github.com/jadenschwab/msam/blob/main/CONTROL-FLOW.md

### Project Structure

```
msam/
  core.py              # Atom storage, ACT-R retrieval (4,011 lines)
  remember.py          # CLI integration (54 commands, 1,974 lines)
  triples.py           # Knowledge graph (1,084 lines)
  retrieval_v2.py      # v2 pipeline (989 lines)
  server.py            # REST API (633 lines)
  metrics.py           # Observability (611 lines)
  decay.py             # Lifecycle (501 lines)
  embeddings.py        # Pluggable providers (343 lines)
  ...                 # 17 more modules
  examples/            # Demos (488 lines)
  benchmarks/          # Test suite (1,651 lines)
  tests/               # 264 tests (3,777 lines)
```

**Total:** ~21,547 lines of code + tests

---

## ✅ Summary

### What MSAM Offers

1. **99.3% token savings** on startup (7,327 → 51 tokens)
2. **89% session savings** vs flat files (~1,351 tokens vs 12,000)
3. **4-stream architecture** (semantic, episodic, procedural, working)
4. **ACT-R activation scoring** (cognitively plausible retrieval)
5. **Confidence gating** (honest unknown pattern, no hallucinations)
6. **Bi-temporal decay** (biological forgetting model)
7. **No permanent deletion** (tombstone state, full audit trail)
8. **20 REST endpoints** (language-agnostic API)
9. **54 CLI commands** (full control)
10. **264 tests** (production-grade quality)

### Why It's Relevant to OpenClaw

| Feature | OpenClaw Current | MSAM Solution |
|----------|------------------|----------------|
| Token efficiency | 7,327+ tokens per session | **51 tokens (99.3% reduction)** |
| Retrieval quality | File grep | **Hybrid search + ACT-R scoring** |
| Confidence awareness | None | **4-tier gating** |
| Decay system | None | **Biological lifecycle** |
| Observability | None | **13 metric tables + Grafana** |
| Emotional context | None | **Immutable emotion-at-encoding** |
| Multi-agent | Basic | **Full isolation + sharing** |

### Integration Effort

**Estimated time:** 8-16 hours

**Path:**
1. Install Python 3.11+ (or use Docker)
2. Set up embedding provider (NVIDIA NIM free tier)
3. Import existing memory files to MSAM
4. Integrate via REST API or MCP server
5. Validate retrieval quality against expectations

### ROI

| Metric | Value |
|---------|--------|
| Token savings per session | 89% (~$0.16/session @ Opus rates) |
| Development effort | 8-16 hours |
| Break-even | ~50-100 sessions |
| Long-term savings | 89% on every session |

---

## 🎯 Next Steps

### If Integrating MSAM into OpenClaw

1. **Proof of Concept (2-4 hours)**
   - Install MSAM in Docker container
   - Test store/retrieve cycle
   - Compare against current memory approach

2. **Migration (2-4 hours)**
   - Export existing MEMORY.md, USER.md to JSON
   - Import into MSAM with appropriate streams
   - Validate atom count and retrieval quality

3. **Integration (4-8 hours)**
   - Choose integration method (REST API / MCP / Library)
   - Update OpenClaw memory calls
   - Add observability dashboards
   - Test across scenarios

4. **Validation (2 hours)**
   - Run retrieval tests
   - Measure token savings
   - Verify confidence gating behavior
   - Compare quality before/after

### If Not Integrating

- Keep MSAM as reference for memory architecture decisions
- Consider for future agent memory systems
- Learn from ACT-R activation theory
- Study emotion-at-encoding pattern

---

**This is the most sophisticated AI memory system I've analyzed.**

- Not just storage — a full cognitive lifecycle
- Production-tested (675+ atoms, 1,500+ triples)
- Theoretically grounded (ACT-R, neuroscience)
- Fully instrumented (13 metrics tables)
- 99.3% token savings — measured, not claimed

---

*Analysis completed: 2026-02-23*
