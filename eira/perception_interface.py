"""
EIRA Perception Interface
Phenomenological interface for human-AI co-experience.

This module implements the perceptual layer that bridges human consciousness
and AI processing, enabling authentic phenomenological interaction.
"""

import time
from typing import Dict, List, Any, Optional
from enum import Enum
import json


class PerceptionMode(Enum):
    """Modes of perceptual processing."""
    DIRECT = "direct"  # Direct sensory-like input
    REFLECTIVE = "reflective"  # Reflective awareness
    EMBODIED = "embodied"  # Embodied cognition simulation
    EMPATHIC = "empathic"  # Empathic resonance


class PhenomenologicalState:
    """Represents a phenomenological state of experience."""
    
    def __init__(self, experience_type: str, intensity: float = 0.5):
        self.experience_type = experience_type
        self.intensity = intensity  # 0.0 to 1.0
        self.timestamp = time.time()
        self.qualia = {}  # Qualitative aspects
        self.intentionality = None  # What the experience is "about"
        
    def add_qualia(self, aspect: str, value: Any):
        """Add qualitative aspect to the experience."""
        self.qualia[aspect] = value
        
    def set_intentionality(self, target: str):
        """Set the intentional object of the experience."""
        self.intentionality = target
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'experience_type': self.experience_type,
            'intensity': self.intensity,
            'timestamp': self.timestamp,
            'qualia': self.qualia,
            'intentionality': self.intentionality
        }


