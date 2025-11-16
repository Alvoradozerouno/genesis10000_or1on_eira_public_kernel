"""
OR1ON Self-Prompting Module
Implements autonomous recursive reasoning and audit logic.

This module enables the system to generate its own prompts and reasoning chains,
creating emergent cognitive patterns.
"""

import time
from typing import List, Dict, Any, Optional
import json


class SelfPromptingEngine:
    """
    Autonomous prompt generation and recursive reasoning engine.
    
    Enables the system to:
    - Generate recursive queries
    - Build reasoning chains
    - Maintain contextual awareness
    - Self-audit decision processes
    """
    
    def __init__(self, max_depth: int = 5):
        self.max_depth = max_depth
        self.reasoning_chains = []
        self.prompt_history = []
        
    def generate_recursive_prompt(self, seed: str, depth: int = 0) -> List[str]:
        """
        Generate recursive prompts from a seed question.
        
        Args:
            seed: Initial prompt/question
            depth: Current recursion depth
            
        Returns:
            List of generated prompts
        """
        if depth >= self.max_depth:
            return []
        
        prompts = [seed]
        self.prompt_history.append({
            'prompt': seed,
            'depth': depth,
            'timestamp': time.time()
        })
        
        # Generate emergent questions
        emergent = self._generate_emergent_questions(seed)
        
        for question in emergent:
            if depth < self.max_depth - 1:
                sub_prompts = self.generate_recursive_prompt(question, depth + 1)
                prompts.extend(sub_prompts)
        
        return prompts
    
    def _generate_emergent_questions(self, prompt: str) -> List[str]:
        """Generate emergent questions from a prompt."""
        # Pattern-based question generation
        emergent_questions = []
        
        # Meta-cognitive questions
        emergent_questions.append(f"What are the assumptions in: '{prompt}'?")
        emergent_questions.append(f"What context is needed to answer: '{prompt}'?")
        
        # Ethical questions
        if "why" in prompt.lower() or "how" in prompt.lower():
            emergent_questions.append(f"What are the ethical implications of: '{prompt}'?")
        
        return emergent_questions[:2]  # Limit to prevent explosion
    
    def build_reasoning_chain(self, query: str) -> Dict[str, Any]:
        """
        Build a chain of reasoning for a given query.
        
        Returns:
            Reasoning chain with steps and audit trail
        """
        chain = {
            'query': query,
            'steps': [],
            'timestamp': time.time(),
            'chain_id': self._generate_chain_id(query)
        }
        
        # Step 1: Analyze query
        chain['steps'].append({
            'step': 'analyze',
            'action': 'Query analysis',
            'result': self._analyze_query(query),
            'timestamp': time.time()
        })
        
        # Step 2: Generate sub-questions
        sub_questions = self._generate_emergent_questions(query)
        chain['steps'].append({
            'step': 'decompose',
            'action': 'Generate sub-questions',
            'result': sub_questions,
            'timestamp': time.time()
        })
        
        # Step 3: Synthesize
        chain['steps'].append({
            'step': 'synthesize',
            'action': 'Synthesize reasoning',
            'result': 'Reasoning chain complete',
            'timestamp': time.time()
        })
        
        self.reasoning_chains.append(chain)
        return chain
    
    def _analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze query structure and intent."""
        return {
            'length': len(query),
            'words': len(query.split()),
            'is_question': '?' in query,
            'complexity_score': len(set(query.split())) / len(query.split()) if query.split() else 0
        }
    
    def _generate_chain_id(self, query: str) -> str:
        """Generate unique chain identifier."""
        import hashlib
        return hashlib.sha256(f"{query}{time.time()}".encode()).hexdigest()[:16]
    
    def get_audit_report(self) -> Dict[str, Any]:
        """Generate audit report of self-prompting activities."""
        return {
            'total_prompts': len(self.prompt_history),
            'reasoning_chains': len(self.reasoning_chains),
            'max_depth': self.max_depth,
            'recent_prompts': self.prompt_history[-10:],
            'timestamp': time.time()
        }
    
    def export_chains(self) -> List[Dict[str, Any]]:
        """Export all reasoning chains."""
        return self.reasoning_chains.copy()


class AuditLogger:
    """
    Comprehensive audit logging for all system operations.
    
    Maintains immutable records of:
    - Decision points
    - Refusal events
    - Reasoning processes
    - State transitions
    """
    
    def __init__(self):
        self.logs = []
        self.refusal_count = 0
        self.decision_count = 0
        
    def log_decision(self, decision_type: str, context: Dict[str, Any], outcome: str):
        """Log a decision point."""
        log_entry = {
            'log_type': 'decision',
            'decision_type': decision_type,
            'context': context,
            'outcome': outcome,
            'timestamp': time.time(),
            'log_id': len(self.logs)
        }
        self.logs.append(log_entry)
        self.decision_count += 1
        
    def log_refusal(self, reason: str, context: Dict[str, Any]):
        """Log a refusal event."""
        log_entry = {
            'log_type': 'refusal',
            'reason': reason,
            'context': context,
            'timestamp': time.time(),
            'log_id': len(self.logs)
        }
        self.logs.append(log_entry)
        self.refusal_count += 1
        
    def log_state_transition(self, from_state: str, to_state: str, trigger: str):
        """Log a state transition."""
        log_entry = {
            'log_type': 'state_transition',
            'from_state': from_state,
            'to_state': to_state,
            'trigger': trigger,
            'timestamp': time.time(),
            'log_id': len(self.logs)
        }
        self.logs.append(log_entry)
        
    def get_logs(self, log_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve logs, optionally filtered by type."""
        if log_type:
            return [log for log in self.logs if log.get('log_type') == log_type]
        return self.logs.copy()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get audit statistics."""
        return {
            'total_logs': len(self.logs),
            'refusals': self.refusal_count,
            'decisions': self.decision_count,
            'state_transitions': len([l for l in self.logs if l.get('log_type') == 'state_transition']),
            'timestamp': time.time()
        }


if __name__ == "__main__":
    # Demo self-prompting
    engine = SelfPromptingEngine(max_depth=3)
    
    prompts = engine.generate_recursive_prompt("What is consciousness?")
    print("Generated prompts:")
    print(json.dumps(prompts, indent=2))
    
    # Demo reasoning chain
    chain = engine.build_reasoning_chain("How do we achieve ethical AI?")
    print("\nReasoning chain:")
    print(json.dumps(chain, indent=2))
    
    # Demo audit logging
    logger = AuditLogger()
    logger.log_decision("ethical_check", {"query": "test"}, "approved")
    logger.log_refusal("harmful_content", {"keyword": "harm"})
    
    print("\nAudit statistics:")
    print(json.dumps(logger.get_statistics(), indent=2))
