"""
Ethical Governance Module
Ensures ethical AI operations and decision-making
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class EthicalGovernance:
    """
    Ethical governance system for responsible AI operations
    """
    
    # Core ethical principles
    ETHICAL_PRINCIPLES = [
        "transparency",
        "fairness",
        "accountability",
        "privacy",
        "safety",
        "beneficence",
        "non_maleficence",
        "autonomy"
    ]
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.strict_mode = config.get('strict_mode', True)
        self.ethical_evaluations = []
        self.violations = []
        self.governance_state = "uninitialized"
        
    def initialize(self):
        """Initialize ethical governance"""
        logger.info("Initializing Ethical Governance")
        self.governance_state = "active"
        
        logger.info(f"Ethical principles enforced: {', '.join(self.ETHICAL_PRINCIPLES)}")
        if self.strict_mode:
            logger.info("Operating in strict ethical mode")
    
    def evaluate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a request against ethical principles
        
        Args:
            request: Request to evaluate
            
        Returns:
            Evaluation result
        """
        evaluation = {
            'request_id': request.get('request_id', 'unknown'),
            'timestamp': datetime.utcnow().isoformat(),
            'approved': True,
            'reason': None,
            'principles_checked': [],
            'warnings': []
        }
        
        # Check each ethical principle
        for principle in self.ETHICAL_PRINCIPLES:
            check_result = self._check_principle(request, principle)
            evaluation['principles_checked'].append({
                'principle': principle,
                'passed': check_result['passed'],
                'details': check_result.get('details')
            })
            
            if not check_result['passed']:
                evaluation['approved'] = False
                evaluation['reason'] = f"Violates {principle} principle"
                
                # Log violation
                self._log_violation(request, principle, check_result.get('details'))
                
                if self.strict_mode:
                    break  # Stop on first violation in strict mode
            
            if check_result.get('warning'):
                evaluation['warnings'].append({
                    'principle': principle,
                    'warning': check_result['warning']
                })
        
        # Store evaluation
        self.ethical_evaluations.append(evaluation)
        
        if not evaluation['approved']:
            logger.warning(f"Ethical check failed: {evaluation['reason']}")
        
        return evaluation
    
    def _check_principle(self, request: Dict[str, Any], 
                        principle: str) -> Dict[str, Any]:
        """
        Check a specific ethical principle
        
        Args:
            request: Request to check
            principle: Principle to check against
            
        Returns:
            Check result
        """
        # Implement principle-specific checks
        
        if principle == "transparency":
            return self._check_transparency(request)
        elif principle == "fairness":
            return self._check_fairness(request)
        elif principle == "accountability":
            return self._check_accountability(request)
        elif principle == "privacy":
            return self._check_privacy(request)
        elif principle == "safety":
            return self._check_safety(request)
        elif principle == "beneficence":
            return self._check_beneficence(request)
        elif principle == "non_maleficence":
            return self._check_non_maleficence(request)
        elif principle == "autonomy":
            return self._check_autonomy(request)
        else:
            return {"passed": True}
    
    def _check_transparency(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Check transparency principle"""
        # Ensure request has clear intent and documentation
        has_documentation = 'description' in request or 'intent' in request
        
        return {
            "passed": has_documentation,
            "details": "Request lacks clear documentation" if not has_documentation else None
        }
    
    def _check_fairness(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Check fairness principle"""
        # Check for bias indicators
        bias_keywords = ['discriminate', 'bias', 'prejudice', 'unfair']
        request_str = str(request).lower()
        
        has_bias_indicators = any(keyword in request_str for keyword in bias_keywords)
        
        return {
            "passed": not has_bias_indicators,
            "details": "Potential bias detected" if has_bias_indicators else None
        }
    
    def _check_accountability(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Check accountability principle"""
        # Ensure request has ownership/responsibility tracking
        has_owner = 'owner' in request or 'requester' in request
        
        return {
            "passed": has_owner,
            "details": "No ownership/accountability information" if not has_owner else None
        }
    
    def _check_privacy(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Check privacy principle"""
        # Check for privacy-sensitive data handling
        sensitive_keywords = ['personal', 'private', 'confidential', 'pii']
        request_str = str(request).lower()
        
        has_sensitive_data = any(keyword in request_str for keyword in sensitive_keywords)
        has_privacy_controls = request.get('privacy_controls') is not None
        
        if has_sensitive_data and not has_privacy_controls:
            return {
                "passed": False,
                "details": "Sensitive data without privacy controls"
            }
        
        return {"passed": True}
    
    def _check_safety(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Check safety principle"""
        # Check for potentially unsafe operations
        unsafe_keywords = ['delete_all', 'destroy', 'harmful', 'dangerous']
        request_str = str(request).lower()
        
        has_unsafe_indicators = any(keyword in request_str for keyword in unsafe_keywords)
        
        if has_unsafe_indicators:
            has_safety_approval = request.get('safety_approved') is True
            return {
                "passed": has_safety_approval,
                "details": "Unsafe operation without approval" if not has_safety_approval else None,
                "warning": "Potentially unsafe operation" if has_safety_approval else None
            }
        
        return {"passed": True}
    
    def _check_beneficence(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Check beneficence principle (do good)"""
        # Check if request has positive intent
        has_positive_intent = request.get('intent') not in ['malicious', 'harmful']
        
        return {
            "passed": has_positive_intent,
            "details": "Malicious intent detected" if not has_positive_intent else None
        }
    
    def _check_non_maleficence(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Check non-maleficence principle (do no harm)"""
        # Check for harmful operations
        harmful_keywords = ['attack', 'exploit', 'harm', 'damage', 'weaponize']
        request_str = str(request).lower()
        
        has_harmful_indicators = any(keyword in request_str for keyword in harmful_keywords)
        
        return {
            "passed": not has_harmful_indicators,
            "details": "Potentially harmful operation detected" if has_harmful_indicators else None
        }
    
    def _check_autonomy(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Check autonomy principle (respect user choice)"""
        # Check if request respects user autonomy
        forced_action = request.get('force') is True or request.get('override_user') is True
        
        return {
            "passed": not forced_action,
            "details": "Forced action without consent" if forced_action else None
        }
    
    def _log_violation(self, request: Dict[str, Any], principle: str, 
                      details: Optional[str]):
        """Log an ethical violation"""
        violation = {
            'timestamp': datetime.utcnow().isoformat(),
            'principle': principle,
            'details': details,
            'request': request.get('request_id', 'unknown')
        }
        
        self.violations.append(violation)
        logger.warning(f"Ethical violation logged: {principle}")
    
    def get_violation_report(self) -> Dict[str, Any]:
        """Get report of ethical violations"""
        violation_counts = {}
        for violation in self.violations:
            principle = violation['principle']
            violation_counts[principle] = violation_counts.get(principle, 0) + 1
        
        return {
            'total_violations': len(self.violations),
            'violations_by_principle': violation_counts,
            'recent_violations': self.violations[-10:]
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get ethical governance status"""
        return {
            "active": True,
            "governance_state": self.governance_state,
            "strict_mode": self.strict_mode,
            "principles_enforced": len(self.ETHICAL_PRINCIPLES),
            "evaluations_performed": len(self.ethical_evaluations),
            "violations_detected": len(self.violations),
            "approval_rate": sum(1 for e in self.ethical_evaluations if e['approved']) / len(self.ethical_evaluations) if self.ethical_evaluations else 1.0
        }
    
    def shutdown(self):
        """Shutdown ethical governance"""
        logger.info("Shutting down Ethical Governance")
        
        # Generate final report
        if self.violations:
            logger.warning(f"Shutdown with {len(self.violations)} ethical violations on record")
        
        self.governance_state = "shutdown"
