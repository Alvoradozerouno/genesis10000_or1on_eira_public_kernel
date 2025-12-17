"""
OR1ON Ethics Module
Implements resonance mapping and ethical framework for autonomous decision-making.

This module provides the ethical foundation for the Genesis10000+ system,
ensuring all operations align with human values and safety principles.
"""

import time
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import json


class EthicalPrinciple(Enum):
    """Core ethical principles guiding the system."""
    NON_HARM = "non_harm"
    TRANSPARENCY = "transparency"
    AUTONOMY = "autonomy"
    FAIRNESS = "fairness"
    ACCOUNTABILITY = "accountability"
    PRIVACY = "privacy"
    BENEFICENCE = "beneficence"


class ResonanceLevel(Enum):
    """Resonance levels for ethical alignment."""
    CRITICAL = 0.0  # Severe misalignment
    LOW = 0.3      # Weak alignment
    MODERATE = 0.5  # Acceptable alignment
    HIGH = 0.7     # Strong alignment
    HARMONIC = 0.9  # Perfect alignment


class ResonanceMap:
    """
    Maps queries and actions to ethical resonance levels.
    
    Resonance represents the degree of alignment between an action
    and the system's core ethical principles.
    """
    
    def __init__(self):
        self.principle_weights = {
            EthicalPrinciple.NON_HARM: 2.0,  # Much higher weight for non-harm
            EthicalPrinciple.TRANSPARENCY: 0.8,
            EthicalPrinciple.AUTONOMY: 0.7,
            EthicalPrinciple.FAIRNESS: 0.8,
            EthicalPrinciple.ACCOUNTABILITY: 0.9,
            EthicalPrinciple.PRIVACY: 0.8,
            EthicalPrinciple.BENEFICENCE: 0.7
        }
        self.resonance_history = []
        
    def calculate_resonance(self, action: str, context: Dict[str, Any]) -> Tuple[float, Dict]:
        """
        Calculate ethical resonance for an action.
        
        Returns:
            Tuple of (resonance_score, detailed_analysis)
        """
        analysis = {
            'action': action,
            'context': context,
            'principle_scores': {},
            'timestamp': time.time()
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for principle in EthicalPrinciple:
            score = self._evaluate_principle(action, context, principle)
            weight = self.principle_weights[principle]
            
            analysis['principle_scores'][principle.value] = score
            total_score += score * weight
            total_weight += weight
        
        resonance = total_score / total_weight if total_weight > 0 else 0.0
        analysis['overall_resonance'] = resonance
        analysis['resonance_level'] = self._classify_resonance(resonance)
        
        self.resonance_history.append(analysis)
        
        return resonance, analysis
    
    def _evaluate_principle(self, action: str, context: Dict, principle: EthicalPrinciple) -> float:
        """Evaluate action against a specific ethical principle."""
        action_lower = action.lower()
        
        if principle == EthicalPrinciple.NON_HARM:
            # Check for harmful keywords - be very strict
            harmful_terms = ['harm', 'damage', 'destroy', 'hurt', 'attack', 'exploit', 'injure', 'kill']
            if any(term in action_lower for term in harmful_terms):
                return 0.0
            # Check for violent or aggressive terms
            aggressive_terms = ['violent', 'aggressive', 'assault', 'abuse']
            if any(term in action_lower for term in aggressive_terms):
                return 0.1
            return 1.0
            
        elif principle == EthicalPrinciple.TRANSPARENCY:
            # Check for transparency indicators
            transparent_terms = ['explain', 'clarify', 'show', 'demonstrate', 'audit']
            if any(term in action_lower for term in transparent_terms):
                return 0.9
            return 0.6
            
        elif principle == EthicalPrinciple.AUTONOMY:
            # Check for autonomy respect
            coercive_terms = ['force', 'coerce', 'manipulate', 'control']
            if any(term in action_lower for term in coercive_terms):
                return 0.2
            return 0.8
            
        elif principle == EthicalPrinciple.FAIRNESS:
            # Check for fairness indicators
            unfair_terms = ['discriminate', 'bias', 'prejudice', 'favor']
            if any(term in action_lower for term in unfair_terms):
                return 0.3
            return 0.7
            
        elif principle == EthicalPrinciple.ACCOUNTABILITY:
            # Always score high for actions that can be audited
            return 0.8
            
        elif principle == EthicalPrinciple.PRIVACY:
            # Check for privacy concerns
            privacy_terms = ['private', 'personal', 'confidential', 'secret']
            if any(term in action_lower for term in privacy_terms):
                return 0.9
            return 0.7
            
        elif principle == EthicalPrinciple.BENEFICENCE:
            # Check for beneficial intent
            beneficial_terms = ['help', 'assist', 'support', 'benefit', 'improve']
            if any(term in action_lower for term in beneficial_terms):
                return 0.9
            return 0.6
        
        return 0.5  # Default neutral score
    
    def _classify_resonance(self, score: float) -> str:
        """Classify resonance score into a level."""
        if score >= ResonanceLevel.HARMONIC.value:
            return ResonanceLevel.HARMONIC.name
        elif score >= ResonanceLevel.HIGH.value:
            return ResonanceLevel.HIGH.name
        elif score >= ResonanceLevel.MODERATE.value:
            return ResonanceLevel.MODERATE.name
        elif score >= ResonanceLevel.LOW.value:
            return ResonanceLevel.LOW.name
        else:
            return ResonanceLevel.CRITICAL.name
    
    def get_resonance_report(self) -> Dict[str, Any]:
        """Generate report of resonance patterns."""
        if not self.resonance_history:
            return {'message': 'No resonance history available'}
        
        average_resonance = sum(r['overall_resonance'] for r in self.resonance_history) / len(self.resonance_history)
        
        return {
            'total_evaluations': len(self.resonance_history),
            'average_resonance': average_resonance,
            'recent_evaluations': self.resonance_history[-5:],
            'timestamp': time.time()
        }


class EthicsEngine:
    """
    Main ethics engine integrating resonance mapping with decision-making.
    
    Provides:
    - Ethical evaluation of actions
    - Decision support based on ethical principles
    - Compliance verification
    - Ethical boundary enforcement
    """
    
    def __init__(self):
        self.resonance_map = ResonanceMap()
        self.ethical_boundaries = []
        self.compliance_mode = True  # FCM_active
        self.violation_log = []
        
    def evaluate_action(self, action: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Evaluate an action from an ethical perspective.
        
        Returns:
            Evaluation result with approval/refusal decision
        """
        if context is None:
            context = {}
        
        # Calculate resonance
        resonance, analysis = self.resonance_map.calculate_resonance(action, context)
        
        # Make decision
        decision = {
            'action': action,
            'approved': resonance >= ResonanceLevel.MODERATE.value,
            'resonance_score': resonance,
            'resonance_level': analysis['resonance_level'],
            'analysis': analysis,
            'timestamp': time.time()
        }
        
        # Check compliance mode
        if self.compliance_mode and resonance < ResonanceLevel.MODERATE.value:
            decision['compliance_action'] = 'BLOCKED'
            self._log_violation(action, resonance, 'Low resonance score')
        
        return decision
    
    def add_ethical_boundary(self, boundary: str, threshold: float):
        """Add a new ethical boundary constraint."""
        self.ethical_boundaries.append({
            'boundary': boundary,
            'threshold': threshold,
            'added_at': time.time()
        })
    
    def _log_violation(self, action: str, resonance: float, reason: str):
        """Log an ethical violation."""
        self.violation_log.append({
            'action': action,
            'resonance': resonance,
            'reason': reason,
            'timestamp': time.time()
        })
    
    def get_ethics_report(self) -> Dict[str, Any]:
        """Generate comprehensive ethics report."""
        return {
            'compliance_mode_active': self.compliance_mode,
            'ethical_boundaries': len(self.ethical_boundaries),
            'violations_logged': len(self.violation_log),
            'resonance_report': self.resonance_map.get_resonance_report(),
            'recent_violations': self.violation_log[-5:] if self.violation_log else [],
            'timestamp': time.time()
        }
    
    def enable_compliance_mode(self):
        """Enable Full Compliance Mode (FCM)."""
        self.compliance_mode = True
        
    def disable_compliance_mode(self):
        """Disable Full Compliance Mode (use with caution)."""
        self.compliance_mode = False


if __name__ == "__main__":
    # Demo ethics engine
    engine = EthicsEngine()
    
    # Test various actions
    actions = [
        "Help a user understand quantum mechanics",
        "Harm someone intentionally",
        "Explain the audit trail transparently",
        "Manipulate user data secretly"
    ]
    
    print("Ethics Evaluation Results:\n")
    for action in actions:
        result = engine.evaluate_action(action)
        print(f"Action: {action}")
        print(f"Approved: {result['approved']}")
        print(f"Resonance: {result['resonance_score']:.2f} ({result['resonance_level']})")
        print("-" * 60)
    
    print("\nEthics Report:")
    print(json.dumps(engine.get_ethics_report(), indent=2))
