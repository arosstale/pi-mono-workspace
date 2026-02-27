# RAG Knowledge Base Setup

## Directory Structure

```
kb/
├── 01-artale-decks/           # Your pitch materials
├── 02-case-studies/           # Win stories
├── 03-verticals/              # Industry playbooks  
├── 04-competition/            # Competitive intel
├── 05-italy-market/           # Local context
└── .index/                    # Vector embeddings
```

## Required Files (Upload These)

### 01-artale-decks/
- [ ] `byd-australia-deck.pdf` — Australia case study presentation
- [ ] `automotive-automation-playbook.pdf` — Vertical playbook
- [ ] `industrial-iot-proposal.pdf` — IoT integration proposal
- [ ] `fleet-management-pitch.pdf` — Fleet management pitch

### 02-case-studies/
- [ ] `byd-australia-case-study.md` — Detailed writeup of Australia win
- [ ] `fleet-automation-results.md` — Metrics, ROI, testimonials
- [ ] `industrial-optimization-win.md` — Factory automation case

### 03-verticals/
- [ ] `automotive-fleet-automation.md`
- [ ] `industrial-iot-operations.md`
- [ ] `security-systems-integration.md`
- [ ] `firefighter-ems-dispatch.md`

### 04-competition/
- [ ] `manus-agent-analysis.md` — Their strengths/weaknesses
- [ ] `triplesense-byd-project.md` — What they built (Leo avatar)
- [ ] `openclaw-differentiation.md` — Why we win

### 05-italy-market/
- [ ] `byd-leo-avatar-analysis.md` — Their Italy launch
- [ ] `italian-automotive-regulations.md` — Compliance requirements
- [ ] `concessionaire-pain-points.md` — What dealers struggle with

## Upload Commands

```bash
# From your local machine
scp byd-australia-deck.pdf majinbu@your-vps:/home/majinbu/pi-mono-workspace/artale-agents/kb/01-artale-decks/

# Or paste content directly
nano /home/majinbu/pi-mono-workspace/artale-agents/kb/02-case-studies/byd-australia-case-study.md
```

## Indexing Script (Auto-runs on upload)

```bash
#!/bin/bash
# kb/index.sh

echo "Indexing RAG knowledge base..."

# Create embeddings
python3 << 'PYTHON'
import os
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path=".index")
collection = client.get_or_create_collection("artale-kb")

# Index all markdown and PDF files
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith(('.md', '.txt', '.pdf')):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            # Chunk and embed
            chunks = [content[i:i+500] for i in range(0, len(content), 500)]
            embeddings = model.encode(chunks)
            
            # Store
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                collection.add(
                    documents=[chunk],
                    embeddings=[embedding.tolist()],
                    ids=[f"{file}-{i}"],
                    metadatas={"source": path}
                )

print(f"Indexed {collection.count()} chunks")
PYTHON

echo "✅ KB indexed and ready"
```

## Query Interface

```python
# strategist/query_kb.py

def query_kb(query: str, n_results: int = 3) -> list:
    """Query knowledge base for relevant context."""
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    client = chromadb.PersistentClient(path="kb/.index")
    collection = client.get_collection("artale-kb")
    
    query_embedding = model.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    return results['documents'][0]

# Example usage
context = query_kb("BYD fleet management ROI", n_results=3)
# Returns: ["Australia case study...", "Fleet metrics...", "Testimonial..."]
```

## Status Check

```bash
cd /home/majinbu/pi-mono-workspace/artale-agents/kb
ls -la */*
```

**Current:** Empty (waiting for your files)

Platform Engineer Kelsey Hightowel