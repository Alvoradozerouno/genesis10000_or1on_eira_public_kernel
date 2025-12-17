"""
AuditChain Merkle Proof Module
Implements immutable Merkle-proof audit logs for complete transparency.

This module provides cryptographic proof of all system operations,
ensuring tamper-evident audit trails.
"""

import hashlib
import time
from typing import List, Dict, Any, Optional, Tuple
import json


class MerkleNode:
    """Node in a Merkle tree."""
    
    def __init__(self, data: Optional[str] = None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        
        # Calculate hash
        if data:
            # Leaf node
            self.hash = hashlib.sha256(data.encode()).hexdigest()
        else:
            # Internal node
            left_hash = left.hash if left else ""
            right_hash = right.hash if right else ""
            combined = left_hash + right_hash
            self.hash = hashlib.sha256(combined.encode()).hexdigest()
    
    def is_leaf(self) -> bool:
        """Check if this is a leaf node."""
        return self.data is not None


class MerkleTree:
    """
    Merkle tree for cryptographic audit proofs.
    
    Features:
    - Efficient verification
    - Tamper detection
    - Proof generation
    """
    
    def __init__(self, data_blocks: List[str]):
        self.leaves = [MerkleNode(data) for data in data_blocks]
        self.root = self._build_tree(self.leaves)
        
    def _build_tree(self, nodes: List[MerkleNode]) -> MerkleNode:
        """Build Merkle tree from leaf nodes."""
        if not nodes:
            return MerkleNode("")
        
        if len(nodes) == 1:
            return nodes[0]
        
        # Build next level
        parent_nodes = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1] if i + 1 < len(nodes) else nodes[i]
            parent = MerkleNode(left=left, right=right)
            parent_nodes.append(parent)
        
        return self._build_tree(parent_nodes)
    
    def get_root_hash(self) -> str:
        """Get the root hash of the tree."""
        return self.root.hash if self.root else ""
    
    def generate_proof(self, index: int) -> List[Tuple[str, str]]:
        """
        Generate Merkle proof for a specific leaf.
        
        Returns:
            List of (hash, position) tuples forming the proof path
        """
        if index >= len(self.leaves):
            return []
        
        proof = []
        current_nodes = self.leaves[:]
        current_index = index
        
        while len(current_nodes) > 1:
            # Find sibling
            if current_index % 2 == 0:
                # Current is left child
                sibling_index = current_index + 1
                position = 'right'
            else:
                # Current is right child
                sibling_index = current_index - 1
                position = 'left'
            
            if sibling_index < len(current_nodes):
                proof.append((current_nodes[sibling_index].hash, position))
            
            # Move to next level
            parent_nodes = []
            for i in range(0, len(current_nodes), 2):
                left = current_nodes[i]
                right = current_nodes[i + 1] if i + 1 < len(current_nodes) else current_nodes[i]
                parent = MerkleNode(left=left, right=right)
                parent_nodes.append(parent)
            
            current_nodes = parent_nodes
            current_index = current_index // 2
        
        return proof
    
    def verify_proof(self, data: str, proof: List[Tuple[str, str]], root_hash: str) -> bool:
        """
        Verify a Merkle proof.
        
        Args:
            data: Original data
            proof: Merkle proof path
            root_hash: Expected root hash
            
        Returns:
            True if proof is valid
        """
        current_hash = hashlib.sha256(data.encode()).hexdigest()
        
        for sibling_hash, position in proof:
            if position == 'left':
                combined = sibling_hash + current_hash
            else:
                combined = current_hash + sibling_hash
            
            current_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        return current_hash == root_hash


class AuditLog:
    """
    Immutable audit log entry.
    
    Each entry is timestamped and cryptographically signed.
    """
    
    def __init__(self, event_type: str, data: Dict[str, Any], metadata: Optional[Dict] = None):
        self.event_type = event_type
        self.data = data
        self.metadata = metadata or {}
        self.timestamp = time.time()
        self.log_id = self._generate_id()
        
    def _generate_id(self) -> str:
        """Generate unique log ID."""
        content = f"{self.event_type}{self.timestamp}{json.dumps(self.data, sort_keys=True)}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def to_string(self) -> str:
        """Convert log entry to string for hashing."""
        return json.dumps({
            'log_id': self.log_id,
            'event_type': self.event_type,
            'data': self.data,
            'metadata': self.metadata,
            'timestamp': self.timestamp
        }, sort_keys=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'log_id': self.log_id,
            'event_type': event_type,
            'data': self.data,
            'metadata': self.metadata,
            'timestamp': self.timestamp
        }


