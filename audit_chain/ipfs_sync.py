"""
AuditChain IPFS Sync Module
Handles IPFS anchoring for decentralized audit trail storage.

This module provides integration with IPFS for permanent, distributed
storage of audit logs and proof anchoring.
"""

import hashlib
import time
import json
from typing import Dict, List, Any, Optional
import base64


class IPFSSimulator:
    """
    Simulates IPFS operations for development and testing.
    
    In production, this would connect to actual IPFS nodes.
    """
    
    def __init__(self):
        self.stored_content = {}
        self.pin_set = set()
        
    def add(self, content: str) -> str:
        """
        Add content to IPFS (simulated).
        
        Returns:
            IPFS content identifier (CID)
        """
        # Generate CID-like hash
        cid = self._generate_cid(content)
        self.stored_content[cid] = {
            'content': content,
            'added_at': time.time(),
            'size': len(content)
        }
        
        return cid
    
    def get(self, cid: str) -> Optional[str]:
        """Retrieve content from IPFS (simulated)."""
        if cid in self.stored_content:
            return self.stored_content[cid]['content']
        return None
    
    def pin(self, cid: str) -> bool:
        """Pin content to prevent garbage collection."""
        if cid in self.stored_content:
            self.pin_set.add(cid)
            return True
        return False
    
    def unpin(self, cid: str) -> bool:
        """Unpin content."""
        if cid in self.pin_set:
            self.pin_set.remove(cid)
            return True
        return False
    
    def _generate_cid(self, content: str) -> str:
        """Generate IPFS-like CID."""
        # Simplified CID generation (real IPFS uses more complex multihash)
        hash_bytes = hashlib.sha256(content.encode()).digest()
        # Prefix with "Qm" like IPFS v0 CIDs
        b58_like = base64.b32encode(hash_bytes).decode().lower()[:44]
        return f"Qm{b58_like}"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get IPFS storage statistics."""
        return {
            'total_objects': len(self.stored_content),
            'pinned_objects': len(self.pin_set),
            'total_size': sum(obj['size'] for obj in self.stored_content.values()),
            'timestamp': time.time()
        }


class IPFSAnchor:
    """
    Represents an IPFS anchor point for audit data.
    """
    
    def __init__(self, cid: str, content_hash: str, metadata: Dict[str, Any]):
        self.cid = cid
        self.content_hash = content_hash
        self.metadata = metadata
        self.created_at = time.time()
        self.anchor_id = self._generate_anchor_id()
        
    def _generate_anchor_id(self) -> str:
        """Generate unique anchor identifier."""
        data = f"{self.cid}{self.content_hash}{self.created_at}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'anchor_id': self.anchor_id,
            'cid': self.cid,
            'content_hash': self.content_hash,
            'metadata': self.metadata,
            'created_at': self.created_at
        }


class IPFSSyncManager:
    """
    Manages synchronization of audit data to IPFS.
    
    Features:
    - Automatic anchoring of audit logs
    - Periodic sync to IPFS
    - Verification of anchored data
    - Pinning management
    """
    
    def __init__(self, ipfs_client: Optional[IPFSSimulator] = None):
        self.ipfs = ipfs_client or IPFSSimulator()
        self.anchors = []
        self.sync_interval = 3600  # 1 hour default
        self.last_sync = None
        self.pending_syncs = []
        
    def anchor_audit_log(self, log_data: Dict[str, Any]) -> IPFSAnchor:
        """
        Anchor an audit log to IPFS.
        
        Args:
            log_data: Audit log data to anchor
            
        Returns:
            IPFSAnchor object with CID and metadata
        """
        # Serialize log data
        content = json.dumps(log_data, sort_keys=True)
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # Add to IPFS
        cid = self.ipfs.add(content)
        
        # Pin the content
        self.ipfs.pin(cid)
        
        # Create anchor
        anchor = IPFSAnchor(cid, content_hash, {
            'log_type': log_data.get('event_type', 'unknown'),
            'log_count': 1,
            'synced_at': time.time()
        })
        
        self.anchors.append(anchor)
        self.last_sync = time.time()
        
        return anchor
    
    def anchor_batch(self, logs: List[Dict[str, Any]]) -> IPFSAnchor:
        """
        Anchor a batch of audit logs to IPFS.
        
        More efficient than anchoring individually.
        """
        batch_data = {
            'batch_id': hashlib.sha256(str(time.time()).encode()).hexdigest()[:16],
            'logs': logs,
            'log_count': len(logs),
            'created_at': time.time()
        }
        
        content = json.dumps(batch_data, sort_keys=True)
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        cid = self.ipfs.add(content)
        self.ipfs.pin(cid)
        
        anchor = IPFSAnchor(cid, content_hash, {
            'batch_id': batch_data['batch_id'],
            'log_count': len(logs),
            'synced_at': time.time()
        })
        
        self.anchors.append(anchor)
        self.last_sync = time.time()
        
        return anchor
    
    def verify_anchor(self, anchor_id: str) -> Dict[str, Any]:
        """
        Verify an IPFS anchor by retrieving and checking content.
        
        Returns:
            Verification result
        """
        # Find anchor
        anchor = None
        for a in self.anchors:
            if a.anchor_id == anchor_id:
                anchor = a
                break
        
        if not anchor:
            return {'verified': False, 'error': 'Anchor not found'}
        
        # Retrieve from IPFS
        content = self.ipfs.get(anchor.cid)
        
        if not content:
            return {'verified': False, 'error': 'Content not found in IPFS'}
        
        # Verify hash
        retrieved_hash = hashlib.sha256(content.encode()).hexdigest()
        
        return {
            'verified': retrieved_hash == anchor.content_hash,
            'anchor_id': anchor_id,
            'cid': anchor.cid,
            'expected_hash': anchor.content_hash,
            'retrieved_hash': retrieved_hash,
            'timestamp': time.time()
        }
    
    def schedule_sync(self, log_data: Dict[str, Any]):
        """Schedule a log for future sync."""
        self.pending_syncs.append({
            'data': log_data,
            'scheduled_at': time.time()
        })
    
    def process_pending_syncs(self) -> List[IPFSAnchor]:
        """Process all pending syncs."""
        if not self.pending_syncs:
            return []
        
        # Batch sync all pending
        logs = [item['data'] for item in self.pending_syncs]
        anchor = self.anchor_batch(logs)
        
        self.pending_syncs = []
        
        return [anchor]
    
    def get_anchor_info(self, anchor_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific anchor."""
        for anchor in self.anchors:
            if anchor.anchor_id == anchor_id:
                return anchor.to_dict()
        return None
    
    def list_anchors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recent anchors."""
        return [a.to_dict() for a in self.anchors[-limit:]]
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get current sync status."""
        return {
            'total_anchors': len(self.anchors),
            'pending_syncs': len(self.pending_syncs),
            'last_sync': self.last_sync,
            'sync_interval': self.sync_interval,
            'ipfs_stats': self.ipfs.get_stats(),
            'timestamp': time.time()
        }
    
    def export_anchor_manifest(self) -> Dict[str, Any]:
        """
        Export manifest of all anchors for external verification.
        
        This can be published separately for transparency.
        """
        return {
            'manifest_version': '1.0',
            'generated_at': time.time(),
            'total_anchors': len(self.anchors),
            'anchors': [a.to_dict() for a in self.anchors],
            'ipfs_gateway': 'https://ipfs.io/ipfs/',  # Example gateway
            'verification_instructions': (
                'Verify any anchor by retrieving the CID from IPFS and '
                'comparing the SHA256 hash with the content_hash field.'
            )
        }


