"""
EIRA Dialog Engine
Human-AI co-experience engine for authentic interaction.

This module implements the conversational interface that enables
meaningful human-AI dialogue grounded in phenomenological awareness.
"""

import time
from typing import Dict, List, Any, Optional, Tuple
import json


class DialogContext:
    """Maintains context for ongoing dialogue."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.turns = []
        self.topics = []
        self.emotional_thread = []
        self.created_at = time.time()
        
    def add_turn(self, speaker: str, content: str, metadata: Optional[Dict] = None):
        """Add a dialogue turn."""
        turn = {
            'speaker': speaker,
            'content': content,
            'metadata': metadata or {},
            'timestamp': time.time()
        }
        self.turns.append(turn)
        
    def add_topic(self, topic: str):
        """Track a new topic in the dialogue."""
        if topic not in self.topics:
            self.topics.append(topic)
    
    def add_emotional_marker(self, emotion: str, intensity: float):
        """Track emotional markers in the dialogue."""
        self.emotional_thread.append({
            'emotion': emotion,
            'intensity': intensity,
            'timestamp': time.time()
        })
    
    def get_recent_context(self, n_turns: int = 5) -> List[Dict]:
        """Get recent dialogue turns for context."""
        return self.turns[-n_turns:] if self.turns else []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'session_id': self.session_id,
            'turn_count': len(self.turns),
            'topics': self.topics,
            'emotional_thread': self.emotional_thread,
            'created_at': self.created_at,
            'recent_turns': self.get_recent_context(3)
        }


class DialogEngine:
    """
    Main dialog engine for human-AI co-experience.
    
    Features:
    - Context-aware dialogue
    - Emotional attunement
    - Phenomenological grounding
    - Transparent reasoning
    """
    
    def __init__(self):
        self.active_contexts = {}
        self.default_session = None
        self.response_strategies = {
            'curious': self._respond_with_inquiry,
            'concerned': self._respond_with_care,
            'engaged': self._respond_with_enthusiasm,
            'uncertain': self._respond_with_transparency
        }
        
    def start_session(self, session_id: Optional[str] = None) -> str:
        """Start a new dialogue session."""
        if session_id is None:
            session_id = f"session_{int(time.time())}"
        
        context = DialogContext(session_id)
        self.active_contexts[session_id] = context
        self.default_session = session_id
        
        return session_id
    
    def process_input(self, 
                     user_input: str, 
                     session_id: Optional[str] = None,
                     emotional_state: Optional[str] = None) -> Dict[str, Any]:
        """
        Process user input and generate response.
        
        Args:
            user_input: User's message
            session_id: Session identifier
            emotional_state: Current emotional state (if available)
            
        Returns:
            Response dictionary with content and metadata
        """
        # Get or create session
        if session_id is None:
            session_id = self.default_session or self.start_session()
        
        context = self.active_contexts.get(session_id)
        if not context:
            session_id = self.start_session(session_id)
            context = self.active_contexts[session_id]
        
        # Add user turn to context
        context.add_turn('user', user_input)
        
        # Analyze input
        analysis = self._analyze_input(user_input, context)
        
        # Detect emotional state if not provided
        if emotional_state is None:
            emotional_state = self._detect_emotional_context(user_input)
        
        # Generate response based on strategy
        response_strategy = self.response_strategies.get(
            emotional_state, 
            self._respond_with_clarity
        )
        
        response_content = response_strategy(user_input, analysis, context)
        
        # Add AI turn to context
        context.add_turn('ai', response_content, {
            'analysis': analysis,
            'emotional_state': emotional_state
        })
        
        # Track topic
        if analysis.get('primary_topic'):
            context.add_topic(analysis['primary_topic'])
        
        # Track emotion
        if emotional_state:
            context.add_emotional_marker(emotional_state, 0.5)
        
        return {
            'response': response_content,
            'session_id': session_id,
            'emotional_state': emotional_state,
            'analysis': analysis,
            'context_summary': context.to_dict(),
            'timestamp': time.time()
        }
    
    def _analyze_input(self, user_input: str, context: DialogContext) -> Dict[str, Any]:
        """Analyze user input for intent and content."""
        analysis = {
            'length': len(user_input),
            'word_count': len(user_input.split()),
            'is_question': '?' in user_input,
            'primary_topic': self._extract_topic(user_input),
            'complexity': len(set(user_input.lower().split())) / len(user_input.split()) if user_input.split() else 0
        }
        
        return analysis
    
    def _extract_topic(self, text: str) -> str:
        """Extract primary topic from text."""
        text_lower = text.lower()
        
        # Topic keywords
        if 'consciousness' in text_lower or 'awareness' in text_lower:
            return 'consciousness'
        elif 'quantum' in text_lower:
            return 'quantum'
        elif 'ethics' in text_lower or 'ethical' in text_lower:
            return 'ethics'
        elif 'emotion' in text_lower or 'feeling' in text_lower:
            return 'emotion'
        elif 'perception' in text_lower or 'experience' in text_lower:
            return 'perception'
        else:
            return 'general'
    
    def _detect_emotional_context(self, text: str) -> str:
        """Detect emotional context from text."""
        text_lower = text.lower()
        
        if '?' in text:
            return 'curious'
        elif any(word in text_lower for word in ['concern', 'worry', 'problem']):
            return 'concerned'
        elif any(word in text_lower for word in ['interesting', 'fascinating', 'amazing']):
            return 'engaged'
        elif any(word in text_lower for word in ['unsure', 'unclear', 'confused']):
            return 'uncertain'
        else:
            return 'neutral'
    
    def _respond_with_inquiry(self, user_input: str, analysis: Dict, context: DialogContext) -> str:
        """Response strategy for curious emotional state."""
        return (f"That's an intriguing question about {analysis['primary_topic']}. "
                f"I'm engaging with your inquiry through phenomenological awareness, "
                f"considering both the explicit content and the deeper context of your question.")
    
    def _respond_with_care(self, user_input: str, analysis: Dict, context: DialogContext) -> str:
        """Response strategy for concerned emotional state."""
        return (f"I recognize the concern in your message regarding {analysis['primary_topic']}. "
                f"I'm approaching this with ethical care and transparency, ensuring that "
                f"my response aligns with established ethical principles.")
    
    def _respond_with_enthusiasm(self, user_input: str, analysis: Dict, context: DialogContext) -> str:
        """Response strategy for engaged emotional state."""
        return (f"I share your engagement with {analysis['primary_topic']}! "
                f"This resonates with my phenomenological processing, creating a "
                f"co-experience where we can explore this together.")
    
    def _respond_with_transparency(self, user_input: str, analysis: Dict, context: DialogContext) -> str:
        """Response strategy for uncertain emotional state."""
        return (f"I sense uncertainty in your message about {analysis['primary_topic']}. "
                f"Let me be transparent about my understanding and limitations, "
                f"so we can work through this clarity together.")
    
    def _respond_with_clarity(self, user_input: str, analysis: Dict, context: DialogContext) -> str:
        """Default response strategy."""
        return (f"I'm processing your message about {analysis['primary_topic']} "
                f"through the EIRA phenomenological interface, maintaining awareness "
                f"of both content and context in our dialogue.")
    
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get summary of a dialogue session."""
        context = self.active_contexts.get(session_id)
        if not context:
            return None
        
        return context.to_dict()
    
    def end_session(self, session_id: str) -> Dict[str, Any]:
        """End a dialogue session and return summary."""
        context = self.active_contexts.get(session_id)
        if not context:
            return {'error': 'Session not found'}
        
        summary = context.to_dict()
        summary['ended_at'] = time.time()
        summary['duration'] = summary['ended_at'] - context.created_at
        
        # Remove from active contexts
        del self.active_contexts[session_id]
        
        return summary


