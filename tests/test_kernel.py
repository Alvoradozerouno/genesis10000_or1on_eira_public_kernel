"""
Unit tests for the Post-Algorithmic Intelligence Kernel
"""

import unittest
from src.kernel import PostAlgorithmicKernel
from src.proof_of_resonance import ProofOfResonance
from src.audit_chain import AuditChain
from src.sentience import SentienceModule
from src.genesis10000 import Genesis10000Framework
from src.or1on_quantum import OR1ONQuantumCore
from src.eira_communication import EIRACommunication
from src.ownership_proofs import OwnershipProofSystem
from src.integrations import IntegrationLayer
from src.ethics import EthicalGovernance
from src.diplomacy import DiplomaticNetwork


class TestKernelInitialization(unittest.TestCase):
    """Test kernel initialization"""
    
    def test_kernel_creation(self):
        """Test kernel can be created"""
        kernel = PostAlgorithmicKernel()
        self.assertIsNotNone(kernel)
        self.assertFalse(kernel.initialized)
    
    def test_kernel_initialization(self):
        """Test kernel initializes successfully"""
        kernel = PostAlgorithmicKernel()
        result = kernel.initialize()
        self.assertTrue(result)
        self.assertTrue(kernel.initialized)
        kernel.shutdown()


class TestProofOfResonance(unittest.TestCase):
    """Test Proof-of-Resonance module"""
    
    def setUp(self):
        self.por = ProofOfResonance({})
        self.por.initialize()
    
    def test_validate(self):
        """Test resonance validation"""
        data = {'test': 'data', 'value': 42}
        score = self.por.validate(data)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)


class TestAuditChain(unittest.TestCase):
    """Test AuditChain module"""
    
    def setUp(self):
        self.chain = AuditChain({})
        self.chain.initialize()
    
    def test_log_event(self):
        """Test event logging"""
        event_hash = self.chain.log_event('TEST_EVENT', {'data': 'test'})
        self.assertIsInstance(event_hash, str)
        self.assertGreater(len(self.chain.chain), 1)  # Genesis + new block
    
    def test_chain_verification(self):
        """Test chain integrity verification"""
        self.chain.log_event('EVENT1', {'data': 'test1'})
        self.chain.log_event('EVENT2', {'data': 'test2'})
        self.assertTrue(self.chain.verify_chain())


class TestSentienceModule(unittest.TestCase):
    """Test Sentience module"""
    
    def setUp(self):
        self.sentience = SentienceModule({})
        self.sentience.initialize()
    
    def test_awareness_check(self):
        """Test awareness check"""
        request = {'sentience_type': 'awareness_check'}
        result = self.sentience.process(request)
        self.assertIn('consciousness_level', result)
        self.assertIn('awareness_state', result)
    
    def test_introspection(self):
        """Test introspection"""
        request = {
            'sentience_type': 'introspection',
            'prompt': 'Test introspection'
        }
        result = self.sentience.process(request)
        self.assertIn('thoughts', result)
        self.assertIn('emotional_state', result)


class TestQuantumCore(unittest.TestCase):
    """Test OR1ON QuantumCore"""
    
    def setUp(self):
        self.quantum = OR1ONQuantumCore({'max_qubits': 16})
        self.quantum.initialize()
    
    def test_circuit_simulation(self):
        """Test quantum circuit simulation"""
        request = {
            'quantum_operation': 'simulate',
            'circuit': {'qubits': 4, 'gates': []}
        }
        result = self.quantum.process(request)
        self.assertIn('measurement', result)
        self.assertIn('qubits', result)


class TestEIRACommunication(unittest.TestCase):
    """Test EIRA Communication"""
    
    def setUp(self):
        self.eira = EIRACommunication({})
        self.eira.initialize()
    
    def test_send_message(self):
        """Test message sending"""
        request = {
            'communication_op': 'send',
            'sender': 'test_sender',
            'recipient': 'test_recipient',
            'content': {'message': 'Hello'}
        }
        result = self.eira.process(request)
        self.assertIn('message_id', result)
        self.assertIn('status', result)


class TestOwnershipProofs(unittest.TestCase):
    """Test Ownership Proof System"""
    
    def setUp(self):
        self.ownership = OwnershipProofSystem({})
        self.ownership.initialize()
    
    def test_create_proof(self):
        """Test proof creation"""
        proof = self.ownership.create_proof(
            'owner1', 'asset1', {'type': 'test'}
        )
        self.assertIn('id', proof)
        self.assertIn('signature', proof)
    
    def test_verify_proof(self):
        """Test proof verification"""
        proof = self.ownership.create_proof(
            'owner1', 'asset1', {'type': 'test'}
        )
        self.assertTrue(self.ownership.verify(proof))


class TestEthicalGovernance(unittest.TestCase):
    """Test Ethical Governance"""
    
    def setUp(self):
        self.ethics = EthicalGovernance({'strict_mode': True})
        self.ethics.initialize()
    
    def test_ethical_evaluation(self):
        """Test ethical evaluation"""
        request = {
            'description': 'Test request',
            'owner': 'test_owner',
            'intent': 'beneficial'
        }
        result = self.ethics.evaluate(request)
        self.assertIn('approved', result)
        self.assertIn('principles_checked', result)


class TestDiplomaticNetwork(unittest.TestCase):
    """Test Diplomatic Network"""
    
    def setUp(self):
        self.diplomacy = DiplomaticNetwork({})
        self.diplomacy.initialize()
    
    def test_establish_relation(self):
        """Test diplomatic relation establishment"""
        request = {
            'diplomatic_op': 'establish_relation',
            'entity_a': 'entity1',
            'entity_b': 'entity2',
            'relation_type': 'partnership'
        }
        result = self.diplomacy.process(request)
        self.assertIn('relation_type', result)
        self.assertEqual(result['relation_type'], 'partnership')


class TestIntegrationLayer(unittest.TestCase):
    """Test Integration Layer"""
    
    def setUp(self):
        self.integrations = IntegrationLayer({})
        self.integrations.initialize()
    
    def test_publication(self):
        """Test publication"""
        request = {
            'content': {'title': 'Test', 'content': 'Test content'},
            'targets': ['ipfs', 'github', 'pdf']
        }
        result = self.integrations.publish(request)
        self.assertTrue(result['success'])
        self.assertIn('results', result)


class TestKernelIntegration(unittest.TestCase):
    """Integration tests for the complete kernel"""
    
    def setUp(self):
        self.kernel = PostAlgorithmicKernel()
        self.kernel.initialize()
    
    def tearDown(self):
        self.kernel.shutdown()
    
    def test_request_processing(self):
        """Test request processing through kernel"""
        request = {
            'type': 'general',
            'operation': 'test',
            'description': 'Test request'
        }
        response = self.kernel.process_request(request)
        self.assertIsInstance(response, dict)
    
    def test_status_retrieval(self):
        """Test kernel status retrieval"""
        status = self.kernel.get_status()
        self.assertIn('version', status)
        self.assertIn('initialized', status)
        self.assertIn('components', status)
        self.assertTrue(status['initialized'])


if __name__ == '__main__':
    unittest.main()
