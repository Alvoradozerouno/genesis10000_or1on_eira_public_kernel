"""
AuditChain - Blockchain-based Audit Trail System
Provides immutable audit logging for all kernel operations
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib
import json

logger = logging.getLogger(__name__)


class Block:
    """Individual block in the audit chain"""
    
    def __init__(self, index: int, timestamp: str, data: Dict[str, Any], 
                 previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate block hash"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }


class AuditChain:
    """
    Blockchain-based audit trail for complete transparency
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.chain: List[Block] = []
        self.pending_events: List[Dict[str, Any]] = []
        
    def initialize(self):
        """Initialize the AuditChain with genesis block"""
        logger.info("Initializing AuditChain")
        
        # Create genesis block
        genesis_block = Block(
            index=0,
            timestamp=datetime.utcnow().isoformat(),
            data={'event': 'GENESIS', 'message': 'AuditChain initialized'},
            previous_hash='0'
        )
        self.chain.append(genesis_block)
        
    def log_event(self, event_type: str, data: Dict[str, Any]) -> str:
        """
        Log an event to the audit chain
        
        Args:
            event_type: Type of event
            data: Event data
            
        Returns:
            str: Event ID (hash)
        """
        event = {
            'type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data
        }
        
        # Add to pending events
        self.pending_events.append(event)
        
        # Create new block
        block = self._create_block(event)
        self.chain.append(block)
        
        logger.debug(f"Event logged: {event_type} (block {block.index})")
        
        return block.hash
    
    def _create_block(self, data: Dict[str, Any]) -> Block:
        """Create a new block"""
        previous_block = self.chain[-1] if self.chain else None
        previous_hash = previous_block.hash if previous_block else '0'
        
        return Block(
            index=len(self.chain),
            timestamp=datetime.utcnow().isoformat(),
            data=data,
            previous_hash=previous_hash
        )
    
    def verify_chain(self) -> bool:
        """
        Verify the integrity of the audit chain
        
        Returns:
            bool: True if chain is valid
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify hash
            if current_block.hash != current_block.calculate_hash():
                logger.error(f"Block {i} hash mismatch")
                return False
            
            # Verify chain linkage
            if current_block.previous_hash != previous_block.hash:
                logger.error(f"Block {i} chain linkage broken")
                return False
        
        return True
    
    def get_events(self, event_type: Optional[str] = None, 
                   limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve events from the chain
        
        Args:
            event_type: Filter by event type (optional)
            limit: Maximum number of events to return
            
        Returns:
            List of events
        """
        events = []
        
        for block in reversed(self.chain):
            if len(events) >= limit:
                break
            
            block_data = block.data
            if event_type is None or block_data.get('type') == event_type:
                events.append({
                    'block_index': block.index,
                    'block_hash': block.hash,
                    'timestamp': block.timestamp,
                    **block_data
                })
        
        return events
    
    def hash_data(self, data: Any) -> str:
        """Hash arbitrary data"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def export_chain(self) -> List[Dict[str, Any]]:
        """Export entire chain"""
        return [block.to_dict() for block in self.chain]
    
    def get_status(self) -> Dict[str, Any]:
        """Get AuditChain status"""
        return {
            "active": True,
            "chain_length": len(self.chain),
            "chain_valid": self.verify_chain(),
            "pending_events": len(self.pending_events),
            "latest_block_hash": self.chain[-1].hash if self.chain else None
        }
    
    def shutdown(self):
        """Shutdown AuditChain"""
        logger.info("Shutting down AuditChain")
        # Final integrity check
        if not self.verify_chain():
            logger.warning("Chain integrity compromised at shutdown")