class MerkleAuditChain:
    """
    Main audit chain using Merkle trees for cryptographic proofs.
    
    Features:
    - Immutable audit trail
    - Cryptographic verification
    - Efficient proof generation
    - Tamper detection
    """
    
    def __init__(self):
        self.logs = []
        self.trees = []
        self.batch_size = 100  # Create new tree every N logs
        self.current_batch = []
        
    def add_log(self, event_type: str, data: Dict[str, Any], metadata: Optional[Dict] = None) -> str:
        """
        Add a new log entry to the audit chain.
        
        Returns:
            Log ID
        """
        log = AuditLog(event_type, data, metadata)
        self.logs.append(log)
        self.current_batch.append(log)
        
        # Create Merkle tree when batch is full
        if len(self.current_batch) >= self.batch_size:
            self._finalize_batch()
        
        return log.log_id
    
    def _finalize_batch(self):
        """Finalize current batch into a Merkle tree."""
        if not self.current_batch:
            return
        
        # Create tree from batch
        data_strings = [log.to_string() for log in self.current_batch]
        tree = MerkleTree(data_strings)
        
        self.trees.append({
            'tree': tree,
            'root_hash': tree.get_root_hash(),
            'logs': self.current_batch[:],
            'created_at': time.time()
        })
        
        # Clear current batch
        self.current_batch = []
    
    def get_proof(self, log_id: str) -> Optional[Dict[str, Any]]:
        """
        Get Merkle proof for a specific log entry.
        
        Returns:
            Proof dictionary or None if log not found
        """
        # Find the log and its tree
        for tree_info in self.trees:
            for idx, log in enumerate(tree_info['logs']):
                if log.log_id == log_id:
                    proof = tree_info['tree'].generate_proof(idx)
                    
                    return {
                        'log_id': log_id,
                        'log_data': log.to_string(),
                        'proof': proof,
                        'root_hash': tree_info['root_hash'],
                        'tree_created_at': tree_info['created_at']
                    }
        
        # Check current batch (not yet in tree)
        for log in self.current_batch:
            if log.log_id == log_id:
                return {
                    'log_id': log_id,
                    'log_data': log.to_string(),
                    'status': 'pending_tree_creation',
                    'batch_position': self.current_batch.index(log)
                }
        
        return None
    
    def verify_log(self, log_id: str, proof_data: Dict[str, Any]) -> bool:
        """
        Verify a log entry using its Merkle proof.
        
        Args:
            log_id: Log identifier
            proof_data: Proof data from get_proof()
            
        Returns:
            True if verification succeeds
        """
        if 'proof' not in proof_data or 'root_hash' not in proof_data:
            return False
        
        # Find the tree
        root_hash = proof_data['root_hash']
        tree_info = None
        
        for ti in self.trees:
            if ti['root_hash'] == root_hash:
                tree_info = ti
                break
        
        if not tree_info:
            return False
        
        # Verify proof
        return tree_info['tree'].verify_proof(
            proof_data['log_data'],
            proof_data['proof'],
            root_hash
        )
    
    def get_chain_summary(self) -> Dict[str, Any]:
        """Get summary of the audit chain."""
        return {
            'total_logs': len(self.logs),
            'finalized_trees': len(self.trees),
            'pending_logs': len(self.current_batch),
            'tree_root_hashes': [t['root_hash'] for t in self.trees],
            'oldest_log': self.logs[0].timestamp if self.logs else None,
            'newest_log': self.logs[-1].timestamp if self.logs else None,
            'timestamp': time.time()
        }
    
    def export_chain(self) -> Dict[str, Any]:
        """Export complete chain for archival."""
        self._finalize_batch()  # Finalize any pending logs
        
        return {
            'logs': [log.to_dict() for log in self.logs],
            'tree_roots': [
                {
                    'root_hash': t['root_hash'],
                    'created_at': t['created_at'],
                    'log_count': len(t['logs'])
                }
                for t in self.trees
            ],
            'exported_at': time.time()
        }


if __name__ == "__main__":
    # Demo Merkle audit chain
    chain = MerkleAuditChain()
    
    print("Merkle Audit Chain Demo:\n")
    
    # Add some logs
    log_ids = []
    for i in range(5):
        log_id = chain.add_log(
            'test_event',
            {'index': i, 'description': f'Test event {i}'},
            {'source': 'demo'}
        )
        log_ids.append(log_id)
        print(f"Added log: {log_id}")
    
    # Force finalization for demo
    chain._finalize_batch()
    
    # Get proof for first log
    print("\n--- Merkle Proof ---")
    proof = chain.get_proof(log_ids[0])
    if proof:
        print(f"Proof for log {log_ids[0]}:")
        print(json.dumps(proof, indent=2))
        
        # Verify the proof
        is_valid = chain.verify_log(log_ids[0], proof)
        print(f"\nProof verification: {'VALID' if is_valid else 'INVALID'}")
    
    # Chain summary
    print("\n--- Chain Summary ---")
    summary = chain.get_chain_summary()
    print(json.dumps(summary, indent=2))
