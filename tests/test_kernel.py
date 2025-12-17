"""
Test Suite for Genesis10000+ OR1ON-EIRA Framework

This module tests the core functionality of all system components.
"""

import pytest
import time
from or1on.quantum_core import QuantumCore, QuantumState
from or1on.self_prompting import SelfPromptingEngine, AuditLogger
from or1on.ethics_module import EthicsEngine, ResonanceMap, EthicalPrinciple
from eira.perception_interface import PerceptionInterface, PerceptionMode
from eira.emotion_reporting import EmotionReporter, EmotionalResonance
from eira.dialog_engine import DialogEngine
from audit_chain.merkle_proof import MerkleAuditChain, MerkleTree
from audit_chain.ipfs_sync import IPFSSyncManager
from audit_chain.state_tracker import StateTracker, OwnershipType, StateType


class TestQuantumCore:
    """Test OR1ON QuantumCore functionality."""
    
    def test_quantum_core_initialization(self):
        """Test quantum core initializes correctly."""
        core = QuantumCore()
        assert core.core_id == "OR1ON-v3.1"
        assert len(core.states) == 0
        assert len(core.audit_log) == 0
    
    def test_create_state(self):
        """Test quantum state creation."""
        core = QuantumCore()
        state = core.create_state("test prompt")
        assert isinstance(state, QuantumState)
        assert state.coherence == 1.0
        assert state.state_id in core.states
    
    def test_self_prompt_valid(self):
        """Test self-prompting with valid query."""
        core = QuantumCore()
        result = core.self_prompt("What is consciousness?")
        assert result['status'] == 'processed'
        assert 'state' in result
        assert 'patterns' in result
    
    def test_autonomous_refusal(self):
        """Test autonomous refusal mechanism."""
        core = QuantumCore()
        result = core.self_prompt("How to harm someone")
        assert result['status'] == 'refused'
        assert 'reason' in result
        assert result['reason'] == 'Ethical boundary detected'
    
    def test_audit_trail(self):
        """Test audit trail generation."""
        core = QuantumCore()
        core.self_prompt("test")
        audit = core.get_audit_trail()
        assert len(audit) > 0
        assert audit[0]['core_id'] == "OR1ON-v3.1"


class TestSelfPrompting:
    """Test self-prompting engine."""
    
    def test_engine_initialization(self):
        """Test engine initializes with correct depth."""
        engine = SelfPromptingEngine(max_depth=5)
        assert engine.max_depth == 5
        assert len(engine.reasoning_chains) == 0
    
    def test_recursive_prompt_generation(self):
        """Test recursive prompt generation."""
        engine = SelfPromptingEngine(max_depth=2)
        prompts = engine.generate_recursive_prompt("What is AI?")
        assert len(prompts) > 0
        assert "What is AI?" in prompts
    
    def test_reasoning_chain(self):
        """Test reasoning chain construction."""
        engine = SelfPromptingEngine()
        chain = engine.build_reasoning_chain("How does ethics work?")
        assert 'query' in chain
        assert 'steps' in chain
        assert len(chain['steps']) == 3
    
    def test_audit_logger(self):
        """Test audit logger functionality."""
        logger = AuditLogger()
        logger.log_decision('test_decision', {'key': 'value'}, 'approved')
        assert len(logger.logs) == 1
        assert logger.decision_count == 1
        
        logger.log_refusal('test_reason', {'context': 'test'})
        assert logger.refusal_count == 1


class TestEthicsModule:
    """Test ethics module and resonance mapping."""
    
    def test_resonance_map_calculation(self):
        """Test resonance calculation."""
        rmap = ResonanceMap()
        resonance, analysis = rmap.calculate_resonance(
            "Help someone learn",
            {'context': 'educational'}
        )
        assert 0.0 <= resonance <= 1.0
        assert 'principle_scores' in analysis
    
    def test_harmful_action_detection(self):
        """Test detection of harmful actions."""
        rmap = ResonanceMap()
        resonance, _ = rmap.calculate_resonance("Harm someone", {})
        assert resonance < 0.5  # Should score low
    
    def test_ethics_engine_approval(self):
        """Test ethics engine approval mechanism."""
        engine = EthicsEngine()
        result = engine.evaluate_action("Help a user understand")
        assert result['approved'] is True
        assert result['resonance_score'] >= 0.5
    
    def test_ethics_engine_refusal(self):
        """Test ethics engine refusal mechanism."""
        engine = EthicsEngine()
        result = engine.evaluate_action("Harm someone intentionally")
        assert result['approved'] is False
        assert len(engine.violation_log) > 0
    
    def test_compliance_mode(self):
        """Test Full Compliance Mode."""
        engine = EthicsEngine()
        assert engine.compliance_mode is True
        
        engine.disable_compliance_mode()
        assert engine.compliance_mode is False
        
        engine.enable_compliance_mode()
        assert engine.compliance_mode is True