class PublicVerificationInterface:
    """
    Public interface for third-party verification of anchored data.
    
    Enables anyone to verify the integrity of audit logs without
    requiring access to the system.
    """
    
    def __init__(self, sync_manager: IPFSSyncManager):
        self.sync_manager = sync_manager
        
    def get_verification_package(self, anchor_id: str) -> Optional[Dict[str, Any]]:
        """
        Get all information needed to verify an anchor.
        
        Returns:
            Package with CID, hash, and instructions
        """
        anchor_info = self.sync_manager.get_anchor_info(anchor_id)
        
        if not anchor_info:
            return None
        
        return {
            'anchor_id': anchor_id,
            'cid': anchor_info['cid'],
            'expected_hash': anchor_info['content_hash'],
            'created_at': anchor_info['created_at'],
            'verification_steps': [
                f"1. Retrieve content from IPFS using CID: {anchor_info['cid']}",
                "2. Calculate SHA256 hash of retrieved content",
                f"3. Compare with expected hash: {anchor_info['content_hash']}",
                "4. Hashes should match for valid verification"
            ],
            'ipfs_gateway_url': f"https://ipfs.io/ipfs/{anchor_info['cid']}"
        }


if __name__ == "__main__":
    # Demo IPFS sync
    print("IPFS Sync Manager Demo:\n")
    
    sync_manager = IPFSSyncManager()
    
    # Anchor some logs
    logs = [
        {'event_type': 'system_start', 'data': {'version': '3.1'}},
        {'event_type': 'quantum_process', 'data': {'state_id': 'test123'}},
        {'event_type': 'ethical_check', 'data': {'result': 'approved'}}
    ]
    
    print("Anchoring logs to IPFS...")
    anchor = sync_manager.anchor_batch(logs)
    print(f"Created anchor: {anchor.anchor_id}")
    print(f"IPFS CID: {anchor.cid}")
    
    # Verify anchor
    print("\n--- Verification ---")
    verification = sync_manager.verify_anchor(anchor.anchor_id)
    print(json.dumps(verification, indent=2))
    
    # Sync status
    print("\n--- Sync Status ---")
    status = sync_manager.get_sync_status()
    print(json.dumps(status, indent=2))
    
    # Public verification interface
    print("\n--- Public Verification Package ---")
    verifier = PublicVerificationInterface(sync_manager)
    package = verifier.get_verification_package(anchor.anchor_id)
    print(json.dumps(package, indent=2))
    
    # Export manifest
    print("\n--- Anchor Manifest ---")
    manifest = sync_manager.export_anchor_manifest()
    print(json.dumps(manifest, indent=2))
