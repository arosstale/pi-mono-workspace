# ACO-Halftone Optimizer

**Ant Colony Optimization for Halftone Pattern Discovery**

---

## Overview

Uses Ant Colony Optimization (ACO) to discover optimal halftone patterns for camouflage, smart materials, and adaptive systems.

## Concept

```
Ants explore pattern space
       ↓
Deposit pheromones (fitness score)
       ↓
Evaporate old trails
       ↓
Emerges optimal pattern
```

## Installation

```bash
cd aco-halftone-optimizer
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from aco_halloptimizer import ACOHalftoneOptimizer

# Create optimizer
optimizer = ACOHalftoneOptimizer(
    n_ants=50,
    n_iterations=100,
    decay_rate=0.95
)

# Define environment
environment = {
    'type': 'desert',
    'lighting': 'high',
    'temperature': 35
}

# Optimize pattern
best_pattern, fitness = optimizer.optimize(
    environment=environment,
    objective='camouflage',
    resolution=64  # 64x64 pattern
)

print(f"Best fitness: {fitness}")
best_pattern.save('optimal_pattern.png')
```

### Command Line

```bash
# Find optimal camouflage for desert
python3 -m aco_halloptimizer \
    --environment desert \
    --objective camouflage \
    --resolution 64 \
    --ants 50 \
    --iterations 100

# Find optimal smart window pattern
python3 -m aco_halloptimizer \
    --environment building \
    --objective thermal_control \
    --resolution 128
```

## Patterns

| Environment | Objective | Best Pattern |
|------------|-----------|--------------|
| Desert | Camouflage | Low-frequency, high-contrast |
| Forest | Camouflage | Medium-frequency, organic |
| Urban | Camouflage | High-frequency, geometric |
| Building | Thermal | Gradient pattern |
| Vehicle | Adaptive | Multi-scale pattern |

## How It Works

### 1. Ant Exploration

Each ant constructs a halftone pattern by making binary decisions:

```python
class Ant:
    def construct_pattern(self, pheromones, environment):
        pattern = np.zeros((resolution, resolution))
        
        for i in range(resolution):
            for j in range(resolution):
                # Follow pheromone trail
                decision = self.follow_pheromones(pheromones, i, j)
                pattern[i, j] = decision
        
        return pattern
```

### 2. Fitness Evaluation

Pattern fitness is calculated based on objective:

```python
def evaluate_fitness(pattern, environment, objective):
    if objective == 'camouflage':
        # Calculate how well pattern blends with environment
        return calculate_blend_score(pattern, environment)
    elif objective == 'thermal_control':
        # Calculate heat blocking efficiency
        return calculate_thermal_efficiency(pattern)
```

### 3. Pheromone Update

```python
def update_pheromones(pheromones, results, decay_rate):
    # Evaporate old pheromones
    pheromones *= decay_rate
    
    # Deposit new pheromones based on fitness
    for result in results:
        pattern, fitness = result
        pheromones += pattern * fitness
```

### 4. Emergence

Over iterations, pheromone trails converge on optimal pattern.

## Advanced Usage

### Custom Fitness Function

```python
def my_fitness(pattern, environment):
    # Your custom fitness calculation
    score = 0
    
    # Example: prefer certain spatial frequencies
    freq_spectrum = np.fft.fft2(pattern)
    score += np.mean(freq_spectrum[10:20])
    
    # Example: penalize high frequency noise
    score -= np.std(pattern) * 0.1
    
    return score

optimizer.set_fitness_function(my_fitness)
```

### Multi-Objective Optimization

```python
optimizer.optimize_multi_objective(
    environment=env,
    objectives=['camouflage', 'thermal_control'],
    weights=[0.7, 0.3]  # 70% camouflage, 30% thermal
)
```

## Architecture

```
┌─────────────────────────────────────────┐
│         ACO-Halftone Optimizer          │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────────────────────────┐  │
│  │       Ant Colony                  │  │
│  │  - n_ants agents                 │  │
│  │  - Explore pattern space         │  │
│  │  - Follow pheromone trails       │  │
│  └───────────────────────────────────┘  │
│              │                          │
│              ▼                          │
│  ┌───────────────────────────────────┐  │
│  │      Pheromone Matrix            │  │
│  │  - fitness storage               │  │
│  │  - evaporate over time           │  │
│  │  - guide ant decisions           │  │
│  └───────────────────────────────────┘  │
│              │                          │
│              ▼                          │
│  ┌───────────────────────────────────┐  │
│  │     Fitness Evaluation           │  │
│  │  - camouflage score             │  │
│  │  - thermal efficiency           │  │
│  │  - custom functions              │  │
│  └───────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

## Examples

See `examples/` directory:
- `basic_camouflage.py` - Simple camouflage optimization
- `smart_window.py` - Thermal control pattern
- `multi_objective.py` - Multiple objectives
- `custom_fitness.py` - Custom fitness function

## References

- Dorigo, M. (1992). Optimization, learning and natural algorithms
- Nature Communications (2025). Halftone-encoded 4D printing
