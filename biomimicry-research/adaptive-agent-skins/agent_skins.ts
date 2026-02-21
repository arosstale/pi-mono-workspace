/**
 * Adaptive Agent Skins
 * Applying cephalopod hydrogel concepts to AI agents
 */

// Types
export interface Stimulus {
  type: string;
  content: string;
  intensity: number; // 0-1
  metadata?: Record<string, any>;
}

export interface ChromatophoreConfig {
  name: string;
  behavior: string;
  activationThreshold: number; // 0-1
  stimuli: string[];
  adaptive?: boolean;
  thresholdType?: 'static' | 'lcst' | 'hysteresis' | 'reinforcement';
  thresholdParams?: ThresholdParams;
}

export interface ThresholdParams {
  critical?: number; // LCST critical value
  below?: number; // Threshold below critical
  above?: number; // Threshold above critical
  transition?: number; // Transition steepness
  hysteresisGap?: number; // Gap between activation/deactivation
  learningRate?: number; // For reinforcement
}

export interface SkinResponse {
  behaviors: string[];
  activeModules: string[];
  confidence: number;
  reasoning: string;
}

export interface Feedback {
  module: string;
  effectiveness: number; // 0-1
  context: Stimulus;
}

export interface SkinConfig {
  resolution: number;
  decayRate?: number;
  learningRate?: number;
}

/**
 * Digital Chromatophore Module
 * Analogous to biological chromatophore cells
 */
export class ChromatophoreModule {
  public name: string;
  public behavior: string;
  public activationThreshold: number;
  public stimuli: string[];
  public adaptive: boolean;
  public thresholdType: 'static' | 'lcst' | 'hysteresis' | 'reinforcement';
  public thresholdParams: ThresholdParams;
  
  // State
  private currentThreshold: number;
  private activationCount: number = 0;
  private lastActivation: boolean = false;

  constructor(config: ChromatophoreConfig) {
    this.name = config.name;
    this.behavior = config.behavior;
    this.activationThreshold = config.activationThreshold;
    this.stimuli = config.stimuli;
    this.adaptive = config.adaptive || false;
    this.thresholdType = config.thresholdType || 'static';
    this.thresholdParams = config.thresholdParams || {};
    
    this.currentThreshold = this.activationThreshold;
  }

  /**
   * Calculate match score for stimulus
   */
  private calculateMatch(stimulus: Stimulus): number {
    let matchScore = 0;
    
    // Check stimulus type
    if (this.stimuli.includes(stimulus.type)) {
      matchScore += 0.5;
    }
    
    // Check content for stimulus keywords
    const content = stimulus.content.toLowerCase();
    for (const keyword of this.stimuli) {
      if (content.includes(keyword.toLowerCase())) {
        matchScore += 0.25;
      }
    }
    
    // Apply intensity
    matchScore *= stimulus.intensity;
    
    return Math.min(1, matchScore);
  }

  /**
   * Calculate adaptive threshold based on intensity (LCST-like)
   */
  private calculateLCSTThreshold(intensity: number): number {
    const { critical = 0.5, below = 0.3, above = 0.7, transition = 0.1 } = this.thresholdParams;
    
    if (intensity < critical - transition) {
      return below;
    } else if (intensity > critical + transition) {
      return above;
    } else {
      // Smooth transition
      const t = (intensity - (critical - transition)) / (2 * transition);
      return below + (above - below) * t;
    }
  }

  /**
   * Calculate hysteresis threshold (prevents rapid toggling)
   */
  private calculateHysteresisThreshold(): number {
    const { hysteresisGap = 0.1 } = this.thresholdParams;
    
    if (this.lastActivation) {
      return this.activationThreshold - hysteresisGap;
    } else {
      return this.activationThreshold + hysteresisGap;
    }
  }