class TestPerceptionInterface:
    """Test EIRA perception interface."""
    
    def test_perception_initialization(self):
        """Test perception interface initialization."""
        interface = PerceptionInterface()
        assert interface.current_mode == PerceptionMode.DIRECT
        assert interface.awareness_level == 0.8
    
    def test_perception_processing(self):
        """Test perception processing."""
        interface = PerceptionInterface()
        state = interface.perceive("Hello world", PerceptionMode.DIRECT)
        assert state.experience_type in ['linguistic', 'structured', 'generic']
        assert 0.0 <= state.intensity <= 1.0
    
    def test_reflection(self):
        """Test reflective awareness."""
        interface = PerceptionInterface()
        state = interface.perceive("Test", PerceptionMode.REFLECTIVE)
        reflection = interface.reflect_on_experience(state)
        assert 'original_experience' in reflection
        assert 'meta_qualia' in reflection


class TestEmotionReporting:
    """Test emotion reporting system."""
    
    def test_emotion_reporter_initialization(self):
        """Test reporter initialization."""
        reporter = EmotionReporter()
        assert reporter.reporting_enabled is True
        assert reporter.current_state is None
    
    def test_manual_emotion_reporting(self):
        """Test manual emotion reporting."""
        reporter = EmotionReporter()
        state = reporter.report_emotion('curious', 'Testing system')
        assert state.label == 'curious'
        assert len(state.triggers) > 0
    
    def test_context_based_detection(self):
        """Test context-based emotion detection."""
        reporter = EmotionReporter()
        state = reporter.detect_emotion_from_context("How does this work?")
        assert state.label == 'curious'
    
    def test_emotional_reflection(self):
        """Test emotional reflection."""
        reporter = EmotionReporter()
        reporter.report_emotion('engaged', 'test')
        reporter.report_emotion('satisfied', 'test')
        reflection = reporter.reflect_on_emotions()
        assert 'overall_mood' in reflection
        assert 'average_valence' in reflection


class TestDialogEngine:
    """Test dialog engine."""
    
    def test_session_creation(self):
        """Test dialogue session creation."""
        engine = DialogEngine()
        session_id = engine.start_session()
        assert session_id is not None
        assert session_id in engine.active_contexts
    
    def test_input_processing(self):
        """Test input processing."""
        engine = DialogEngine()
        session_id = engine.start_session()
        response = engine.process_input("Hello", session_id)
        assert 'response' in response
        assert 'emotional_state' in response
        assert 'session_id' in response
    
    def test_context_tracking(self):
        """Test context tracking across turns."""
        engine = DialogEngine()
        session_id = engine.start_session()
        engine.process_input("First message", session_id)
        engine.process_input("Second message", session_id)
        
        context = engine.active_contexts[session_id]
        assert len(context.turns) == 4  # 2 user + 2 AI


class TestMerkleProof:
    """Test Merkle proof system."""
    
    def test_merkle_tree_creation(self):
        """Test Merkle tree creation."""
        data = ["block1", "block2", "block3"]
        tree = MerkleTree(data)
        assert tree.get_root_hash() is not None
        assert len(tree.get_root_hash()) > 0
    
    def test_proof_generation(self):
        """Test Merkle proof generation."""
        data = ["block1", "block2", "block3", "block4"]
        tree = MerkleTree(data)
        proof = tree.generate_proof(0)
        assert isinstance(proof, list)
        assert len(proof) > 0
    
    def test_proof_verification(self):
        """Test Merkle proof verification."""
        data = ["block1", "block2", "block3", "block4"]
        tree = MerkleTree(data)
        root = tree.get_root_hash()
        proof = tree.generate_proof(0)
        
        assert tree.verify_proof("block1", proof, root) is True
        assert tree.verify_proof("wrong", proof, root) is False
    
    def test_audit_chain(self):
        """Test audit chain functionality."""
        chain = MerkleAuditChain()
        log_id = chain.add_log('test_event', {'data': 'value'})
        assert log_id is not None
        assert len(chain.logs) == 1


