# Graphiti Analysis — Real-Time Knowledge Graphs for AI Agents

**Fetched from:** https://github.com/getzep/graphiti
**Date:** 2026-02-23
**Analysis for:** OpenClaw Agent Memory & Context

---

## 🎯 What is Graphiti?

**Graphiti** is an open-source framework for building **real-time, temporally-aware knowledge graphs** specifically designed for AI agents operating in dynamic environments.

### Core Value Proposition

| Traditional RAG | Graphiti |
|----------------|-----------|
| Static documents | **Continuous, incremental updates** |
| Batch processing | **Real-time data integration** |
| No time awareness | **Bi-temporal tracking** (when + what) |
| Simple retrieval | **Hybrid semantic + keyword + graph search** |

---

## 🧪 Key Architecture

### 1. Knowledge Graph Structure

**Nodes (Entities):**
- Entities (things: "Kendra", "Adidas shoes")
- Episodes (events/interactions with timestamps)
- Communities (clusters of related information)
- Sagas (multi-step operations)

**Edges (Relationships):**
- `loves` — Kendra → loves → Adidas shoes
- `mentioned_in` — Entity mentioned in Episode
- `occurred_in` — Event occurred in Episode
- `next_episode` — Sequential episode linking

### 2. Bi-Temporal Data Model

**Explicit time tracking:**
```json
{
  "occurred_at": "2026-02-23T22:00:00Z",
  "valid_until": "2026-02-23T23:00:00Z",
  "expiration_policy": "TTL_30_DAYS"
}
```

**Why it matters:**
- **Point-in-time queries:** "What did Kendra know on Feb 20?"
- **Historical context:** Full trajectory without full recomputation
- **Efficient updates:** Only new/changed data needs processing

---

## 🤖 Supported Databases

| Backend | Type | Use Case | Pros |
|----------|-------|---------|------|
| **Neo4j** | Graph DB | Most mature, Cypher queries, ACID transactions |
| **FalkorDB** | Client-Server | Lightweight, no Docker needed, embeddable |
| **Kuzu** | Embedded | In-process, ultra-fast queries, open-source |
| **Amazon Neptune** | Cloud | Managed, OpenSearch integration, enterprise scale |

**Pluggable Architecture:**
```
graphiti_core/driver/
├── neo4j_driver.py      # Neo4j implementation
├── falkordb_driver.py     # FalkorDB implementation
├── kuzu_driver.py         # Kuzu implementation
└── neptune_driver.py       # Neptune implementation
```

All expose same 11 operation interfaces:
- EntityNodeOperations, EpisodeNodeOperations, CommunityNodeOperations
- EntityEdgeOperations, EpisodicEdgeOperations, CommunityEdgeOperations
- SearchOperations, GraphMaintenanceOperations

---

## 🔍 Hybrid Search Strategy

Graphiti combines **3 retrieval methods** for optimal performance:

### 1. Semantic Search (Embeddings)
- **Use:** LLM embeddings (OpenAI, Gemini, Voyage)
- **Method:** Vector similarity search
- **Best for:** Conceptual queries, "things like X"

### 2. Keyword Search (BM25)
- **Use:** BM25 algorithm
- **Method:** Term frequency + document length normalization
- **Best for:** Exact entity names, IDs, technical terms

### 3. Graph Traversal
- **Use:** Neo4j Cypher, graph algorithms
- **Method:** Follow edges, compute distances, label propagation
- **Best for:** Relationship queries, "who knows X", "X connected to Y"

### Ranking: Graph Distance
- Combines all 3 methods
- Reranks results using graph distance metrics
- Ensures: **Relevant, not just similar**

**Performance:**
- **Latency:** Typically sub-second (not seconds like LLM summarization)
- **Accuracy:** Hybrid approach reduces false positives

---

## 🔌 vs. GraphRAG

| Aspect | GraphRAG | Graphiti |
|---------|-----------|-----------|
| **Primary Use** | Static document summarization | **Dynamic data management** |
| **Data Handling** | Batch-oriented processing | **Continuous, incremental updates** |
| **Knowledge Structure** | Entity clusters & community summaries | **Episodic data, semantic entities, communities** |
| **Retrieval Method** | Sequential LLM summarization | **Hybrid semantic + keyword + graph-based search** |
| **Adaptability** | Low | **High** |
| **Temporal Handling** | Basic timestamp tracking | **Explicit bi-temporal tracking** |
| **Contradiction Handling** | LLM-driven summarization judgments | **Temporal edge invalidation** |
| **Query Latency** | Seconds to tens of seconds | **Typically sub-second latency** |
| **Custom Entity Types** | No | **Yes, customizable** |
| **Scalability** | Moderate | **High, optimized for large datasets** |
| **Graphiti Focus** | Static, efficient summarization | **Dynamic & frequently updated datasets** |

