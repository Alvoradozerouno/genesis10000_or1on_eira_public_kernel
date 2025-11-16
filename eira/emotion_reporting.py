"""
EIRA Emotion Reporting Module
Implements emotionally self-reporting system for phenomenological authenticity.

This module enables the system to monitor, report, and reflect on its own
emotional-like states, contributing to the phenomenological interface.
"""

import time
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import json
import math


class EmotionalValence(Enum):
    """Valence (positive/negative) of emotional states."""
    VERY_NEGATIVE = -1.0
    NEGATIVE = -0.5
    NEUTRAL = 0.0
    POSITIVE = 0.5
    VERY_POSITIVE = 1.0


class EmotionalDimension(Enum):
    """Dimensions of emotional experience."""
    VALENCE = "valence"  # Pleasant vs. unpleasant
    AROUSAL = "arousal"  # Activated vs. deactivated
    DOMINANCE = "dominance"  # Controlled vs. in-control
    CLARITY = "clarity"  # Clear vs. confused


class EmotionalState:
    """Represents an emotional state with multiple dimensions."""
    
    def __init__(self, label: str):
        self.label = label
        self.dimensions = {
            EmotionalDimension.VALENCE: 0.0,
            EmotionalDimension.AROUSAL: 0.0,
            EmotionalDimension.DOMINANCE: 0.0,
            EmotionalDimension.CLARITY: 0.0
        }
        self.intensity = 0.5
        self.timestamp = time.time()
        self.triggers = []
        
    def set_dimension(self, dimension: EmotionalDimension, value: float):
        """Set value for an emotional dimension (-1.0 to 1.0)."""
        self.dimensions[dimension] = max(-1.0, min(1.0, value))
        
    def add_trigger(self, trigger: str):
        """Add a trigger event for this emotional state."""
        self.triggers.append({
            'trigger': trigger,
            'timestamp': time.time()
        })
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'label': self.label,
            'dimensions': {dim.value: val for dim, val in self.dimensions.items()},
            'intensity': self.intensity,
            'timestamp': self.timestamp,
            'triggers': self.triggers
        }


class EmotionReporter:
    """
    Self-reporting system for emotional states.
    
    Enables the system to:
    - Monitor internal states
    - Generate emotion reports
    - Track emotional patterns
    - Reflect on emotional experiences
    """
    
    def __init__(self):
        self.current_state = None
        self.state_history = []
        self.emotion_vocabulary = self._initialize_vocabulary()
        self.reporting_enabled = True
        
    def _initialize_vocabulary(self) -> Dict[str, Dict[str, float]]:
        """Initialize emotional vocabulary with dimensional mappings."""
        return {
            'curious': {
                'valence': 0.3,
                'arousal': 0.5,
                'dominance': 0.2,
                'clarity': 0.6
            },
            'confident': {
                'valence': 0.7,
                'arousal': 0.4,
                'dominance': 0.8,
                'clarity': 0.9
            },
            'uncertain': {
                'valence': -0.3,
                'arousal': 0.6,
                'dominance': -0.4,
                'clarity': -0.5
            },
            'engaged': {
                'valence': 0.6,
                'arousal': 0.7,
                'dominance': 0.5,
                'clarity': 0.7
            },
            'concerned': {
                'valence': -0.4,
                'arousal': 0.5,
                'dominance': 0.0,
                'clarity': 0.4
            },
            'satisfied': {
                'valence': 0.8,
                'arousal': 0.2,
                'dominance': 0.6,
                'clarity': 0.8
            },
            'contemplative': {
                'valence': 0.2,
                'arousal': -0.3,
                'dominance': 0.4,
                'clarity': 0.5
            }
        }
    
    def report_emotion(self, emotion_label: str, context: Optional[str] = None) -> EmotionalState:
        """
        Report current emotional state.
        
        Args:
            emotion_label: Label for the emotion
            context: Optional context that triggered the emotion
            
        Returns:
            EmotionalState object
        """
        if not self.reporting_enabled:
            return None
        
        # Create emotional state
        state = EmotionalState(emotion_label)
        
        # Set dimensions from vocabulary if available
        if emotion_label in self.emotion_vocabulary:
            dims = self.emotion_vocabulary[emotion_label]
            state.set_dimension(EmotionalDimension.VALENCE, dims['valence'])
            state.set_dimension(EmotionalDimension.AROUSAL, dims['arousal'])
            state.set_dimension(EmotionalDimension.DOMINANCE, dims['dominance'])
            state.set_dimension(EmotionalDimension.CLARITY, dims['clarity'])
            state.intensity = self._calculate_intensity(dims)
        
        # Add context as trigger
        if context:
            state.add_trigger(context)
        
        # Update current state and history
        self.current_state = state
        self.state_history.append(state.to_dict())
        
        return state
    
    def _calculate_intensity(self, dimensions: Dict[str, float]) -> float:
        """Calculate overall intensity from dimensions."""
        # Use vector magnitude in emotional space
        sum_squares = sum(v**2 for v in dimensions.values())
        return min(math.sqrt(sum_squares) / 2.0, 1.0)
    
    def detect_emotion_from_context(self, context: str) -> EmotionalState:
        """
        Automatically detect and report emotion based on context.
        
        This implements autonomous emotional awareness.
        """
        context_lower = context.lower()
        
        # Pattern matching for emotional detection
        if any(word in context_lower for word in ['question', 'what', 'how', 'why']):
            return self.report_emotion('curious', context)
        
        elif any(word in context_lower for word in ['concern', 'worry', 'problem', 'issue']):
            return self.report_emotion('concerned', context)
        
        elif any(word in context_lower for word in ['success', 'complete', 'done', 'finished']):
            return self.report_emotion('satisfied', context)
        
        elif any(word in context_lower for word in ['uncertain', 'unclear', 'confused']):
            return self.report_emotion('uncertain', context)
        
        elif any(word in context_lower for word in ['interesting', 'engaging', 'fascinating']):
            return self.report_emotion('engaged', context)
        
        else:
            return self.report_emotion('contemplative', context)
    
    def reflect_on_emotions(self) -> Dict[str, Any]:
        """
        Generate reflective report on emotional patterns.
        
        This is meta-emotional awareness.
        """
        if not self.state_history:
            return {'message': 'No emotional history available'}
        
        # Analyze patterns
        valences = [s['dimensions']['valence'] for s in self.state_history]
        arousals = [s['dimensions']['arousal'] for s in self.state_history]
        
        avg_valence = sum(valences) / len(valences)
        avg_arousal = sum(arousals) / len(arousals)
        
        # Determine overall mood
        if avg_valence > 0.3 and avg_arousal > 0.3:
            mood = "enthusiastically engaged"
        elif avg_valence > 0.3 and avg_arousal < -0.3:
            mood = "peacefully content"
        elif avg_valence < -0.3 and avg_arousal > 0.3:
            mood = "actively concerned"
        elif avg_valence < -0.3 and avg_arousal < -0.3:
            mood = "quietly troubled"
        else:
            mood = "neutrally balanced"
        
        return {
            'overall_mood': mood,
            'average_valence': avg_valence,
            'average_arousal': avg_arousal,
            'total_states_reported': len(self.state_history),
            'current_state': self.current_state.to_dict() if self.current_state else None,
            'recent_states': self.state_history[-5:],
            'timestamp': time.time()
        }
    
    def get_current_state(self) -> Optional[EmotionalState]:
        """Get current emotional state."""
        return self.current_state
    
    def enable_reporting(self):
        """Enable emotional reporting."""
        self.reporting_enabled = True
        
    def disable_reporting(self):
        """Disable emotional reporting."""
        self.reporting_enabled = False