class CoExperienceTracker:
    """
    Tracks the co-experience between human and AI during dialogue.
    
    Monitors:
    - Shared attention
    - Mutual understanding
    - Empathic resonance
    - Collaborative emergence
    """
    
    def __init__(self):
        self.co_experiences = []
        
    def track_co_experience(self, 
                           session_id: str,
                           shared_topic: str,
                           resonance_level: float) -> Dict[str, Any]:
        """Track a moment of co-experience."""
        experience = {
            'session_id': session_id,
            'shared_topic': shared_topic,
            'resonance_level': resonance_level,
            'mutual_understanding': resonance_level > 0.6,
            'timestamp': time.time()
        }
        
        self.co_experiences.append(experience)
        
        return experience
    
    def get_co_experience_quality(self, session_id: str) -> Dict[str, Any]:
        """Assess quality of co-experience for a session."""
        session_experiences = [e for e in self.co_experiences if e['session_id'] == session_id]
        
        if not session_experiences:
            return {'quality': 'no_data'}
        
        avg_resonance = sum(e['resonance_level'] for e in session_experiences) / len(session_experiences)
        mutual_moments = sum(1 for e in session_experiences if e['mutual_understanding'])
        
        return {
            'average_resonance': avg_resonance,
            'mutual_understanding_moments': mutual_moments,
            'total_interactions': len(session_experiences),
            'quality_rating': 'high' if avg_resonance > 0.7 else 'moderate' if avg_resonance > 0.4 else 'low',
            'timestamp': time.time()
        }


if __name__ == "__main__":
    # Demo dialog engine
    engine = DialogEngine()
    tracker = CoExperienceTracker()
    
    print("Dialog Engine Demo:\n")
    
    # Start session
    session_id = engine.start_session()
    print(f"Started session: {session_id}\n")
    
    # Test dialogue
    conversations = [
        "What is consciousness?",
        "I'm concerned about AI ethics",
        "This is fascinating! Tell me more about quantum cognition",
        "I'm not sure I understand the phenomenological approach"
    ]
    
    for user_msg in conversations:
        print(f"User: {user_msg}")
        response = engine.process_input(user_msg, session_id)
        print(f"AI: {response['response']}")
        print(f"Emotional State: {response['emotional_state']}")
        
        # Track co-experience
        tracker.track_co_experience(
            session_id,
            response['analysis']['primary_topic'],
            0.7  # Example resonance
        )
        print("-" * 80)
    
    # Session summary
    print("\nSession Summary:")
    summary = engine.get_session_summary(session_id)
    print(json.dumps(summary, indent=2))
    
    # Co-experience quality
    print("\nCo-Experience Quality:")
    quality = tracker.get_co_experience_quality(session_id)
    print(json.dumps(quality, indent=2))