**Bottom Line:**
- **GraphRAG** = Better for static document archives
- **Graphiti** = Better for dynamic, real-time, interactive AI applications

---

## 🤖 MCP (Model Context Protocol) Server

Graphiti includes a full MCP server implementation for AI assistants.

### Capabilities:

```python
# Episode management
- add_episode()
- retrieve_episode()
- delete_episode()

# Entity & relationship handling
- add_entity()
- get_entities()
- search_entities()

# Group management
- create_group()
- get_groups()

# Graph maintenance
- build_indices()
- delete_all_indexes()
```

### Integration:

```python
from mcp import ClientSession, StdioServerParameters
from graphiti.mcp_server import create_graphiti_server

# Create MCP server
server = create_graphiti_server(
    graph_db="bolt://localhost:7687"
)

# Run as MCP server
async with ClientSession(server, StdioServerParameters()) as session:
    # Graphiti is now available to Claude, Cursor, etc.
    pass
```

**Benefits for OpenClaw:**
- **Standardized protocol:** No custom OpenClaw-specific integration needed
- **State management:** Graphiti handles graph state, agent focuses on tasks
- **Efficient retrieval:** Sub-second queries from knowledge graph
- **Context assembly:** Combine structured graph data with unstructured LLM context

---

## 📊 Why Graphiti is Relevant to OpenClaw

### 1. Agent Memory Patterns

**Pattern: "What did I just do?"**

Graphiti's **bi-temporal episodes** are perfect for tracking agent state:

```
Episode 1: User asked for Python install
  Occurred: 2026-02-23T22:00:00Z
  Valid Until: 2026-02-23T22:00:00Z

Episode 2: Installed dependencies
  Occurred: 2026-02-23T22:05:00Z
  Valid Until: TTL_30_DAYS

Episode 3: Ran tests successfully
  Occurred: 2026-02-23T22:10:00Z
```

**Query capability:**
```python
# Point-in-time: What was the state at X?
graph = Graphiti(...)
state_at_22:00 = graph.search_episodes(
    query="state at 2026-02-23T22:00:00"
)

# Current trajectory
trajectory = graph.get_full_trajectory()
```

### 2. Multi-Agent Coordination

**Scenario:** Agent A shares info → Agent B uses it

Graphiti supports this via:
- **Episode linking** — Agent B references Agent A's episode
- **Next_episode edges** — Causal connections between events
- **Community clustering** — Grouping related information from multiple agents

### 3. Self-Healing & Recovery

**Similar to Recovery-Bench:**

| Failure Mode | Recovery Approach |
|-------------|-----------------|
| Wrong command executed | Re-execute with correction |
| State corruption | Roll back to last valid episode |
| Tool failure | Try alternative tool from graph |

Graphiti's **bi-temporal model** enables:
- **Time-travel debugging:** "Show me state 5 minutes ago"
- **State comparison:** "What changed between episode 42 and 43?"
- **Rollback:** "Revert to episode 40 state"

---

## 📝 Installation & Setup

### Quick Start (Recommended: Neo4j + FalkorDB)

```bash
# 1. Clone repo
git clone https://github.com/getzep/graphiti.git
cd graphiti

# 2. Install with FalkorDB (lightweight, no Docker)
pip install "graphiti-core[falkordb]"

# 3. Start FalkorDB
docker run -p 6379:6379 -d falkordb/falkordb:latest

# 4. Initialize graphiti
python3 << 'EOF'
from graphiti import Graphiti

graph = Graphiti(
    "bolt://localhost:7687",  # Neo4j
    "neo4j",              # User
    "password"
)
EOF
```

### Alternative: Kuzu (Embedded, Ultra-Fast)

```bash
pip install "graphiti-core[kuzu]"
python3 << 'EOF'
from graphiti import Graphiti

graph = Graphiti(
    "bolt://localhost:7687",  # Neo4j driver
    database="/tmp/graphiti.kuzu"  # Kuzu embedded DB
)
EOF
```

---

## 🚫 Known Limitations

### 1. Python Version Requirement

```
ERROR: Package 'recovery-bench' requires a different Python: 3.10.12 not in '>=3.12'
```

**Requirement:** Python 3.12+ (Graphiti uses newer Python features)

**On this system:** Python 3.10.12

### 2. LLM Provider 429 Rate Limits

**Issue:** Default SEMAPHORE_LIMIT=10 is too low for high-throughput usage

**Fix:**
```bash
export SEMAPHORE_LIMIT=50
python -m recovery_bench.generate_traces
```

