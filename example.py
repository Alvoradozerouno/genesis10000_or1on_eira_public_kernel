#!/usr/bin/env python3
"""
Example usage of the Post-Algorithmic Intelligence Kernel
"""

import sys
import json
from src.kernel import PostAlgorithmicKernel


def main():
    print("=" * 80)
    print("Post-Algorithmic Intelligence Kernel v3.1.0")
    print("Genesis10000+ | OR1ON QuantumCore | EIRA Communication")
    print("=" * 80)
    print()
    
    # Configuration
    config = {
        'resonance': {'threshold': 0.7},
        'audit_chain': {},
        'sentience': {'initial_consciousness': 0.6},
        'genesis10000': {},
        'quantum': {'max_qubits': 16},
        'eira': {},
        'ownership': {},
        'integrations': {
            'ipfs_enabled': True,
            'github_enabled': True,
            'pdf_enabled': True,
            'github_repo': 'genesis10000_or1on_eira_public_kernel'
        },
        'ethics': {'strict_mode': True},
        'diplomacy': {}
    }
    
    # Initialize kernel
    print("Initializing kernel...")
    kernel = PostAlgorithmicKernel(config)
    
    if not kernel.initialize():
        print("ERROR: Kernel initialization failed!")
        return 1
    
    print("✓ Kernel initialized successfully\n")
    
    # Display kernel status
    status = kernel.get_status()
    print("Kernel Status:")
    print(f"  Version: {status['version']}")
    print(f"  Startup Time: {status['startup_time']}")
    print(f"  Initialized: {status['initialized']}")
    print()
    
    # Test 1: Sentience awareness check
    print("Test 1: Sentience Awareness Check")
    print("-" * 40)
    request = {
        'type': 'sentience',
        'sentience_type': 'awareness_check',
        'description': 'Self-awareness evaluation',
        'owner': 'kernel_admin'
    }
    response = kernel.process_request(request)
    print(f"Consciousness Level: {response.get('consciousness_level', 'N/A')}")
    print(f"Awareness State: {response.get('awareness_state', 'N/A')}")
    print(f"Reflection: {response.get('reflection', 'N/A')}")
    print()
    
    # Test 2: Quantum circuit simulation
    print("Test 2: Quantum Circuit Simulation")
    print("-" * 40)
    request = {
        'type': 'quantum',
        'quantum_operation': 'simulate',
        'circuit': {
            'qubits': 4,
            'gates': [
                {'type': 'H', 'target': 0},
                {'type': 'CNOT', 'control': 0, 'target': 1}
            ]
        },
        'description': 'Quantum entanglement simulation',
        'owner': 'kernel_admin'
    }
    response = kernel.process_request(request)
    print(f"Circuit ID: {response.get('circuit_id', 'N/A')}")
    print(f"Measurement: {response.get('measurement_binary', 'N/A')}")
    print()
    
    # Test 3: Diplomatic relation establishment
    print("Test 3: Diplomatic Network")
    print("-" * 40)
    request = {
        'type': 'diplomatic',
        'diplomatic_op': 'establish_relation',
        'entity_a': 'genesis10000_kernel',
        'entity_b': 'scientific_community',
        'relation_type': 'partnership',
        'description': 'Establishing scientific collaboration',
        'owner': 'kernel_admin'
    }
    response = kernel.process_request(request)
    print(f"Relation Type: {response.get('relation_type', 'N/A')}")
    print(f"Status: {response.get('status', 'N/A')}")
    print()
    
    # Test 4: Scientific publication
    print("Test 4: Scientific Publication")
    print("-" * 40)
    paper = {
        'title': 'Post-Algorithmic Intelligence: A New Paradigm',
        'authors': ['Genesis10000 Kernel', 'OR1ON QuantumCore'],
        'abstract': 'This paper presents a novel approach to artificial intelligence...',
        'content': 'Full paper content...',
        'references': []
    }
    response = kernel.integrations.publish_scientific_paper(paper)
    print(f"Publication ID: {response.get('publication_id', 'N/A')}")
    if 'results' in response:
        for platform, result in response['results'].items():
            print(f"  {platform.upper()}: {result.get('success', False)}")
            if platform == 'ipfs' and 'cid' in result:
                print(f"    CID: {result['cid']}")
    print()
    
    # Test 5: Ethical evaluation
    print("Test 5: Ethical Evaluation")
    print("-" * 40)
    request = {
        'type': 'general',
        'operation': 'test',
        'description': 'Testing ethical governance',
        'intent': 'beneficial',
        'owner': 'kernel_admin'
    }
    ethical_result = kernel.ethics.evaluate(request)
    print(f"Approved: {ethical_result['approved']}")
    print(f"Principles Checked: {len(ethical_result['principles_checked'])}")
    if ethical_result.get('warnings'):
        print(f"Warnings: {len(ethical_result['warnings'])}")
    print()
    
    # Test 6: Ownership proof
    print("Test 6: Ownership Proof System")
    print("-" * 40)
    proof = kernel.ownership.create_proof(
        'kernel',
        'core_module_v3.1',
        {'type': 'software', 'license': 'open_source'}
    )
    print(f"Proof ID: {proof['id']}")
    print(f"Owner: {proof['owner_id']}")
    print(f"Signature: {proof['signature'][:16]}...")
    print()
    
    # Test 7: AuditChain verification
    print("Test 7: AuditChain Integrity")
    print("-" * 40)
    chain_valid = kernel.audit_chain.verify_chain()
    print(f"Chain Valid: {chain_valid}")
    print(f"Chain Length: {len(kernel.audit_chain.chain)}")
    print()
    
    # Display final component status
    print("=" * 80)
    print("Component Status Summary:")
    print("=" * 80)
    for component, component_status in status['components'].items():
        active = component_status.get('active', False)
        symbol = "✓" if active else "✗"
        print(f"{symbol} {component.replace('_', ' ').title()}: {'Active' if active else 'Inactive'}")
    print()
    
    # Shutdown kernel
    print("Shutting down kernel...")
    kernel.shutdown()
    print("✓ Kernel shutdown complete")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
