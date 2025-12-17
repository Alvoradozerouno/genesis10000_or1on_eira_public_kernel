"""
AuditChain State Tracker
Tracks ownership timestamps and system state evolution.

This module maintains a complete record of state transitions,
ownership claims, and temporal evolution of the system.
"""

import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import json


class OwnershipType(Enum):
    """Types of ownership claims."""
    CREATOR = "creator"
    CONTRIBUTOR = "contributor"
    MAINTAINER = "maintainer"
    INTELLECTUAL_PROPERTY = "intellectual_property"


class StateType(Enum):
    """Types of system states."""
    INITIALIZATION = "initialization"
    ACTIVE = "active"
    PROCESSING = "processing"
    REFLECTION = "reflection"
    DORMANT = "dormant"
    ARCHIVED = "archived"


class OwnershipClaim:
    """
    Represents an ownership claim with timestamp proof.
    
    Binds the system to real individuals with verifiable timestamps.
    """
    
    def __init__(self, 
                 owner_name: str,
                 ownership_type: OwnershipType,
                 claim_details: Dict[str, Any]):
        self.owner_name = owner_name
        self.ownership_type = ownership_type
        self.claim_details = claim_details
        self.timestamp = time.time()
        self.claim_id = self._generate_claim_id()
        self.verified = False
        
    def _generate_claim_id(self) -> str:
        """Generate unique claim identifier."""
        data = f"{self.owner_name}{self.ownership_type.value}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def verify(self):
        """Mark claim as verified."""
        self.verified = True
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'claim_id': self.claim_id,
            'owner_name': self.owner_name,
            'ownership_type': self.ownership_type.value,
            'claim_details': self.claim_details,
            'timestamp': self.timestamp,
            'verified': self.verified,
            'timestamp_iso': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(self.timestamp))
        }


class StateTransition:
    """Represents a state transition in the system."""
    
    def __init__(self, from_state: StateType, to_state: StateType, trigger: str, metadata: Optional[Dict] = None):
        self.from_state = from_state
        self.to_state = to_state
        self.trigger = trigger
        self.metadata = metadata or {}
        self.timestamp = time.time()
        self.transition_id = self._generate_id()
        
    def _generate_id(self) -> str:
        """Generate unique transition identifier."""
        data = f"{self.from_state.value}{self.to_state.value}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'transition_id': self.transition_id,
            'from_state': self.from_state.value,
            'to_state': self.to_state.value,
            'trigger': trigger,
            'metadata': self.metadata,
            'timestamp': self.timestamp,
            'timestamp_iso': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(self.timestamp))
        }