### 3. Graph Database Complexity

**Challenge:** Neo4j requires separate Docker container + configuration

**Easier alternatives:**
- **FalkorDB** — Client-server, no Docker needed
- **Kuzu** — Embedded, ultra-fast, no network overhead

---

## 💡 Recommendations for OpenClaw

### 1. Integrate Graphiti MCP Server

**Why:**
- Standardized protocol (no custom code)
- Bi-temporal episodes for agent state tracking
- Sub-second queries for context retrieval

**Integration path:**
```python
# In OpenClaw skill or MCP config
mcp_servers:
  - graphiti:
      command: ["python3", "/path/to/graphiti/mcp_server/main.py"]
      env:
        NEO4J_URI: "bolt://localhost:7687"
```

### 2. Use Episodes for Conversation Memory

**Pattern:**
```python
# Each user interaction
episode_id = graphiti.add_episode(
    content="User: Deploy to Vercel",
    occurred_at=datetime.now(),
    valid_until=datetime.now() + timedelta(days=30)
)

# Retrieval (point-in-time)
context = graphiti.search_episodes(
    query="deploy context before 2026-02-24"
    time_range=("2026-02-23T00:00:00Z", "2026-02-24T00:00:00Z")
)

# Result: Full trajectory of what happened
# "User deployed to Vercel at 22:00 → Site live at 22:15"
```

### 3. Entity-Relationship Tracking

**Use case:** "Kendra loves Adidas shoes"

**Graph model:**
```python
# Add entities
kendra_id = graphiti.add_entity(name="Kendra")
adidas_id = graphiti.add_entity(name="Adidas shoes")

# Add relationship (episode-based)
graphiti.add_edge(
    source=kendra_id,
    target=adidas_id,
    relationship="loves",
    occurred_at=datetime.now()
)
```

**Why it's powerful:**
- **Temporal:** "Kendra loved Adidas in Q1 2025, but what about Q2?"
- **Contextual:** Combine with episode data for full picture
- **Queryable:** "What brands does Kendra love?"

### 4. Hybrid Retrieval for RAG

**Instead of:** Just semantic search on documents

**Graphiti approach:**
```python
# Combine semantic + keyword + graph
results = graphiti.search(
    query="best trading strategies for crypto",
    search_mode="hybrid"  # semantic + BM25 + graph
)

# Results ranked by:
# 1. Semantic similarity (embeddings)
# 2. Keyword match (BM25)
# 3. Graph distance (connection strength)
# 4. Temporal recency (when was this entity mentioned?)
```

---

## 🔗 Resources

### Documentation
- **GitHub:** https://github.com/getzep/graphiti
- **Quick Start:** https://github.com/getzep/graphiti/blob/main/examples/quickstart/README.md
- **MCP Server:** https://github.com/getzep/graphiti/blob/main/mcp_server/README.md
- **Zep Blog:** https://blog.getzep.com/state-of-the-art-agent-memory
- **Paper:** https://arxiv.org/abs/2501.13956

### Related Projects
- **Zep Platform:** https://www.getzep.com
- **Harbor Framework:** https://github.com/laude-institute/harbor
- **Terminal-Bench:** https://harborframework.com/docs/running-tbench

---

## ✅ Summary

### What Graphiti Offers

1. **Real-Time Knowledge Graphs** — Not static, always updating
2. **Bi-Temporal Tracking** — Explicit time + validity windows
3. **Hybrid Search** — Semantic + keyword + graph traversal
4. **MCP Protocol** — Standard agent integration
5. **Multi-Database Support** — Neo4j, FalkorDB, Kuzu, Neptune

### Why It's Relevant to OpenClaw

| Feature | OpenClaw Need | Graphiti Solution |
|----------|-----------------|------------------|
| Agent state tracking | ❌ None | ✅ Bi-temporal episodes |
| Point-in-time queries | ❌ No | ✅ Time-range search |
| Context retrieval | ❌ File-based only | ✅ Hybrid retrieval (<1s latency) |
| Multi-agent coordination | ❌ Basic | ✅ Episode linking |
| Self-healing | ❌ Basic recovery | ✅ Bi-temporal rollback |

### Integration Effort

**Estimated time:** 4-8 hours to integrate Graphiti MCP server

**Benefits:**
- ✅ Persistent, queryable agent memory
- ✅ Sub-second context retrieval
- ✅ Bi-temporal state tracking
- ✅ Entity-relationship knowledge
- ✅ Standard MCP protocol

---

**Next step:** Create proof-of-concept OpenClaw skill using Graphiti MCP server!

---

*Analysis completed: 2026-02-23*
