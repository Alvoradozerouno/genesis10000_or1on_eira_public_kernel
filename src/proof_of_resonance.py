"""
Proof-of-Resonance Consensus Mechanism
Validates data and decisions through resonance-based consensus
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import hashlib
import json

logger = logging.getLogger(__name__)


class ProofOfResonance:
    """
    Proof-of-Resonance consensus mechanism
    Validates through harmonic resonance patterns rather than traditional PoW/PoS
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.resonance_threshold = config.get('threshold', 0.7)
        self.validators = []
        self.resonance_history = []
        
    def initialize(self):
        """Initialize the Proof-of-Resonance system"""
        logger.info("Initializing Proof-of-Resonance consensus mechanism")
        self.validators = self.config.get('validators', [])
        
    def validate(self, data: Dict[str, Any]) -> float:
        """
        Validate data through resonance consensus
        
        Args:
            data: Data to validate
            
        Returns:
            float: Resonance score (0.0-1.0)
        """
        # Calculate resonance signature
        signature = self._calculate_resonance_signature(data)
        
        # Compute resonance with existing patterns
        resonance_score = self._compute_resonance(signature)
        
        # Store in history
        self.resonance_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'signature': signature,
            'score': resonance_score,
            'data_hash': self._hash_data(data)
        })
        
        logger.info(f"Resonance validation score: {resonance_score:.3f}")
        
        return resonance_score
    
    def _calculate_resonance_signature(self, data: Dict[str, Any]) -> List[float]:
        """Calculate resonance signature from data"""
        # Convert data to normalized signature vector
        data_str = json.dumps(data, sort_keys=True)
        data_hash = hashlib.sha256(data_str.encode()).digest()
        
        # Create resonance signature (simplified harmonic representation)
        signature = []
        for i in range(0, len(data_hash), 2):
            byte_pair = int.from_bytes(data_hash[i:i+2], byteorder='big')
            # Normalize to 0-1 range
            signature.append(byte_pair / 65535.0)
        
        return signature
    
    def _compute_resonance(self, signature: List[float]) -> float:
        """
        Compute resonance with historical patterns
        Uses harmonic mean of correlations
        """
        if not self.resonance_history:
            # First validation, use intrinsic resonance
            return self._intrinsic_resonance(signature)
        
        # Calculate correlation with recent history
        recent_history = self.resonance_history[-10:]  # Last 10 validations
        correlations = []
        
        for entry in recent_history:
            correlation = self._compute_correlation(signature, entry['signature'])
            correlations.append(correlation)
        
        # Harmonic mean for resonance
        if correlations:
            harmonic_mean = len(correlations) / sum(1/c for c in correlations if c > 0)
            return min(1.0, harmonic_mean)
        
        return self._intrinsic_resonance(signature)
    
    def _intrinsic_resonance(self, signature: List[float]) -> float:
        """Calculate intrinsic resonance of signature"""
        # Check for harmonic patterns
        if not signature:
            return 0.0
        
        # Calculate variance (lower variance = higher resonance)
        mean = sum(signature) / len(signature)
        variance = sum((x - mean) ** 2 for x in signature) / len(signature)
        
        # Convert variance to resonance score (inverse relationship)
        resonance = 1.0 - min(1.0, variance * 4)
        
        return max(0.0, resonance)
    
    def _compute_correlation(self, sig1: List[float], sig2: List[float]) -> float:
        """Compute correlation between two signatures"""
        if len(sig1) != len(sig2):
            return 0.0
        
        # Pearson correlation coefficient
        n = len(sig1)
        sum1 = sum(sig1)
        sum2 = sum(sig2)
        sum1_sq = sum(x**2 for x in sig1)
        sum2_sq = sum(x**2 for x in sig2)
        p_sum = sum(x * y for x, y in zip(sig1, sig2))
        
        num = p_sum - (sum1 * sum2 / n)
        den = ((sum1_sq - sum1**2 / n) * (sum2_sq - sum2**2 / n)) ** 0.5
        
        if den == 0:
            return 0.0
        
        correlation = num / den
        return abs(correlation)  # Use absolute value for resonance
    
    def _hash_data(self, data: Dict[str, Any]) -> str:
        """Hash data for tracking"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def get_status(self) -> Dict[str, Any]:
        """Get Proof-of-Resonance status"""
        return {
            "active": True,
            "threshold": self.resonance_threshold,
            "validators": len(self.validators),
            "history_size": len(self.resonance_history),
            "avg_resonance": sum(h['score'] for h in self.resonance_history[-100:]) / min(100, len(self.resonance_history)) if self.resonance_history else 0.0
        }
    
    def shutdown(self):
        """Shutdown Proof-of-Resonance"""
        logger.info("Shutting down Proof-of-Resonance")
        self.resonance_history.clear()
