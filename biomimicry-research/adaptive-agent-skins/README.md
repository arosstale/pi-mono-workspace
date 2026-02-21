# Adaptive Agent Skins

**Applying Cephalopod Hydrogel Concepts to AI Agents**

---

## Overview

AI agents with "digital chromatophores" that change behavior patterns based on environmental stimuli, inspired by cephalopod skin cells.

## Concept

```
Biological Chromatophore → Digital Chromatophore
     ├─ Pigment cell          ├─ Behavior module
     ├─ Radial muscle         ├─ Activation threshold
     ├─ Neural signal         ├─ Stimulus input
     └─ Color change          └─ Behavior output

Multiple Chromatophores → Emergent Behavior
Multiple Modules → Adaptive Agent Response
```

## Installation

```bash
cd adaptive-agent-skins
npm install
```

## Usage

### Basic Example

```typescript
import { AdaptiveAgentSkin, ChromatophoreModule } from '@biomimicry/agent-skin';

// Create skin with digital chromatophores
const skin = new AdaptiveAgentSkin({
  resolution: 64
});

// Add behavior modules (chromatophores)
const modules = [
  new ChromatophoreModule({
    name: 'coding',
    behavior: 'write_code',
    activationThreshold: 0.7,
    stimuli: ['programming', 'debug', 'implement']
  }),
  new ChromatophoreModule({
    name: 'research',
    behavior: 'search_web',
    activationThreshold: 0.6,
    stimuli: ['find', 'research', 'discover']
  }),
  new ChromatophoreModule({
    name: 'analysis',
    behavior: 'analyze',
    activationThreshold: 0.5,
    stimuli: ['explain', 'understand', 'break down']
  })
];

modules.forEach(m => skin.addModule(m));

// Respond to stimuli
const stimulus = {
  type: 'user_input',
  content: 'Implement a REST API for user management',
  intensity: 0.8
};

const response = skin.respond(stimulus);
console.log(response.behaviors);
// Output: ['write_code'] - coding module activated
```

### Advanced: Dynamic Thresholds

```typescript
// Chromatophore with dynamic threshold (like LCST response)
const dynamicModule = new ChromatophoreModule({
  name: 'safety_check',
  behavior: 'validate_safety',
  baseThreshold: 0.5,
  adaptive: true,
  thresholdType: 'lcst',  // Lower Critical Threshold
  thresholdParams: {
    critical: 0.7,
    below: 0.3,
    transition: 0.1
  }
});

// Threshold changes based on "temperature" (intensity)
const lowIntensity = { type: 'user_input', intensity: 0.2 };
dynamicModule.calculateThreshold(lowIntensity.intensity);
// Returns 0.3 (below critical, more permissive)

const highIntensity = { type: 'user_input', intensity: 0.8 };
dynamicModule.calculateThreshold(highIntensity.intensity);
// Returns 0.9 (above critical, more restrictive)
```

### Integration with OpenClaw