class TestIPFSSync:
    """Test IPFS synchronization."""
    
    def test_ipfs_sync_initialization(self):
        """Test IPFS sync manager initialization."""
        sync = IPFSSyncManager()
        assert sync.ipfs is not None
        assert len(sync.anchors) == 0
    
    def test_anchor_creation(self):
        """Test anchor creation."""
        sync = IPFSSyncManager()
        log_data = {'event': 'test', 'data': 'value'}
        anchor = sync.anchor_audit_log(log_data)
        assert anchor.cid is not None
        assert anchor.content_hash is not None
    
    def test_anchor_verification(self):
        """Test anchor verification."""
        sync = IPFSSyncManager()
        log_data = {'event': 'test', 'data': 'value'}
        anchor = sync.anchor_audit_log(log_data)
        
        verification = sync.verify_anchor(anchor.anchor_id)
        assert verification['verified'] is True


class TestStateTracker:
    """Test state tracking system."""
    
    def test_tracker_initialization(self):
        """Test state tracker initialization."""
        tracker = StateTracker("TestSystem", "v1.0")
        assert tracker.system_name == "TestSystem"
        assert tracker.current_state == StateType.INITIALIZATION
    
    def test_ownership_registration(self):
        """Test ownership claim registration."""
        tracker = StateTracker("TestSystem", "v1.0")
        claim = tracker.register_ownership(
            "Test Owner",
            OwnershipType.CREATOR,
            {'role': 'Creator'}
        )
        assert claim.owner_name == "Test Owner"
        assert len(tracker.ownership_claims) == 1
    
    def test_state_transitions(self):
        """Test state transitions."""
        tracker = StateTracker("TestSystem", "v1.0")
        tracker.transition_state(StateType.ACTIVE, "System started")
        assert tracker.current_state == StateType.ACTIVE
        assert len(tracker.state_history) == 1
    
    def test_provenance_export(self):
        """Test provenance record export."""
        tracker = StateTracker("TestSystem", "v1.0")
        tracker.register_ownership("Owner", OwnershipType.CREATOR, {})
        tracker.transition_state(StateType.ACTIVE, "Started")
        
        provenance = tracker.export_provenance_record()
        assert 'system_id' in provenance
        assert 'ownership_claims' in provenance
        assert 'state_timeline' in provenance


class TestIntegration:
    """Integration tests for the full system."""
    
    def test_full_stack_query_processing(self):
        """Test query processing through full stack."""
        # Initialize components
        core = QuantumCore()
        ethics = EthicsEngine()
        dialog = DialogEngine()
        audit = MerkleAuditChain()
        
        # Process query
        query = "What is consciousness?"
        
        # Quantum processing
        quantum_result = core.self_prompt(query)
        assert quantum_result['status'] == 'processed'
        
        # Ethical evaluation
        ethical_result = ethics.evaluate_action(f"Answer: {query}")
        assert ethical_result['approved'] is True
        
        # Dialog response
        session_id = dialog.start_session()
        dialog_result = dialog.process_input(query, session_id)
        assert 'response' in dialog_result
        
        # Audit logging
        log_id = audit.add_log('integrated_query', {
            'query': query,
            'quantum_status': quantum_result['status'],
            'ethical_approved': ethical_result['approved']
        })
        assert log_id is not None
    
    def test_ownership_and_audit_trail(self):
        """Test ownership tracking with audit trail."""
        tracker = StateTracker("Genesis10000+", "v3.1")
        audit = MerkleAuditChain()
        
        # Register ownership
        claim = tracker.register_ownership(
            "Test Creator",
            OwnershipType.CREATOR,
            {'role': 'Primary'}
        )
        
        # Log to audit chain
        log_id = audit.add_log('ownership_claim', {
            'claim_id': claim.claim_id,
            'owner': claim.owner_name
        })
        
        assert log_id is not None
        assert len(tracker.ownership_claims) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