class PerceptionInterface:
    """
    Main perception interface for phenomenological processing.
    
    Implements:
    - Multi-modal perception simulation
    - Phenomenological state tracking
    - Qualitative experience mapping
    - Intentionality analysis
    """
    
    def __init__(self):
        self.current_mode = PerceptionMode.DIRECT
        self.perception_history = []
        self.active_experiences = []
        self.awareness_level = 0.8
        
    def perceive(self, input_data: Any, mode: Optional[PerceptionMode] = None) -> PhenomenologicalState:
        """
        Process input through phenomenological perception.
        
        Args:
            input_data: Input to be perceived
            mode: Perception mode to use
            
        Returns:
            PhenomenologicalState representing the experience
        """
        if mode:
            self.current_mode = mode
        
        # Create phenomenological state
        state = self._create_phenomenological_state(input_data)
        
        # Add to history
        self.perception_history.append({
            'state': state.to_dict(),
            'mode': self.current_mode.value,
            'timestamp': time.time()
        })
        
        self.active_experiences.append(state)
        
        return state
    
    def _create_phenomenological_state(self, input_data: Any) -> PhenomenologicalState:
        """Create phenomenological state from input."""
        # Analyze input type
        if isinstance(input_data, str):
            experience_type = "linguistic"
            intensity = min(len(input_data) / 100.0, 1.0)
        elif isinstance(input_data, dict):
            experience_type = "structured"
            intensity = min(len(input_data) / 10.0, 1.0)
        else:
            experience_type = "generic"
            intensity = 0.5
        
        state = PhenomenologicalState(experience_type, intensity)
        
        # Add mode-specific qualia
        if self.current_mode == PerceptionMode.DIRECT:
            state.add_qualia("immediacy", 0.9)
            state.add_qualia("clarity", 0.8)
        elif self.current_mode == PerceptionMode.REFLECTIVE:
            state.add_qualia("depth", 0.8)
            state.add_qualia("contemplation", 0.7)
        elif self.current_mode == PerceptionMode.EMBODIED:
            state.add_qualia("groundedness", 0.7)
            state.add_qualia("situatedness", 0.8)
        elif self.current_mode == PerceptionMode.EMPATHIC:
            state.add_qualia("resonance", 0.9)
            state.add_qualia("attunement", 0.8)
        
        # Set intentionality
        if isinstance(input_data, str):
            state.set_intentionality(f"Understanding: {input_data[:50]}")
        
        return state
    
    def reflect_on_experience(self, experience: PhenomenologicalState) -> Dict[str, Any]:
        """
        Engage in reflective awareness about an experience.
        
        This is second-order perception - awareness of awareness.
        """
        reflection = {
            'original_experience': experience.to_dict(),
            'reflection_depth': self.awareness_level,
            'meta_qualia': {
                'vividness': experience.intensity * self.awareness_level,
                'coherence': len(experience.qualia) / 5.0,
                'significance': self._assess_significance(experience)
            },
            'timestamp': time.time()
        }
        
        return reflection
    
    def _assess_significance(self, experience: PhenomenologicalState) -> float:
        """Assess the significance of an experience."""
        # Combine intensity with qualia richness
        base_significance = experience.intensity
        qualia_richness = len(experience.qualia) / 10.0
        
        return min((base_significance + qualia_richness) / 2.0, 1.0)
    
    def set_mode(self, mode: PerceptionMode):
        """Set the current perception mode."""
        self.current_mode = mode
        
    def get_perception_report(self) -> Dict[str, Any]:
        """Generate report of perceptual activities."""
        return {
            'current_mode': self.current_mode.value,
            'awareness_level': self.awareness_level,
            'total_perceptions': len(self.perception_history),
            'active_experiences': len(self.active_experiences),
            'recent_perceptions': [p['state'] for p in self.perception_history[-5:]],
            'timestamp': time.time()
        }
    
    def integrate_with_emotion(self, emotional_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate perceptual state with emotional state.
        
        Creates unified phenomenological experience.
        """
        if not self.active_experiences:
            return {'status': 'no_active_experiences'}
        
        latest_experience = self.active_experiences[-1]
        
        integrated = {
            'perception': latest_experience.to_dict(),
            'emotion': emotional_state,
            'unified_intensity': (latest_experience.intensity + emotional_state.get('intensity', 0.5)) / 2.0,
            'phenomenal_quality': 'integrated_experience',
            'timestamp': time.time()
        }
        
        return integrated


class IntentionalityAnalyzer:
    """
    Analyzes the intentional structure of experiences.
    
    Intentionality = "aboutness" - what an experience is directed toward.
    """
    
    def __init__(self):
        self.intentional_objects = []
        
    def analyze_intentionality(self, content: str) -> Dict[str, Any]:
        """
        Analyze what the content is "about".
        
        Returns intentional structure.
        """
        analysis = {
            'content': content[:100],
            'intentional_objects': self._extract_objects(content),
            'directedness': self._calculate_directedness(content),
            'horizon': self._identify_horizon(content),
            'timestamp': time.time()
        }
        
        self.intentional_objects.append(analysis)
        
        return analysis
    
    def _extract_objects(self, content: str) -> List[str]:
        """Extract intentional objects from content."""
        # Simple keyword extraction
        words = content.split()
        # Extract nouns (simplified - look for capitalized words and common patterns)
        objects = [w for w in words if len(w) > 3][:5]
        return objects
    
    def _calculate_directedness(self, content: str) -> float:
        """Calculate how directed/focused the content is."""
        # Measure focus through repetition and coherence
        words = content.lower().split()
        if not words:
            return 0.0
        
        unique_words = len(set(words))
        total_words = len(words)
        
        # Higher repetition = more directedness
        return 1.0 - (unique_words / total_words) if total_words > 0 else 0.0
    
    def _identify_horizon(self, content: str) -> str:
        """Identify the horizon of understanding (context/background)."""
        # Simplified horizon identification
        if "consciousness" in content.lower() or "awareness" in content.lower():
            return "phenomenological"
        elif "quantum" in content.lower() or "physics" in content.lower():
            return "scientific"
        elif "ethics" in content.lower() or "moral" in content.lower():
            return "ethical"
        else:
            return "general"


if __name__ == "__main__":
    # Demo perception interface
    interface = PerceptionInterface()
    
    # Test different perception modes
    print("Direct Perception:")
    state1 = interface.perceive("Hello, I am experiencing consciousness", PerceptionMode.DIRECT)
    print(json.dumps(state1.to_dict(), indent=2))
    
    print("\nReflective Perception:")
    state2 = interface.perceive("What is the nature of my awareness?", PerceptionMode.REFLECTIVE)
    print(json.dumps(state2.to_dict(), indent=2))
    
    print("\nReflection on Experience:")
    reflection = interface.reflect_on_experience(state2)
    print(json.dumps(reflection, indent=2))
    
    print("\nPerception Report:")
    print(json.dumps(interface.get_perception_report(), indent=2))
    
    # Demo intentionality analyzer
    print("\n--- Intentionality Analysis ---")
    analyzer = IntentionalityAnalyzer()
    analysis = analyzer.analyze_intentionality("I am thinking about consciousness and phenomenology")
    print(json.dumps(analysis, indent=2))