```typescript
// Create OpenClaw agent with adaptive skin
import { OpenClawAgent } from 'openclaw';

class AdaptiveOpenClawAgent {
  private agent: OpenClawAgent;
  private skin: AdaptiveAgentSkin;

  constructor(apiKey: string) {
    this.agent = new OpenClawAgent({ apiKey });
    this.skin = new AdaptiveAgentSkin();
    
    // Configure skin for OpenClaw context
    this.configureOpenClawSkin();
  }

  private configureOpenClawSkin() {
    // Add task-specific modules
    this.skin.addModule(new ChromatophoreModule({
      name: 'file_operations',
      behavior: 'read_write_files',
      activationThreshold: 0.6,
      stimuli: ['file', 'read', 'write', 'directory']
    }));

    this.skin.addModule(new ChromatophoreModule({
      name: 'tool_execution',
      behavior: 'execute_tool',
      activationThreshold: 0.7,
      stimuli: ['run', 'execute', 'command']
    }));

    this.skin.addModule(new ChromatophoreModule({
      name: 'web_search',
      behavior: 'search',
      activationThreshold: 0.5,
      stimuli: ['find', 'search', 'look up']
    }));
  }

  async handleRequest(request: string): Promise<Response> {
    // 1. Analyze stimulus
    const stimulus = this.analyzeStimulus(request);
    
    // 2. Get activated behaviors from skin
    const activeBehaviors = this.skin.respond(stimulus);
    
    // 3. Execute behaviors through OpenClaw agent
    const results = [];
    for (const behavior of activeBehaviors.behaviors) {
      const result = await this.executeBehavior(behavior, request);
      results.push(result);
    }
    
    // 4. Synthesize response
    return this.synthesizeResponse(results);
  }
}
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              Adaptive Agent Skin                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │        Digital Chromatophore Modules        │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐    │   │
│  │  │ Module 1│  │ Module 2│  │ Module 3│    │   │
│  │  │Coding   │  │Research │  │Analysis │    │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘    │   │
│  └───────┼────────────┼────────────┼──────────┘   │
│          │            │            │               │
│          ▼            ▼            ▼               │
│  ┌─────────────────────────────────────────────┐   │
│  │         Activation Logic                      │   │
│  │  - Threshold comparison                      │   │
│  │  - Stimulus pattern matching                │   │
│  │  - Adaptive thresholds (LCST-like)          │   │
│  └─────────────────────────────────────────────┘   │
│          │                                         │
│          ▼                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │         Emergent Behavior                    │   │
│  │  - Synthesize from active modules           │   │
│  │  - Context-aware response                   │   │
│  │  - Dynamic adaptation                       │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Chromatophore Module Types

| Module Type | Behavior | Use Case |
|-------------|----------|----------|
| **Static** | Fixed threshold | Reliable, predictable behavior |
| **LCST-Adaptive** | Threshold changes at critical intensity | Context-sensitive (like hydrogel temperature response) |
| **Hysteresis** | Different activation/deactivation thresholds | Prevent rapid toggling |
| **Reinforcement** | Threshold adjusts based on feedback | Learning over time |

## Examples

See `examples/` directory:
- `basic_agent.ts` - Simple adaptive agent
- `openclaw_integration.ts` - OpenClaw integration
- `lcst_thresholds.ts` - Adaptive thresholds demo
- `reinforcement_learning.ts` - Self-adapting modules

## API Reference

### ChromatophoreModule

```typescript
interface ChromatophoreConfig {
  name: string;
  behavior: string;
  activationThreshold: number;
  stimuli: string[];
  adaptive?: boolean;
  thresholdType?: 'static' | 'lcst' | 'hysteresis' | 'reinforcement';
  thresholdParams?: {
    critical?: number;
    below?: number;
    above?: number;
    transition?: number;
  };
}

class ChromatophoreModule {
  constructor(config: ChromatophoreConfig);
  
  activate(stimulus: Stimulus): boolean;
  calculateThreshold(intensity: number): number;
  updateThreshold(feedback: number): void;
}
```

### AdaptiveAgentSkin

```typescript
interface SkinConfig {
  resolution: number;
  decayRate?: number;
  learningRate?: number;
}

class AdaptiveAgentSkin {
  constructor(config: SkinConfig);
  
  addModule(module: ChromatophoreModule): void;
  removeModule(name: string): void;
  respond(stimulus: Stimulus): SkinResponse;
  learn(feedback: Feedback): void;
}
```

## Biological Inspiration

| Biological | Digital | Function |
|------------|---------|----------|
| **Chromatophore** | Module | Behavior unit |
| **Radial muscle** | Threshold | Activation control |
| **Neural signal** | Stimulus | Trigger input |
| **Pigment change** | Behavior output | Result |
| **LCST response** | Adaptive threshold | Context sensitivity |
| **Papillae formation** | Emergent behavior | Global response |

## Benefits

1. **Modularity** - Easy to add/remove behavior modules
2. **Adaptability** - Thresholds adjust to context
3. **Emergence** - Complex responses from simple modules
4. **Transparency** - Clear activation logic
5. **Biological fidelity** - Proven pattern from nature

## References

- Nature Communications (2025). Halftone-encoded 4D printing
- Cephalopod neurobiology research
