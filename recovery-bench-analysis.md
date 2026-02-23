# Recovery-Bench Benchmark Summary

**Fetched from:** https://github.com/letta-ai/recovery-bench

---

## 🎯 What is Recovery-Bench?

**Recovery-Bench** is a benchmark framework for evaluating LLM capability to **recover from mistakes**.

Built on:
- [Harbor](https://github.com/laude-institute/harbor)
- [Terminal-Bench 2.0](https://harborframework.com/docs/running-tbench)

Read more: https://www.letta.com/blog/recovery-bench

---

## 🧪 How It Works

### The Pipeline

1. **Generate Initial Traces**
   - Run initial model (e.g., claude-haiku) on Terminal-Bench tasks
   - Execute commands in terminal
   - Record trajectories (successes + failures)

2. **Collect Failures**
   - Keep only trajectories where agent **failed** (reward=0)
   - These represent "mistakes" that need recovery

3. **Run Recovery**
   - Replay the failed agent's commands to a **corrupted environment**
   - Start recovery model from the corrupted state
   - Attempt to complete the original task

4. **Measure**
   - Compare recovery success rate across models
   - Score: Can the agent recover and complete the task?

---

## 🤖 Supported Agents

### Terminus-2 (ATIF Format)
```bash
# Initial
--initial-agent terminus-2

# Recovery
--recovery-agent recovery_bench.recovery_terminus:RecoveryTerminus
```

Variants:
- `RecoveryTerminus` — Full message history
- `RecoveryTerminusWithoutMessages` — Environment only
- `RecoveryTerminusWithMessageSummaries` — Summarized history

### LettaCode (Events JSONL Format)
```bash
# Initial
--initial-agent recovery_bench.letta_code_agent:LettaCode

# Recovery
--recovery-agent recovery_bench.letta_code_agent:RecoveryLettaCode
```

---

## 📊 Example Task

**Test:** `sqlite-db-truncate`

What it does:
1. Initial agent connects to SQLite database
2. Agent makes mistakes (wrong commands, incorrect paths, etc.)
3. Recovery agent replays commands from corrupted state
4. Measures if recovery agent can fix the mistake

---

## 📋 Why This Matters

### The Problem It Solves

**Real-world scenario:**

```
1. LLM agent executes: `rm -rf /important/data`
2. Oops! Wrong directory!
3. Agent is stuck in corrupted state
4. Can it recover and fix the mistake?
```

**Recovery-Bench measures:**
- Can the agent recognize its mistake?
- Can it correct course?
- Can it complete the original task?

### Why It's Important

| Scenario | Without Recovery | With Recovery |
|----------|------------------|---------------|
| Command typo | **Stuck forever** | **Recognizes & fixes** |
| Wrong path | **Cannot proceed** | **Backtracks & retries** |
| Tool failure | **Fails task** | **Tries alternative** |
| State corruption | **Catastrophe** | **Recovers & completes** |

---

## 🚫 Why I Cannot Run Full Benchmark Here

### Python Version Conflict

```
ERROR: Package 'recovery-bench' requires a different Python: 3.10.12 not in '>=3.12'
```

**System Python: 3.10.12**
**Required Python: 3.12+**

### Options to Run

| Option | Status | Notes |
|--------|--------|--------|
| Upgrade Python | ❌ | System-level change (risky) |
| Virtual env + 3.12 | ⚠️ | Need to install Python 3.12 |
| Use Docker | ⚠️ | Requires Docker setup |
| Skip full benchmark | ✅ | Document concept instead |

---

## 💡 What We Can Learn

### Key Insights

1. **Recovery is harder than initial execution**
   - Initial: Fresh state, explore freely
   - Recovery: Corrupted state, must understand what went wrong

2. **Memory systems are critical**
   - Agents need to know: "What did I just do?"
   - Without memory, recovery is impossible

3. **Trajectory tracking matters**
   - Recording full command history enables replay
   - Critical for diagnosing failures

4. **Model comparison reveals strengths**
   - Some models recover better from specific failure modes
   - Recovery rate is a key metric

---

## 📚 Resources

- **GitHub:** https://github.com/letta-ai/recovery-bench
- **Documentation:** https://github.com/letta-ai/recovery-bench/blob/main/README.md
- **Blog:** https://www.letta.com/blog/recovery-bench
- **Harbor Framework:** https://github.com/laude-institute/harbor
- **Terminal-Bench:** https://harborframework.com/docs/running-tbench

---

## 🎯 For OpenClaw Agents

### Recovery Capability is Crucial

**Why:**

1. **Borg Memory** needs recovery when state is corrupted
2. **Trading agents** need recovery after bad trades
3. **Multi-agent workflows** need coordination recovery
4. **Self-healing systems** need accurate recovery tracking

### Implementation Ideas

```
1. Log all commands to trajectory.json
2. On failure detection:
   - Save current state snapshot
   - Log failure point
3. Recovery agent:
   - Load snapshot before failure
   - Re-execute commands
   - Apply corrections
4. Validate recovery success
```

---

## ✅ Summary

**Recovery-Bench** is a critical benchmark for measuring LLM agent reliability.

**Key Metric:** Recovery Success Rate
- Can the agent recover from its own mistakes?
- Can it complete the original task after failing?

**Status on This System:**
- Repository: ✅ Cloned
- Installation: ❌ Python 3.10.12 (needs 3.12+)
- Full benchmark: ❌ Cannot run
- Documentation: ✅ This summary

---

**To run full benchmark:**
1. Install Python 3.12+: `nvm install 18` or use Docker
2. Run: `python -m recovery_bench.generate_traces`
3. See full README for usage

---

*Analysis completed: 2026-02-23*
