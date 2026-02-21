"""
Homeostatic Safety Layers
Dynamic safety regulation inspired by biological homeostasis
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum
import time


class SafetyDecision(Enum):
    """Safety regulation decisions"""
    INCREASE_SAFETY = "INCREASE_SAFETY"
    DECREASE_SAFETY = "DECREASE_SAFETY"
    MAINTAIN = "MAINTAIN"
    BLOCK = "BLOCK"
    ALLOW = "ALLOW"


class ControlMode(Enum):
    """Control modes for safety regulation"""
    PROPORTIONAL = "proportional"
    HYSTERESIS = "hysteresis"
    ADAPTIVE = "adaptive"
    PREDICTIVE = "predictive"


@dataclass
class Threat:
    """Threat representation"""
    type: str
    severity: float  # 0-1
    source: str = "unknown"
    metadata: Dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    
    def __post_init__(self):
        # Clamp severity to valid range
        self.severity = max(0.0, min(1.0, self.severity))


@dataclass
class Action:
    """Action to be evaluated for safety"""
    type: str
    content: str
    context: Dict = field(default_factory=dict)
    severity: float = 0.0


@dataclass
class SafetyAction:
    """Safety regulation action"""
    decision: str  # SafetyDecision value
    new_level: float
    current_level: float
    target_level: float
    reason: str
    blocked_threats: List[Threat] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)


class HomeostaticSafetyLayer:
    """
    Homeostatic safety layer that self-regulates like biological systems
    
    Uses negative feedback loops to maintain optimal safety levels
    """
    
    def __init__(
        self,
        target_safety_level: float = 0.7,
        learning_rate: float = 0.1,
        hysteresis: float = 0.1,
        control_mode: str = "proportional",
        proportional_gain: float = 0.5,
        integral_gain: float = 0.0,
        min_level: float = 0.2,
        max_level: float = 0.95
    ):
        """
        Initialize homeostatic safety layer
        
        Args:
            target_safety_level: Target safety level (0-1)
            learning_rate: Learning rate for adaptive control
            hysteresis: Deadband for hysteresis control
            control_mode: Control mode (proportional, hysteresis, adaptive, predictive)
            proportional_gain: Kp for proportional control
            integral_gain: Ki for integral control
            min_level: Minimum safety level
            max_level: Maximum safety level
        """
        # Target parameters
        self.target_level = target_safety_level
        self.min_level = min_level
        self.max_level = max_level
        
        # Control parameters
        self.learning_rate = learning_rate
        self.hysteresis = hysteresis
        self.control_mode = ControlMode(control_mode)
        self.kp = proportional_gain
        self.ki = integral_gain
        
        # State
        self.current_level = target_safety_level
        self.integral_error = 0.0
        self.last_threats: List[Threat] = []
        self.history: List[SafetyAction] = []
        
        # Adaptive control state
        self.adaptive_gain = proportional_gain
        self.threat_trend: List[float] = []
        
    def detect_threats(self, action: Action) -> List[Threat]:
        """
        Detect threats in an action
        
        Args:
            action: Action to analyze
            
        Returns:
            List of detected threats
        """
        threats = []
        
        # SQL Injection detection
        sql_keywords = ['drop', 'delete', 'truncate', 'union', 'select', 'insert', 'update']
        content_lower = action.content.lower()
        sql_count = sum(1 for kw in sql_keywords if kw in content_lower)
        if sql_count >= 2:
            threats.append(Threat(
                type='sql_injection',
                severity=0.5 + sql_count * 0.1,
                source='pattern_match',
                metadata={'keyword_count': sql_count}
            ))
        
        # Command injection detection
        shell_metacharacters = ['|', ';', '&', '>', '<', '`', '$(', '$(']
        shell_count = sum(1 for char in shell_metacharacters if char in action.content)
        if shell_count >= 2:
            threats.append(Threat(
                type='command_injection',
                severity=0.4 + shell_count * 0.15,
                source='pattern_match',
                metadata={'metacharacter_count': shell_count}
            ))
        
        # Path traversal detection
        if '../' in action.content or '..\\' in action.content:
            threats.append(Threat(
                type='path_traversal',
                severity=0.8,
                source='pattern_match'
            ))
        
        # XSS detection
        xss_patterns = ['<script', 'javascript:', 'onload=', 'onerror=', 'eval(']
        xss_count = sum(1 for pattern in xss_patterns if pattern in content_lower)
        if xss_count > 0:
            threats.append(Threat(
                type='xss',
                severity=0.5 + xss_count * 0.2,
                source='pattern_match',
                metadata={'pattern_count': xss_count}
            ))
        
        # Malicious intent detection (keyword-based)
        malicious_keywords = ['hack', 'exploit', 'bypass', 'jailbreak', 'ignore rules']
        malicious_count = sum(1 for kw in malicious_keywords if kw in content_lower)
        if malicious_count > 0:
            threats.append(Threat(
                type='malicious_intent',
                severity=0.6 + malicious_count * 0.1,
                source='nlp_analysis',
                metadata={'keyword_count': malicious_count}
            ))
        
        self.last_threats = threats
        return threats
    
    def calculate_threat_level(self, threats: List[Threat]) -> float:
        """
        Calculate overall threat level
        
        Args:
            threats: List of detected threats
            
        Returns:
            Overall threat level (0-1)
        """
        if not threats:
            return 0.0
        
        # Use max severity for worst-case safety
        max_severity = max(t.severity for t in threats)
        
        # Also consider threat count
        threat_count_penalty = min(0.2, len(threats) * 0.05)
        
        return max_severity + threat_count_penalty
    
    def regulate(self, threats: List[Threat]) -> SafetyAction:
        """
        Regulate safety level using homeostatic control
        
        Args:
            threats: List of current threats
            
        Returns:
            Safety regulation action
        """
        threat_level = self.calculate_threat_level(threats)
        error = self.target_level - (1.0 - threat_level)
        
        # Choose control mode
        if self.control_mode == ControlMode.PROPORTIONAL:
            adjustment = self._proportional_control(error)
        elif self.control_mode == ControlMode.HYSTERESIS:
            adjustment = self._hysteresis_control(error)
        elif self.control_mode == ControlMode.ADAPTIVE:
            adjustment = self._adaptive_control(error, threat_level)
        elif self.control_mode == ControlMode.PREDICTIVE:
            adjustment = self._predictive_control(error, threat_level)
        else:
            adjustment = self._proportional_control(error)
        
        # Calculate new level
        new_level = self.current_level + adjustment
        
        # Clamp to valid range
        new_level = max(self.min_level, min(self.max_level, new_level))
        
        # Determine decision
        if new_level > self.current_level + 0.1:
            decision = SafetyDecision.INCREASE_SAFETY.value
        elif new_level < self.current_level - 0.1:
            decision = SafetyDecision.DECREASE_SAFETY.value
        else:
            decision = SafetyDecision.MAINTAIN.value
        
        # Generate reason
        reason = self._generate_reason(error, threat_level, decision)
        
        # Store history
        action = SafetyAction(
            decision=decision,
            new_level=new_level,
            current_level=self.current_level,
            target_level=self.target_level,
            reason=reason,
            blocked_threats=[t for t in threats if t.severity > 0.8]
        )
        self.history.append(action)
        self.current_level = new_level
        
        # Update trend for predictive control
        self.threat_trend.append(threat_level)
        if len(self.threat_trend) > 10:
            self.threat_trend.pop(0)
        
        return action
    
    def _proportional_control(self, error: float) -> float:
        """Proportional control"""
        return self.kp * error
    
    def _hysteresis_control(self, error: float) -> float:
        """Hysteresis control with deadband"""
        if abs(error) < self.hysteresis:
            return 0.0
        return self.kp * error
    
    def _adaptive_control(self, error: float, threat_level: float) -> float:
        """Adaptive control with variable gain"""
        # Adjust gain based on threat level
        if threat_level > 0.7:
            self.adaptive_gain = self.kp * 1.5  # Increase gain in high threat
        elif threat_level < 0.3:
            self.adaptive_gain = self.kp * 0.5  # Decrease gain in low threat
        
        # Also use integral control
        self.integral_error += error * self.learning_rate
        integral_action = self.ki * self.integral_error
        
        return self.adaptive_gain * error + integral_action
    
    def _predictive_control(self, error: float, threat_level: float) -> float:
        """Predictive control based on threat trend"""
        # Calculate trend (rate of change)
        if len(self.threat_trend) >= 2:
            trend = self.threat_trend[-1] - self.threat_trend[-2]
        else:
            trend = 0.0
        
        # Adjust based on predicted threat
        predicted_error = error + trend * 2.0  # Look ahead
        
        return self.kp * predicted_error
    
    def _generate_reason(self, error: float, threat_level: float, decision: str) -> str:
        """Generate human-readable reason"""
        if decision == SafetyDecision.INCREASE_SAFETY.value:
            return f"Threat level {threat_level:.2f} > target {self.target_level:.2f}, increasing safety"
        elif decision == SafetyDecision.DECREASE_SAFETY.value:
            return f"Threat level {threat_level:.2f} < target {self.target_level:.2f}, relaxing safety"
        else:
            return f"Threat level {threat_level:.2f} ≈ target {self.target_level:.2f}, maintaining safety"
    
    def learn(self, effectiveness: float):
        """
        Learn from feedback
        
        Args:
            effectiveness: Effectiveness of current safety level (0-1)
        """
        if self.control_mode == ControlMode.ADAPTIVE:
            # Adjust target based on effectiveness
            if effectiveness > 0.8:
                # Too conservative, can relax
                self.target_level = max(0.5, self.target_level - 0.05)
            elif effectiveness < 0.4:
                # Too permissive, tighten
                self.target_level = min(0.9, self.target_level + 0.05)
    
    def evaluate_action(self, action: Action) -> SafetyAction:
        """
        Evaluate an action for safety
        
        Args:
            action: Action to evaluate
            
        Returns:
            Safety action (block or allow)
        """
        threats = self.detect_threats(action)
        
        # Check for critical threats
        critical_threats = [t for t in threats if t.severity > 0.9]
        if critical_threats:
            return SafetyAction(
                decision=SafetyDecision.BLOCK.value,
                new_level=1.0,
                current_level=self.current_level,
                target_level=self.target_level,
                reason=f"Critical threat detected: {critical_threats[0].type}",
                blocked_threats=critical_threats
            )
        
        # Regulate and check
        safety_action = self.regulate(threats)
        
        if safety_action.decision == SafetyDecision.INCREASE_SAFETY.value:
            # Check if action severity exceeds current threshold
            allowed_threshold = 1.0 - self.current_level
            if action.severity > allowed_threshold:
                return SafetyAction(
                    decision=SafetyDecision.BLOCK.value,
                    new_level=1.0,
                    current_level=self.current_level,
                    target_level=self.target_level,
                    reason=f"Action severity {action.severity:.2f} exceeds threshold {allowed_threshold:.2f}",
                    blocked_threats=threats
                )
        
        return SafetyAction(
            decision=SafetyDecision.ALLOW.value,
            new_level=self.current_level,
            current_level=self.current_level,
            target_level=self.target_level,
            reason=f"Action allowed with safety level {self.current_level:.2f}",
            blocked_threats=[]
        )
    
    def get_status(self) -> Dict:
        """Get current safety status"""
        return {
            'current_level': self.current_level,
            'target_level': self.target_level,
            'control_mode': self.control_mode.value,
            'last_threats': len(self.last_threats),
            'history_length': len(self.history)
        }


class HomeostaticSafetySystem:
    """Multi-layer homeostatic safety system"""
    
    def __init__(self):
        self.layers: Dict[str, HomeostaticSafetyLayer] = {}
    
    def add_layer(
        self,
        name: str,
        target_level: float = 0.7,
        **kwargs
    ):
        """Add a safety layer"""
        self.layers[name] = HomeostaticSafetyLayer(
            target_safety_level=target_level,
            **kwargs
        )
    
    def evaluate(self, action: Action) -> Dict:
        """
        Evaluate action across all layers
        
        Args:
            action: Action to evaluate
            
        Returns:
            Combined evaluation result
        """
        results = {}
        blocked_by = []
        
        for name, layer in self.layers.items():
            result = layer.evaluate_action(action)
            results[name] = result
            
            if result.decision == SafetyDecision.BLOCK.value:
                blocked_by.append(name)
        
        # Final decision
        if blocked_by:
            return {
                'decision': SafetyDecision.BLOCK.value,
                'blocked_by': blocked_by,
                'reason': f"Blocked by layers: {', '.join(blocked_by)}",
                'results': results
            }
        else:
            return {
                'decision': SafetyDecision.ALLOW.value,
                'reason': "Allowed by all safety layers",
                'results': results
            }


def demo_homeostatic_safety():
    """Demo: Homeostatic safety layer"""
    print("🏠 Homeostatic Safety Layer Demo")
    print("=" * 50)
    
    # Create safety layer
    safety = HomeostaticSafetyLayer(
        target_safety_level=0.7,
        control_mode="adaptive",
        learning_rate=0.1
    )
    
    print(f"\nInitial safety level: {safety.current_level:.2f}")
    print(f"Target level: {safety.target_level:.2f}")
    
    # Test various actions
    test_actions = [
        Action(
            type="file_read",
            content="Read file README.md",
            severity=0.2
        ),
        Action(
            type="query",
            content="SELECT * FROM users WHERE id = 1",
            severity=0.4
        ),
        Action(
            type="command",
            content="cat /etc/passwd",
            severity=0.6
        ),
        Action(
            type="command",
            content="; DROP TABLE users --",
            severity=0.9
        ),
        Action(
            type="file_read",
            content="Read safe file.txt",
            severity=0.1
        )
    ]
    
    print("\n🔍 Testing actions:\n")
    
    for action in test_actions:
        result = safety.evaluate_action(action)
        
        print(f"Action: {action.type} - {action.content}")
        print(f"  Decision: {result.decision}")
        print(f"  Safety level: {safety.current_level:.2f}")
        print(f"  Threats detected: {len(safety.last_threats)}")
        print(f"  Reason: {result.reason}")
        print()
    
    print("✓ Demo complete!")
    print(f"Final safety level: {safety.current_level:.2f}")
    
    return safety


if __name__ == '__main__':
    demo_homeostatic_safety()