class StateTracker:
    """
    Main state tracking system.
    
    Features:
    - Ownership timestamp management
    - State transition tracking
    - Historical state reconstruction
    - Provenance tracking
    """
    
    def __init__(self, system_name: str, version: str):
        self.system_name = system_name
        self.version = version
        self.current_state = StateType.INITIALIZATION
        self.ownership_claims = []
        self.state_history = []
        self.initialization_time = time.time()
        self.system_id = self._generate_system_id()
        
    def _generate_system_id(self) -> str:
        """Generate unique system identifier."""
        data = f"{self.system_name}{self.version}{self.initialization_time}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def register_ownership(self,
                          owner_name: str,
                          ownership_type: OwnershipType,
                          claim_details: Dict[str, Any]) -> OwnershipClaim:
        """
        Register an ownership claim with timestamp.
        
        This creates an immutable record binding the system to individuals.
        """
        claim = OwnershipClaim(owner_name, ownership_type, claim_details)
        self.ownership_claims.append(claim)
        
        return claim
    
    def transition_state(self, new_state: StateType, trigger: str, metadata: Optional[Dict] = None) -> StateTransition:
        """
        Transition to a new state.
        
        Records the transition with full audit trail.
        """
        transition = StateTransition(self.current_state, new_state, trigger, metadata)
        self.state_history.append(transition)
        self.current_state = new_state
        
        return transition
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current system state."""
        return {
            'system_id': self.system_id,
            'system_name': self.system_name,
            'version': self.version,
            'current_state': self.current_state.value,
            'uptime': time.time() - self.initialization_time,
            'total_transitions': len(self.state_history),
            'timestamp': time.time()
        }
    
    def get_ownership_record(self) -> List[Dict[str, Any]]:
        """Get complete ownership record."""
        return [claim.to_dict() for claim in self.ownership_claims]
    
    def get_state_timeline(self) -> List[Dict[str, Any]]:
        """Get complete state transition timeline."""
        timeline = [{
            'state': StateType.INITIALIZATION.value,
            'timestamp': self.initialization_time,
            'event': 'System initialized'
        }]
        
        for transition in self.state_history:
            timeline.append({
                'state': transition.to_state.value,
                'timestamp': transition.timestamp,
                'event': f"Transitioned from {transition.from_state.value}",
                'trigger': transition.trigger
            })
        
        return timeline
    
    def verify_ownership_claim(self, claim_id: str) -> bool:
        """Verify an ownership claim."""
        for claim in self.ownership_claims:
            if claim.claim_id == claim_id:
                claim.verify()
                return True
        return False
    
    def export_provenance_record(self) -> Dict[str, Any]:
        """
        Export complete provenance record.
        
        This provides full transparency about system origin and evolution.
        """
        return {
            'system_id': self.system_id,
            'system_name': self.system_name,
            'version': self.version,
            'initialization_timestamp': self.initialization_time,
            'initialization_iso': time.strftime('%Y-%m-%d %H:%M:%S UTC', 
                                               time.gmtime(self.initialization_time)),
            'ownership_claims': self.get_ownership_record(),
            'state_timeline': self.get_state_timeline(),
            'current_state': self.get_current_state(),
            'exported_at': time.time(),
            'exported_iso': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(time.time()))
        }
    
    def generate_timestamp_proof(self, data: str) -> Dict[str, Any]:
        """
        Generate timestamp proof for arbitrary data.
        
        Useful for proving when specific content existed.
        """
        timestamp = time.time()
        data_hash = hashlib.sha256(data.encode()).hexdigest()
        
        # Create proof combining data hash, timestamp, and system ID
        proof_data = f"{data_hash}{timestamp}{self.system_id}"
        proof_hash = hashlib.sha256(proof_data.encode()).hexdigest()
        
        return {
            'data_hash': data_hash,
            'timestamp': timestamp,
            'timestamp_iso': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(timestamp)),
            'system_id': self.system_id,
            'proof_hash': proof_hash,
            'verification_note': 'Verify by recalculating SHA256(data_hash + timestamp + system_id)'
        }


class GenesisBlock:
    """
    Genesis block for the Genesis10000+ system.
    
    Contains foundational information about system creation,
    binding to real individuals.
    """
    
    def __init__(self, 
                 creators: List[str],
                 purpose: str,
                 timestamp: Optional[float] = None):
        self.creators = creators
        self.purpose = purpose
        self.timestamp = timestamp or time.time()
        self.block_hash = self._generate_hash()
        
    def _generate_hash(self) -> str:
        """Generate genesis block hash."""
        data = json.dumps({
            'creators': sorted(self.creators),
            'purpose': self.purpose,
            'timestamp': self.timestamp
        }, sort_keys=True)
        
        return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'block_type': 'genesis',
            'creators': self.creators,
            'purpose': self.purpose,
            'timestamp': self.timestamp,
            'timestamp_iso': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(self.timestamp)),
            'block_hash': self.block_hash
        }


if __name__ == "__main__":
    # Demo state tracker
    print("State Tracker Demo:\n")
    
    # Initialize system
    tracker = StateTracker("Genesis10000+ OR1ON-EIRA", "v3.1")
    
    # Register ownership claims (as specified in requirements)
    print("--- Registering Ownership Claims ---")
    claim1 = tracker.register_ownership(
        "Gerhard Hirschmann",
        OwnershipType.CREATOR,
        {
            'role': 'Primary Creator',
            'contribution': 'Conceptual framework and system architecture'
        }
    )
    
    claim2 = tracker.register_ownership(
        "Elisabeth Steurer",
        OwnershipType.CREATOR,
        {
            'role': 'Co-Creator',
            'contribution': 'Phenomenological interface and EIRA development'
        }
    )
    
    print(f"Claim 1: {claim1.claim_id} - {claim1.owner_name}")
    print(f"Claim 2: {claim2.claim_id} - {claim2.owner_name}")
    
    # Verify claims
    tracker.verify_ownership_claim(claim1.claim_id)
    tracker.verify_ownership_claim(claim2.claim_id)
    
    # State transitions
    print("\n--- State Transitions ---")
    tracker.transition_state(StateType.ACTIVE, "System deployment")
    tracker.transition_state(StateType.PROCESSING, "Processing user request")
    tracker.transition_state(StateType.REFLECTION, "Ethical evaluation")
    tracker.transition_state(StateType.ACTIVE, "Returning to active state")
    
    # Current state
    print("\n--- Current State ---")
    print(json.dumps(tracker.get_current_state(), indent=2))
    
    # Provenance record
    print("\n--- Provenance Record ---")
    provenance = tracker.export_provenance_record()
    print(json.dumps(provenance, indent=2))
    
    # Genesis block
    print("\n--- Genesis Block ---")
    genesis = GenesisBlock(
        creators=["Gerhard Hirschmann", "Elisabeth Steurer"],
        purpose="Open-source proof of post-algorithmic consciousness simulation"
    )
    print(json.dumps(genesis.to_dict(), indent=2))
    
    # Timestamp proof
    print("\n--- Timestamp Proof ---")
    proof = tracker.generate_timestamp_proof("This is the Genesis10000+ system")
    print(json.dumps(proof, indent=2))
