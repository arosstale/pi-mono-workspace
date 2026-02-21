"""
ACO-Halftone Optimizer
Ant Colony Optimization for Halftone Pattern Discovery
"""

import numpy as np
from typing import Tuple, Dict, List, Callable, Optional
from dataclasses import dataclass
import random


@dataclass
class Environment:
    """Environment definition for pattern optimization"""
    type: str  # desert, forest, urban, building, vehicle
    lighting: str  # low, medium, high
    temperature: float  # in Celsius
    humidity: float = 0.5  # 0-1


@dataclass
class OptimizationResult:
    """Result from optimization run"""
    pattern: np.ndarray
    fitness: float
    iterations: int
    final_pheromones: np.ndarray
    convergence_history: List[float]


class HalftonePattern:
    """Halftone pattern representation"""
    
    def __init__(self, pixels: np.ndarray):
        self.pixels = pixels
        self.resolution = pixels.shape[0]
    
    @classmethod
    def create_random(cls, resolution: int) -> 'HalftonePattern':
        """Create random halftone pattern"""
        pixels = np.random.randint(0, 2, (resolution, resolution))
        return cls(pixels)
    
    @classmethod
    def create_from_pheromones(
        cls,
        pheromones: np.ndarray,
        threshold: Optional[float] = None
    ) -> 'HalftonePattern':
        """Create pattern from pheromone matrix"""
        if threshold is None:
            threshold = np.mean(pheromones)
        pixels = (pheromones > threshold).astype(int)
        return cls(pixels)
    
    def save(self, filename: str):
        """Save pattern to file"""
        from PIL import Image
        img = Image.fromarray((self.pixels * 255).astype(np.uint8), mode='L')
        img.save(filename)
    
    def get_spatial_frequency(self) -> np.ndarray:
        """Get spatial frequency spectrum"""
        return np.fft.fft2(self.pixels)
    
    def get_entropy(self) -> float:
        """Calculate pattern entropy"""
        hist, _ = np.histogram(self.pixels, bins=2, range=(0, 1))
        hist = hist / np.sum(hist)
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        return entropy


class Ant:
    """Ant agent for ACO optimization"""
    
    def __init__(self, id: int):
        self.id = id
        self.current_pattern: Optional[HalftonePattern] = None
        self.fitness: float = 0.0
    
    def construct_pattern(
        self,
        resolution: int,
        pheromones: np.ndarray,
        exploration_rate: float = 0.1
    ) -> HalftonePattern:
        """
        Construct halftone pattern by following pheromone trails
        
        Args:
            resolution: Pattern resolution (N x N)
            pheromones: Pheromone matrix guiding decisions
            exploration_rate: Probability of random exploration
        """
        pattern = np.zeros((resolution, resolution))
        
        for i in range(resolution):
            for j in range(resolution):
                # Follow pheromone trail with probability
                if random.random() < exploration_rate:
                    # Explore randomly
                    pattern[i, j] = random.randint(0, 1)
                else:
                    # Follow pheromone trail
                    pattern[i, j] = 1 if pheromones[i, j] > 0.5 else 0
        
        self.current_pattern = HalftonePattern(pattern)
        return self.current_pattern