  /**
   * Calculate current threshold
   */
  calculateThreshold(intensity: number): number {
    if (!this.adaptive) {
      return this.activationThreshold;
    }
    
    switch (this.thresholdType) {
      case 'lcst':
        return this.calculateLCSTThreshold(intensity);
      case 'hysteresis':
        return this.calculateHysteresisThreshold();
      case 'reinforcement':
        return this.currentThreshold;
      default:
        return this.activationThreshold;
    }
  }

  /**
   * Check if module should activate
   */
  activate(stimulus: Stimulus): boolean {
    const matchScore = this.calculateMatch(stimulus);
    const threshold = this.calculateThreshold(stimulus.intensity);
    
    const shouldActivate = matchScore >= threshold;
    
    if (shouldActivate) {
      this.activationCount++;
      this.lastActivation = true;
    } else {
      this.lastActivation = false;
    }
    
    return shouldActivate;
  }

  /**
   * Update threshold based on feedback (reinforcement learning)
   */
  updateThreshold(feedback: Feedback): void {
    if (feedback.module !== this.name || this.thresholdType !== 'reinforcement') {
      return;
    }
    
    const learningRate = this.thresholdParams.learningRate || 0.1;
    const effectiveness = feedback.effectiveness;
    
    if (effectiveness > 0.7) {
      // Effective - lower threshold to activate more easily
      this.currentThreshold *= (1 - learningRate * 0.5);
    } else if (effectiveness < 0.3) {
      // Ineffective - raise threshold
      this.currentThreshold *= (1 + learningRate);
    }
    
    // Keep threshold in valid range
    this.currentThreshold = Math.max(0.1, Math.min(0.9, this.currentThreshold));
  }

  /**
   * Get module stats
   */
  getStats() {
    return {
      name: this.name,
      behavior: this.behavior,
      currentThreshold: this.currentThreshold,
      activationCount: this.activationCount,
      adaptive: this.adaptive,
      thresholdType: this.thresholdType
    };
  }
}

/**
 * Adaptive Agent Skin
 * Manages digital chromatophore modules
 */
export class AdaptiveAgentSkin {
  private modules: Map<string, ChromatophoreModule> = new Map();
  private resolution: number;
  private decayRate: number;
  private learningRate: number;
  private responseHistory: SkinResponse[] = [];

  constructor(config: SkinConfig) {
    this.resolution = config.resolution;
    this.decayRate = config.decayRate || 0.95;
    this.learningRate = config.learningRate || 0.1;
  }

  /**
   * Add a chromatophore module
   */
  addModule(module: ChromatophoreModule): void {
    this.modules.set(module.name, module);
  }

  /**
   * Remove a chromatophore module
   */
  removeModule(name: string): void {
    this.modules.delete(name);
  }

  /**
   * Get a module by name
   */
  getModule(name: string): ChromatophoreModule | undefined {
    return this.modules.get(name);
  }

  /**
   * Get all modules
   */
  getAllModules(): ChromatophoreModule[] {
    return Array.from(this.modules.values());
  }

  /**
   * Respond to stimulus with emergent behavior
   */
  respond(stimulus: Stimulus): SkinResponse {
    const activeModules: string[] = [];
    const behaviors: string[] = [];
    let totalMatchScore = 0;
    
    // Check all modules for activation
    for (const module of this.modules.values()) {
      if (module.activate(stimulus)) {
        activeModules.push(module.name);
        behaviors.push(module.behavior);
        totalMatchScore += 1;
      }
    }
    
    // Calculate confidence
    const confidence = this.modules.size > 0 
      ? totalMatchScore / this.modules.size 
      : 0;
    
    // Generate reasoning
    const reasoning = this.generateReasoning(activeModules, stimulus);
    
    const response: SkinResponse = {
      behaviors,
      activeModules,
      confidence,
      reasoning
    };
    
    // Store in history
    this.responseHistory.push(response);
    
    // Decay history
    if (this.responseHistory.length > this.resolution) {
      this.responseHistory.shift();
    }
    
    return response;
  }

  /**
   * Learn from feedback
   */
  learn(feedback: Feedback): void {
    const module = this.modules.get(feedback.module);
    if (module) {
      module.updateThreshold(feedback);
    }
  }

