"""
Ownership Proof System
Complete ownership verification and proof management
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib
import json
import uuid

logger = logging.getLogger(__name__)


class OwnershipProof:
    """Represents an ownership proof"""
    
    def __init__(self, owner_id: str, asset_id: str, proof_data: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.owner_id = owner_id
        self.asset_id = asset_id
        self.proof_data = proof_data
        self.timestamp = datetime.utcnow().isoformat()
        self.signature = self._generate_signature()
        
    def _generate_signature(self) -> str:
        """Generate cryptographic signature for the proof"""
        proof_string = json.dumps({
            'id': self.id,
            'owner_id': self.owner_id,
            'asset_id': self.asset_id,
            'proof_data': self.proof_data,
            'timestamp': self.timestamp
        }, sort_keys=True)
        
        return hashlib.sha256(proof_string.encode()).hexdigest()
    
    def verify(self) -> bool:
        """Verify proof integrity"""
        expected_signature = self._generate_signature()
        return self.signature == expected_signature
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'asset_id': self.asset_id,
            'proof_data': self.proof_data,
            'timestamp': self.timestamp,
            'signature': self.signature
        }


class OwnershipProofSystem:
    """
    Complete ownership verification and proof management system
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.proofs = {}
        self.ownership_registry = {}
        self.verification_history = []
        self.system_state = "uninitialized"
        
    def initialize(self):
        """Initialize ownership proof system"""
        logger.info("Initializing Ownership Proof System")
        self.system_state = "active"
        
        # Register kernel ownership
        self._register_ownership("kernel", "genesis10000_or1on_eira_kernel", {
            "type": "core_system",
            "created": datetime.utcnow().isoformat()
        })
        
    def create_proof(self, owner_id: str, asset_id: str, 
                     proof_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an ownership proof
        
        Args:
            owner_id: Owner identifier
            asset_id: Asset identifier
            proof_data: Proof data
            
        Returns:
            Created proof
        """
        proof = OwnershipProof(owner_id, asset_id, proof_data)
        
        # Store proof
        self.proofs[proof.id] = proof
        
        # Update registry
        if asset_id not in self.ownership_registry:
            self.ownership_registry[asset_id] = []
        
        self.ownership_registry[asset_id].append({
            'proof_id': proof.id,
            'owner_id': owner_id,
            'timestamp': proof.timestamp
        })
        
        logger.info(f"Created ownership proof: {proof.id}")
        
        return proof.to_dict()
    
    def verify(self, proof_data: Optional[Dict[str, Any]]) -> bool:
        """
        Verify an ownership proof
        
        Args:
            proof_data: Proof to verify
            
        Returns:
            bool: True if proof is valid
        """
        if not proof_data:
            return False
        
        proof_id = proof_data.get('id')
        
        if not proof_id or proof_id not in self.proofs:
            logger.warning(f"Proof not found: {proof_id}")
            self._log_verification(proof_id, False, "proof_not_found")
            return False
        
        proof = self.proofs[proof_id]
        
        # Verify signature
        if not proof.verify():
            logger.warning(f"Proof signature invalid: {proof_id}")
            self._log_verification(proof_id, False, "invalid_signature")
            return False
        
        # Verify ownership chain
        if not self._verify_ownership_chain(proof):
            logger.warning(f"Ownership chain invalid: {proof_id}")
            self._log_verification(proof_id, False, "invalid_chain")
            return False
        
        self._log_verification(proof_id, True, "verified")
        
        return True
    
    def _verify_ownership_chain(self, proof: OwnershipProof) -> bool:
        """Verify the ownership chain is valid"""
        # Check if asset exists in registry
        if proof.asset_id not in self.ownership_registry:
            return False
        
        # Check if proof is in the ownership chain
        for entry in self.ownership_registry[proof.asset_id]:
            if entry['proof_id'] == proof.id:
                return True
        
        return False
    
    def _register_ownership(self, owner_id: str, asset_id: str, 
                           metadata: Dict[str, Any]):
        """Register initial ownership"""
        proof_data = {
            "registration": True,
            "metadata": metadata
        }
        
        self.create_proof(owner_id, asset_id, proof_data)
    
    def _log_verification(self, proof_id: Optional[str], result: bool, 
                         reason: str):
        """Log verification attempt"""
        verification_record = {
            'proof_id': proof_id,
            'result': result,
            'reason': reason,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.verification_history.append(verification_record)
        
        # Keep only recent history
        if len(self.verification_history) > 1000:
            self.verification_history = self.verification_history[-1000:]
    
    def get_ownership(self, asset_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get ownership information for an asset
        
        Args:
            asset_id: Asset identifier
            
        Returns:
            Ownership information
        """
        if asset_id not in self.ownership_registry:
            return None
        
        ownership_chain = []
        for entry in self.ownership_registry[asset_id]:
            proof_id = entry['proof_id']
            if proof_id in self.proofs:
                proof = self.proofs[proof_id]
                ownership_chain.append(proof.to_dict())
        
        return ownership_chain
    
    def transfer_ownership(self, asset_id: str, from_owner: str, 
                          to_owner: str, proof_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transfer ownership of an asset
        
        Args:
            asset_id: Asset identifier
            from_owner: Current owner
            to_owner: New owner
            proof_data: Transfer proof data
            
        Returns:
            Transfer result
        """
        # Verify current ownership
        current_ownership = self.get_ownership(asset_id)
        if not current_ownership:
            return {"error": "Asset not found"}
        
        # Verify from_owner is current owner
        latest_owner = current_ownership[-1]['owner_id']
        if latest_owner != from_owner:
            return {"error": "Ownership verification failed"}
        
        # Create transfer proof
        transfer_proof_data = {
            "transfer": True,
            "from_owner": from_owner,
            "to_owner": to_owner,
            **proof_data
        }
        
        new_proof = self.create_proof(to_owner, asset_id, transfer_proof_data)
        
        logger.info(f"Ownership transferred: {asset_id} from {from_owner} to {to_owner}")
        
        return {
            "success": True,
            "transfer_proof": new_proof,
            "asset_id": asset_id,
            "new_owner": to_owner
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get ownership system status"""
        return {
            "active": True,
            "system_state": self.system_state,
            "total_proofs": len(self.proofs),
            "registered_assets": len(self.ownership_registry),
            "verifications_performed": len(self.verification_history),
            "successful_verifications": sum(1 for v in self.verification_history if v['result'])
        }
    
    def shutdown(self):
        """Shutdown ownership system"""
        logger.info("Shutting down Ownership Proof System")
        self.system_state = "shutdown"