class ACOHalftoneOptimizer:
    """
    Ant Colony Optimization for Halftone Pattern Discovery
    
    Uses ant colony optimization to discover optimal halftone patterns
    for camouflage, thermal control, and other applications.
    """
    
    def __init__(
        self,
        n_ants: int = 50,
        n_iterations: int = 100,
        decay_rate: float = 0.95,
        exploration_rate: float = 0.1,
        resolution: int = 64
    ):
        """
        Initialize ACO-Halftone Optimizer
        
        Args:
            n_ants: Number of ants in colony
            n_iterations: Maximum iterations
            decay_rate: Pheromone evaporation rate (0-1)
            exploration_rate: Random exploration probability
            resolution: Pattern resolution (N x N)
        """
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.decay_rate = decay_rate
        self.exploration_rate = exploration_rate
        self.resolution = resolution
        
        # Initialize pheromone matrix
        self.pheromones = np.random.random((resolution, resolution))
        
        # Create ant colony
        self.ants = [Ant(i) for i in range(n_ants)]
        
        # Fitness function (can be customized)
        self.fitness_function: Optional[Callable] = None
        
        # History tracking
        self.best_fitness_history: List[float] = []
        self.best_pattern: Optional[HalftonePattern] = None
        self.best_fitness: float = 0.0
    
    def set_fitness_function(self, func: Callable):
        """Set custom fitness function"""
        self.fitness_function = func
    
    def _evaluate_fitness(
        self,
        pattern: HalftonePattern,
        environment: Environment,
        objective: str
    ) -> float:
        """
        Evaluate pattern fitness based on objective
        
        Args:
            pattern: Halftone pattern to evaluate
            environment: Environment context
            objective: Optimization objective
            
        Returns:
            Fitness score (0-1, higher is better)
        """
        # Use custom fitness function if provided
        if self.fitness_function:
            return self.fitness_function(pattern, environment, objective)
        
        # Default fitness evaluation
        if objective == 'camouflage':
            return self._camouflage_fitness(pattern, environment)
        elif objective == 'thermal_control':
            return self._thermal_fitness(pattern, environment)
        else:
            return self._generic_fitness(pattern, environment)
    
    def _camouflage_fitness(
        self,
        pattern: HalftonePattern,
        environment: Environment
    ) -> float:
        """Calculate camouflage fitness"""
        pixels = pattern.pixels
        
        # Spatial frequency analysis
        freq = np.fft.fft2(pixels)
        freq_magnitude = np.abs(freq)
        
        # Fitness factors
        fitness = 0.0
        
        # 1. Prefer medium spatial frequencies for most environments
        freq_score = 1.0 - np.std(freq_magnitude[10:30]) / np.mean(freq_magnitude)
        fitness += 0.4 * freq_score
        
        # 2. Prefer moderate density (not too sparse, not too dense)
        density = np.mean(pixels)
        density_score = 1.0 - abs(density - 0.5)
        fitness += 0.3 * density_score
        
        # 3. Prefer some pattern entropy (not solid, not random)
        entropy = pattern.get_entropy()
        entropy_score = 1.0 - abs(entropy - 0.8)
        fitness += 0.3 * entropy_score
        
        return max(0.0, min(1.0, fitness))
    
    def _thermal_fitness(
        self,
        pattern: HalftonePattern,
        environment: Environment
    ) -> float:
        """Calculate thermal control fitness"""
        pixels = pattern.pixels
        
        # Prefer gradient patterns for thermal control
        gradients_x = np.diff(pixels, axis=1)
        gradients_y = np.diff(pixels, axis=0)
        
        # Calculate smoothness
        gradient_magnitude = np.mean(np.abs(gradients_x)) + np.mean(np.abs(gradients_y))
        smoothness_score = 1.0 - min(1.0, gradient_magnitude)
        
        # Prefer progressive density changes
        row_densities = np.mean(pixels, axis=1)
        gradient_smoothness = 1.0 - np.std(np.diff(row_densities))
        
        fitness = 0.5 * smoothness_score + 0.5 * gradient_smoothness
        
        return max(0.0, min(1.0, fitness))
    
    def _generic_fitness(
        self,
        pattern: HalftonePattern,
        environment: Environment
    ) -> float:
        """Generic fitness evaluation"""
        return 0.5  # Neutral fitness
    
    def _deposit_pheromones(
        self,
        ants: List[Ant],
        fitnesses: np.ndarray
    ):
        """
        Deposit pheromones based on ant fitness scores
        
        Args:
            ants: List of ants with constructed patterns
            fitnesses: Fitness scores for each ant
        """
        for ant, fitness in zip(ants, fitnesses):
            if ant.current_pattern:
                pattern = ant.current_pattern.pixels
                # Deposit pheromones proportional to fitness
                deposit = pattern * fitness
                self.pheromones += deposit
    
    def _evaporate_pheromones(self):
        """Evaporate pheromone trails"""
        self.pheromones *= self.decay_rate
    
    def optimize(
        self,
        environment: Environment,
        objective: str = 'camouflage'
    ) -> OptimizationResult:
        """
        Run ACO optimization
        
        Args:
            environment: Environment context
            objective: Optimization objective
            
        Returns:
            Optimization result with best pattern and metadata
        """
        convergence_history = []
        
        for iteration in range(self.n_iterations):
            # Deploy ants to construct patterns
            patterns = []
            fitnesses = []
            
            for ant in self.ants:
                pattern = ant.construct_pattern(
                    self.resolution,
                    self.pheromones,
                    self.exploration_rate
                )
                fitness = self._evaluate_fitness(pattern, environment, objective)
                ant.fitness = fitness
                
                patterns.append(pattern)
                fitnesses.append(fitness)
                
                # Track best
                if fitness > self.best_fitness:
                    self.best_fitness = fitness
                    self.best_pattern = pattern
            
            # Evaporate pheromones
            self._evaporate_pheromones()
            
            # Deposit new pheromones
            self._deposit_pheromones(self.ants, np.array(fitnesses))
            
            # Record convergence
            convergence_history.append(self.best_fitness)
            
            # Early termination if converged
            if iteration > 20:
                recent_variance = np.var(convergence_history[-10:])
                if recent_variance < 0.001:
                    break
        
        return OptimizationResult(
            pattern=self.best_pattern,
            fitness=self.best_fitness,
            iterations=len(convergence_history),
            final_pheromones=self.pheromones.copy(),
            convergence_history=convergence_history
        )
    
    def optimize_multi_objective(
        self,
        environment: Environment,
        objectives: List[str],
        weights: Optional[List[float]] = None
    ) -> OptimizationResult:
        """
        Multi-objective optimization
        
        Args:
            environment: Environment context
            objectives: List of objectives
            weights: Weights for each objective (default: equal)
            
        Returns:
            Optimization result
        """
        if weights is None:
            weights = [1.0 / len(objectives)] * len(objectives)
        
        # Create multi-objective fitness function
        def multi_fitness(pattern, env, obj):
            scores = []
            for obj_type in objectives:
                score = self._evaluate_fitness(pattern, env, obj_type)
                scores.append(score)
            return np.sum([s * w for s, w in zip(scores, weights)])
        
        # Set and run
        self.set_fitness_function(multi_fitness)
        return self.optimize(environment, 'multi_objective')