  /**
   * Generate reasoning explanation
   */
  private generateReasoning(activeModules: string[], stimulus: Stimulus): string {
    if (activeModules.length === 0) {
      return `No modules activated for stimulus: "${stimulus.content}"`;
    }
    
    const moduleNames = activeModules.join(', ');
    return `Activated modules [${moduleNames}] in response to "${stimulus.content}" with intensity ${stimulus.intensity.toFixed(2)}`;
  }

  /**
   * Get skin statistics
   */
  getStats() {
    return {
      totalModules: this.modules.size,
      activeThresholds: Array.from(this.modules.values()).map(m => m.getStats()),
      responseHistoryLength: this.responseHistory.length
    };
  }

  /**
   * Export skin configuration
   */
  exportConfig(): Record<string, any> {
    return {
      modules: Array.from(this.modules.values()).map(m => m.getStats()),
      config: {
        resolution: this.resolution,
        decayRate: this.decayRate,
        learningRate: this.learningRate
      }
    };
  }
}

/**
 * Factory function to create pre-configured skins
 */
export function createOpenClawSkin(): AdaptiveAgentSkin {
  const skin = new AdaptiveAgentSkin({ resolution: 50 });
  
  // File operations module
  skin.addModule(new ChromatophoreModule({
    name: 'file_operations',
    behavior: 'read_write_files',
    activationThreshold: 0.6,
    stimuli: ['file', 'read', 'write', 'directory', 'path']
  }));
  
  // Tool execution module
  skin.addModule(new ChromatophoreModule({
    name: 'tool_execution',
    behavior: 'execute_tool',
    activationThreshold: 0.7,
    stimuli: ['run', 'execute', 'command', 'tool', 'function']
  }));
  
  // Web search module
  skin.addModule(new ChromatophoreModule({
    name: 'web_search',
    behavior: 'search',
    activationThreshold: 0.5,
    stimuli: ['find', 'search', 'look up', 'research', 'discover']
  }));
  
  // Coding module (LCST adaptive)
  skin.addModule(new ChromatophoreModule({
    name: 'coding',
    behavior: 'write_code',
    activationThreshold: 0.6,
    stimuli: ['code', 'implement', 'develop', 'function', 'class'],
    adaptive: true,
    thresholdType: 'lcst',
    thresholdParams: {
      critical: 0.5,
      below: 0.4,
      above: 0.8,
      transition: 0.1
    }
  }));
  
  return skin;
}

/**
 * Demo: Basic adaptive agent
 */
export function demoAdaptiveAgent() {
  console.log('🐙 Adaptive Agent Skin Demo');
  console.log('='.repeat(50));
  
  // Create skin with OpenClaw configuration
  const skin = createOpenClawSkin();
  
  console.log(`\nInitialized skin with ${skin.getStats().totalModules} modules`);
  
  // Test various stimuli
  const testCases: Stimulus[] = [
    {
      type: 'user_input',
      content: 'Read the file README.md',
      intensity: 0.8
    },
    {
      type: 'user_input',
      content: 'Search for information about cephalopods',
      intensity: 0.7
    },
    {
      type: 'user_input',
      content: 'Implement a REST API endpoint',
      intensity: 0.9
    },
    {
      type: 'user_input',
      content: 'What is the weather today?',
      intensity: 0.5
    }
  ];
  
  console.log('\n📝 Testing stimuli responses:\n');
  
  for (const testCase of testCases) {
    const response = skin.respond(testCase);
    
    console.log(`Input: "${testCase.content}"`);
    console.log(`  Active modules: [${response.activeModules.join(', ') || 'none'}]`);
    console.log(`  Behaviors: [${response.behaviors.join(', ') || 'none'}]`);
    console.log(`  Confidence: ${(response.confidence * 100).toFixed(1)}%`);
    console.log(`  Reasoning: ${response.reasoning}`);
    console.log();
  }
  
  return skin;
}

if (typeof require !== 'undefined' && require.main === module) {
  demoAdaptiveAgent();
}
