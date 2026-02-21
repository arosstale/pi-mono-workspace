# Homeostatic Safety Layers

**Dynamic Safety Regulation Inspired by Biological Homeostasis**

---

## Overview

Safety systems that self-regulate like biological systems, using negative feedback loops to maintain optimal security levels without manual intervention.

## Concept

```
Biological Homeostasis → Digital Homeostasis
     ├─ Temperature regulation ├─ Threat level regulation
     ├─ Negative feedback      ├─ Dynamic thresholds
     ├─ Set point             ├─ Target safety level
     ├─ Sensor input          ├─ Monitoring input
     └─ Effector output       └─ Safety action output

Body maintains 37°C → System maintains optimal safety
```

## Installation

```bash
cd homeostatic-safety
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from homeostatic_safety import HomeostaticSafetyLayer

# Create safety layer
safety = HomeostaticSafetyLayer(
    target_safety_level=0.7,  # Target: 70% safety
    learning_rate=0.1,
    hysteresis=0.1
)

# Monitor and regulate
threats = [
    Threat(type='sql_injection', severity=0.9),
    Threat(type='xss', severity=0.3),
    Threat(type='rate_limit', severity=0.5)
]

action = safety.regulate(threats)
print(action.decision)  # 'INCREASE_SAFETY'
print(action.new_level)  # 0.85 (increased due to high threats)
print(action.reason)    # 'Threat level 0.57 > target 0.7'
```

### Multi-Layer Safety System

```python
from homeostatic_safety import HomeostaticSafetySystem

# Create multi-layer system
system = HomeostaticSafetySystem()

# Add layers with different target levels
system.add_layer('input_filter', target=0.8)
system.add_layer('output_filter', target=0.7)
system.add_layer('execution_control', target=0.9)

# Evaluate action across all layers
action = Action(
    type='execute',
    command='rm -rf /',
    context={'user': 'untrusted'}
)

result = system.evaluate(action)
print(result.decision)  # 'BLOCKED'
print(result.blocked_by)  # ['input_filter', 'execution_control']
```

### Integration with OpenClaw

```python
from openclaw import OpenClawAgent
from homeostatic_safety import HomeostaticSafetyLayer

class SafeOpenClawAgent:
    def __init__(self, api_key):
        self.agent = OpenClawAgent(api_key=api_key)
        self.safety = HomeostaticSafetyLayer(target_safety_level=0.7)
    
    def execute(self, request):
        # Analyze threat
        threat = self.analyze_threat(request)
        
        # Regulate safety
        safety_action = self.safety.regulate([threat])
        
        if safety_action.decision == 'BLOCK':
            return {
                'success': False,
                'reason': f'Blocked by safety: {safety_action.reason}'
            }
        
        # Execute with current safety level
        result = self.agent.execute(
            request,
            safety_threshold=safety_action.current_level
        )
        
        # Learn from result
        if result['success']:
            self.safety.learn(effectiveness=0.9)
        else:
            self.safety.learn(effectiveness=0.2)
        
        return result
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│          Homeostatic Safety Layer                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │        Threat Detection                       │   │
│  │  - Analyze incoming actions                 │   │
│  │  - Calculate threat severity                 │   │
│  │  - Identify threat types                    │   │
│  └─────────────────────────────────────────────┘   │
│          │                                         │
│          ▼                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │        Safety Level Calculation             │   │
│  │  current_level = 1 - threat_level          │   │
│  │  (0 = no safety, 1 = maximum safety)      │   │
│  └─────────────────────────────────────────────┘   │
│          │                                         │
│          ▼                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │        Negative Feedback Loop               │   │
│  │                                            │   │
│  │  error = current_level - target            │   │
│  │  adjustment = -k * error                   │   │
│  │  new_level = current_level + adjustment    │   │
│  │                                            │   │
│  │  (k = proportional gain)                   │   │
│  └─────────────────────────────────────────────┘   │
│          │                                         │
│          ▼                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │        Safety Action                        │   │
│  │  - INCREASE_SAFETY (add restrictions)      │   │
│  │  - DECREASE_SAFETY (relax restrictions)    │   │
│  │  - MAINTAIN (no change)                    │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Safety Regulation Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| **Proportional** | Adjust based on error magnitude | Smooth, continuous adjustment |
| **Hysteresis** | Deadband prevents rapid toggling | Stable in noisy environments |
| **Adaptive** | Gain adjusts based on conditions | Dynamic threat environments |
| **Predictive** | Anticipate based on trend | Proactive threat prevention |

## Threat Detection

| Threat Type | Detection Method | Severity Factors |
|-------------|------------------|------------------|
| **SQL Injection** | Pattern matching | Query complexity, blacklisted keywords |
| **XSS** | HTML sanitization check | Script tags, event handlers |
| **Command Injection** | Shell metacharacters detection | Pipes, redirects, command substitution |
| **Path Traversal** | Path normalization check | `../`, absolute paths |
| **Rate Limit** | Request frequency | Requests per minute |
| **Malicious Intent** | NLP analysis | Suspicious keywords, jailbreak patterns |

## Examples

See `examples/` directory:
- `basic_homeostasis.py` - Simple safety regulation
- `multi_layer_system.py` - Layered safety
- `openclaw_integration.py` - OpenClaw integration
- `adaptive_control.py` - Adaptive control modes

## API Reference

### Threat

```python
@dataclass
class Threat:
    type: str
    severity: float  # 0-1
    source: str
    metadata: dict
```

### SafetyAction

```python
@dataclass
class SafetyAction:
    decision: str  # 'INCREASE_SAFETY', 'DECREASE_SAFETY', 'MAINTAIN'
    new_level: float  # 0-1
    current_level: float
    reason: str
    blocked_threats: List[Threat]
```

### HomeostaticSafetyLayer

```python
class HomeostaticSafetyLayer:
    def __init__(
        self,
        target_safety_level: float = 0.7,
        learning_rate: float = 0.1,
        hysteresis: float = 0.1,
        control_mode: str = 'proportional'
    )
    
    def regulate(self, threats: List[Threat]) -> SafetyAction
    def learn(self, effectiveness: float) -> None
    def get_status(self) -> dict
```

## Biological Inspiration

| Biological | Digital | Function |
|------------|---------|----------|
| **Hypothalamus** | Safety controller | Regulation center |
| **Thermoreceptors** | Threat detectors | Sensor input |
| **Blood vessels** | Safety filters | Effector output |
| **Sweat glands** | Mitigation actions | Cooling down |
| **Shivering** | Defensive actions | Warming up |
| **Set point (37°C)** | Target safety level | Homeostatic target |

## Benefits

1. **Self-regulating** - No manual threshold tuning
2. **Dynamic** - Adapts to changing threat landscape
3. **Proportional** - Response scales with threat severity
4. **Stable** - Hysteresis prevents rapid toggling
5. **Proven** - Billions of years of evolutionary refinement

## Mathematical Model

### Proportional Control

```
error = current_safety - target_safety
adjustment = -k_p * error
new_safety = current_safety + adjustment
```

### Proportional-Integral Control

```
integral += error * dt
adjustment = -k_p * error - k_i * integral
new_safety = current_safety + adjustment
```

### Hysteresis

```
if current > target + hysteresis:
    action = 'DECREASE_SAFETY'
elif current < target - hysteresis:
    action = 'INCREASE_SAFETY'
else:
    action = 'MAINTAIN'
```

## References

- Cannon, W. (1932). The Wisdom of the Body
- Claude Bernard (1865). Introduction to the Study of Experimental Medicine
- Feedback control theory
