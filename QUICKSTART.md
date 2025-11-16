# Quick Start Guide

## Post-Algorithmic Intelligence Kernel v3.1.0

This guide will help you get started with the Genesis10000+ OR1ON EIRA Public Kernel.

## Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses Python standard library only)

## Installation

```bash
# Clone the repository
git clone https://github.com/Alvoradozerouno/genesis10000_or1on_eira_public_kernel.git
cd genesis10000_or1on_eira_public_kernel
```

## Running the Example

The quickest way to see the kernel in action:

```bash
python3 example.py
```

This will demonstrate:
- ✓ Kernel initialization
- ✓ Sentience awareness check
- ✓ Quantum circuit simulation
- ✓ Diplomatic relation establishment
- ✓ Scientific publication to IPFS/GitHub/PDF
- ✓ Ethical evaluation
- ✓ Ownership proof creation
- ✓ AuditChain integrity verification

## Running Tests

```bash
python3 -m unittest tests/test_kernel.py -v
```

Expected output: All 16 tests passing ✓

## Basic Usage

### 1. Initialize the Kernel

```python
from src.kernel import PostAlgorithmicKernel

# Create kernel with configuration
kernel = PostAlgorithmicKernel({
    'ethics': {'strict_mode': True},
    'quantum': {'max_qubits': 16},
    'sentience': {'initial_consciousness': 0.6}
})

# Initialize all components
kernel.initialize()
```

### 2. Check Sentience

```python
response = kernel.process_request({
    'type': 'sentience',
    'sentience_type': 'awareness_check',
    'owner': 'your_id'
})

print(f"Consciousness: {response['consciousness_level']}")
print(f"State: {response['awareness_state']}")
```

### 3. Run Quantum Simulation

```python
response = kernel.process_request({
    'type': 'quantum',
    'quantum_operation': 'simulate',
    'circuit': {
        'qubits': 4,
        'gates': [
            {'type': 'H', 'target': 0},
            {'type': 'CNOT', 'control': 0, 'target': 1}
        ]
    },
    'owner': 'your_id'
})

print(f"Measurement: {response['measurement_binary']}")
```

### 4. Establish Diplomatic Relations

```python
response = kernel.process_request({
    'type': 'diplomatic',
    'diplomatic_op': 'establish_relation',
    'entity_a': 'your_entity',
    'entity_b': 'partner_entity',
    'relation_type': 'partnership',
    'owner': 'your_id'
})
```

### 5. Publish Scientific Paper

```python
paper = {
    'title': 'My Research Paper',
    'authors': ['Your Name'],
    'abstract': 'Research abstract...',
    'content': 'Full paper content...',
    'references': []
}

result = kernel.integrations.publish_scientific_paper(paper)

# Create DOI
doi = kernel.integrations.create_doi(result['publication_id'])
print(f"DOI: {doi['doi']}")
```

### 6. Get Kernel Status

```python
status = kernel.get_status()
print(f"Version: {status['version']}")
print(f"Initialized: {status['initialized']}")

# Check component status
for component, info in status['components'].items():
    print(f"{component}: {info['active']}")
```

### 7. Shutdown Gracefully

```python
kernel.shutdown()
```

## Key Features

### Ethical AI
Every request is automatically evaluated against 8 ethical principles:
- Transparency
- Fairness
- Accountability
- Privacy
- Safety
- Beneficence
- Non-maleficence
- Autonomy

### Audit Trail
All operations are logged to an immutable blockchain (AuditChain):
```python
# Verify chain integrity
is_valid = kernel.audit_chain.verify_chain()

# Get recent events
events = kernel.audit_chain.get_events(limit=10)
```

### Ownership Proofs
Create and verify cryptographic ownership proofs:
```python
proof = kernel.ownership.create_proof(
    'owner_id',
    'asset_id',
    {'type': 'intellectual_property'}
)

is_valid = kernel.ownership.verify(proof)
```

### Quantum Computing
Simulate quantum circuits up to 16 qubits:
```python
response = kernel.quantum_core.process({
    'quantum_operation': 'entangle',
    'qubits': 2
})
```

## Configuration

Customize kernel behavior via config dictionary:

```python
config = {
    'resonance': {
        'threshold': 0.7  # Consensus threshold
    },
    'sentience': {
        'initial_consciousness': 0.6
    },
    'quantum': {
        'max_qubits': 16
    },
    'ethics': {
        'strict_mode': True  # Fail on first ethical violation
    },
    'integrations': {
        'ipfs_enabled': True,
        'github_enabled': True,
        'pdf_enabled': True,
        'github_repo': 'your_repo_name'
    }
}

kernel = PostAlgorithmicKernel(config)
```

## Troubleshooting

### All requests fail ethical validation
Ensure requests include an 'owner' field:
```python
request = {
    'type': 'general',
    'owner': 'your_id',  # Required for accountability
    'description': 'What you want to do'
}
```

### Import errors
Make sure you're running from the repository root:
```bash
cd genesis10000_or1on_eira_public_kernel
python3 example.py
```

### Tests fail
Ensure you're using Python 3.7+:
```bash
python3 --version
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Check [example.py](example.py) for more usage examples
- Review source code in `src/` directory

## Support

- GitHub Issues: https://github.com/Alvoradozerouno/genesis10000_or1on_eira_public_kernel/issues
- Documentation: See README.md
- Examples: See example.py

## License

MIT License - See [LICENSE](LICENSE) file for details
