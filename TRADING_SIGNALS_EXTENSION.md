# Trading Signals Extension - Live

## Extension: `trading-signals.ts`

**Location:** `~/.pi/agent/extensions/trading-signals.ts` (389 lines)
**Status:** ✅ Live and ready

---

## Widget

Auto-hides when no active signals:

```
📡 SIGNALS
XAU ▲ long ema-cross conf 82% R:R 2.4
XAG ─ neutral
◆ 2 pending outcomes
```

During scan:
```
📡 SIGNALS
◆ scanning XAU/XAG…
```

---

## Tools

| Tool | What it does | Example |
|------|--------------|---------|
| **signals_scan** | Runs scanner, updates widget, silent message if found | `signals_scan XAU/XAG → Found 2` |
| **signals_pending** | Open positions waiting for outcome | `signals_pending → 3 pending` |
| **signals_stats** | Win rate, avg P&L, totals | `signals_stats → Win Rate: 68.0%` |
| **signals_recent** | Last N hours (default 24h) | `signals_recent 4h` |
| **signal_resolve** | Record exit + P&L, refreshes widget | `signal_resolve a1b2c3d4 +$142.00` |

---

## /signals Command

Quick dashboard without a full prompt:

```
/signals scan      - Run scanner
/signals pending   - Show pending outcomes
/signals stats     - View statistics
/signals recent 4h - Last 4 hours
```

---

## Silent Messages

When `signals_scan` finds new signals:

```typescript
await pi.sendMessage!({
  customType: "signals-found",
  content: "Found 2 new signals...",
  display: false,  // Model sees, user doesn't
  details: { signals: [...] },
}, {
  triggerTurn: false,
  deliverAs: "followUp",
});
```

The model can decide whether to surface it.

---

## Files

**Signals storage:** `/home/majinbu/organized/active-projects/trading-system/quant/signals/`
- `signals.json` - Active and closed signals
- `outcomes.json` - Exit data (if CLI exists)

**CLI integration:** `~/Projects/trading-signals/src/cli.ts`
- Resolve command: `node --import tsx src/cli.ts resolve <id> <exit> <pnl>`

---

## Auto-Scan

Background poll every 5 minutes for XAU/XAG signals.

---

**Created:** 2026-02-21
**Based on:** Joel pattern (silent messages, auto-hide widgets, theme tokens)