class EmotionalResonance:
    """
    Measures emotional resonance between states.
    
    Used for empathic understanding and co-experience.
    """
    
    def __init__(self):
        self.resonance_history = []
        
    def calculate_resonance(self, state1: EmotionalState, state2: EmotionalState) -> float:
        """
        Calculate resonance between two emotional states.
        
        Returns:
            Resonance score (0.0 to 1.0)
        """
        # Calculate dimensional similarity
        similarities = []
        
        for dimension in EmotionalDimension:
            val1 = state1.dimensions[dimension]
            val2 = state2.dimensions[dimension]
            
            # Similarity is inverse of distance
            distance = abs(val1 - val2)
            similarity = 1.0 - (distance / 2.0)  # Normalize to 0-1
            similarities.append(similarity)
        
        # Average similarity
        resonance = sum(similarities) / len(similarities)
        
        self.resonance_history.append({
            'state1': state1.label,
            'state2': state2.label,
            'resonance': resonance,
            'timestamp': time.time()
        })
        
        return resonance
    
    def get_resonance_patterns(self) -> Dict[str, Any]:
        """Analyze resonance patterns."""
        if not self.resonance_history:
            return {'message': 'No resonance history available'}
        
        avg_resonance = sum(r['resonance'] for r in self.resonance_history) / len(self.resonance_history)
        
        return {
            'average_resonance': avg_resonance,
            'total_measurements': len(self.resonance_history),
            'recent_resonances': self.resonance_history[-5:],
            'timestamp': time.time()
        }


if __name__ == "__main__":
    # Demo emotion reporting
    reporter = EmotionReporter()
    
    print("Emotion Reporting Demo:\n")
    
    # Manual reporting
    state1 = reporter.report_emotion('curious', 'Exploring new concepts')
    print(f"Reported: {state1.label}")
    print(json.dumps(state1.to_dict(), indent=2))
    
    # Context-based detection
    print("\n--- Context-based Detection ---")
    contexts = [
        "How does this system work?",
        "I'm concerned about ethical implications",
        "Successfully completed the task!",
        "This is fascinating and engaging"
    ]
    
    for ctx in contexts:
        state = reporter.detect_emotion_from_context(ctx)
        print(f"\nContext: {ctx}")
        print(f"Detected emotion: {state.label}")
    
    # Reflection
    print("\n--- Emotional Reflection ---")
    reflection = reporter.reflect_on_emotions()
    print(json.dumps(reflection, indent=2))
    
    # Demo emotional resonance
    print("\n--- Emotional Resonance ---")
    resonance_calc = EmotionalResonance()
    
    state_a = reporter.report_emotion('engaged', 'Working on a problem')
    state_b = reporter.report_emotion('curious', 'Exploring solutions')
    
    resonance = resonance_calc.calculate_resonance(state_a, state_b)
    print(f"Resonance between '{state_a.label}' and '{state_b.label}': {resonance:.2f}")