def create_optimizer(
    n_ants: int = 50,
    n_iterations: int = 100,
    resolution: int = 64
) -> ACOHalftoneOptimizer:
    """Factory function to create optimizer"""
    return ACOHalftoneOptimizer(
        n_ants=n_ants,
        n_iterations=n_iterations,
        resolution=resolution
    )


def demo_camouflage_optimization():
    """Demo: Optimize camouflage pattern for desert environment"""
    print("🐜 ACO-Halftone Optimizer Demo: Desert Camouflage")
    print("=" * 50)
    
    # Create optimizer
    optimizer = create_optimizer(
        n_ants=50,
        n_iterations=100,
        resolution=64
    )
    
    # Define desert environment
    desert_env = Environment(
        type='desert',
        lighting='high',
        temperature=40
    )
    
    # Optimize
    print(f"\nOptimizing for desert camouflage...")
    result = optimizer.optimize(desert_env, 'camouflage')
    
    print(f"\n✓ Optimization complete!")
    print(f"  Best fitness: {result.fitness:.4f}")
    print(f"  Iterations: {result.iterations}")
    print(f"  Pattern resolution: {result.pattern.resolution}x{result.pattern.resolution}")
    
    # Save pattern
    result.pattern.save('desert_camouflage.png')
    print(f"\n📁 Pattern saved to: desert_camouflage.png")
    
    return result


if __name__ == '__main__':
    demo_camouflage_optimization()
