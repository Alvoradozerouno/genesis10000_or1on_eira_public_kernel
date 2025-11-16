"""
EIRA Communication Structure
Advanced communication and networking infrastructure
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class Message:
    """Communication message"""
    
    def __init__(self, sender: str, recipient: str, content: Any, 
                 message_type: str = "standard"):
        self.id = str(uuid.uuid4())
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.message_type = message_type
        self.timestamp = datetime.utcnow().isoformat()
        self.delivered = False
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'sender': self.sender,
            'recipient': self.recipient,
            'content': self.content,
            'type': self.message_type,
            'timestamp': self.timestamp,
            'delivered': self.delivered
        }


class EIRACommunication:
    """
    EIRA (Enhanced Intelligent Relay Architecture) Communication Structure
    Advanced networking and communication infrastructure
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.nodes = {}
        self.message_queue = []
        self.delivered_messages = []
        self.network_state = "offline"
        self.protocols = ['EIRA-1', 'EIRA-2', 'Quantum-Secure']
        
    def initialize(self):
        """Initialize EIRA communication structure"""
        logger.info("Initializing EIRA Communication Structure")
        self.network_state = "online"
        
        # Register local node
        self._register_node("kernel_core", "local")
        
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a communication request
        
        Args:
            request: Request data
            
        Returns:
            Response data
        """
        operation = request.get('communication_op', 'send')
        
        if operation == 'send':
            return self._send_message(request)
        elif operation == 'receive':
            return self._receive_messages(request.get('node_id'))
        elif operation == 'broadcast':
            return self._broadcast(request.get('content'))
        elif operation == 'establish_channel':
            return self._establish_channel(request.get('channel_config', {}))
        else:
            return {"error": "Unknown communication operation"}
    
    def _register_node(self, node_id: str, node_type: str) -> Dict[str, Any]:
        """Register a communication node"""
        node = {
            "id": node_id,
            "type": node_type,
            "registered": datetime.utcnow().isoformat(),
            "status": "active",
            "messages_sent": 0,
            "messages_received": 0
        }
        
        self.nodes[node_id] = node
        
        logger.info(f"Registered node: {node_id}")
        
        return node
    
    def _send_message(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a message
        
        Args:
            request: Message request
            
        Returns:
            Send result
        """
        sender = request.get('sender', 'unknown')
        recipient = request.get('recipient', 'broadcast')
        content = request.get('content', {})
        message_type = request.get('message_type', 'standard')
        
        # Create message
        message = Message(sender, recipient, content, message_type)
        
        # Add to queue
        self.message_queue.append(message)
        
        # Update sender stats
        if sender in self.nodes:
            self.nodes[sender]['messages_sent'] += 1
        
        # Attempt delivery
        delivered = self._deliver_message(message)
        
        result = {
            "message_id": message.id,
            "status": "delivered" if delivered else "queued",
            "timestamp": message.timestamp
        }
        
        logger.info(f"Message sent: {message.id} ({result['status']})")
        
        return result
    
    def _deliver_message(self, message: Message) -> bool:
        """Deliver a message to recipient"""
        recipient = message.recipient
        
        if recipient == 'broadcast':
            # Broadcast to all nodes
            for node_id in self.nodes:
                if node_id != message.sender:
                    self.nodes[node_id]['messages_received'] += 1
            message.delivered = True
            self.delivered_messages.append(message)
            return True
        
        elif recipient in self.nodes:
            # Direct delivery
            self.nodes[recipient]['messages_received'] += 1
            message.delivered = True
            self.delivered_messages.append(message)
            return True
        
        return False
    
    def _receive_messages(self, node_id: str) -> Dict[str, Any]:
        """
        Receive messages for a node
        
        Args:
            node_id: Node identifier
            
        Returns:
            Messages for the node
        """
        messages = []
        
        for msg in self.delivered_messages:
            if msg.recipient == node_id or msg.recipient == 'broadcast':
                messages.append(msg.to_dict())
        
        return {
            "node_id": node_id,
            "message_count": len(messages),
            "messages": messages[-10:]  # Last 10 messages
        }
    
    def _broadcast(self, content: Any) -> Dict[str, Any]:
        """
        Broadcast message to all nodes
        
        Args:
            content: Content to broadcast
            
        Returns:
            Broadcast result
        """
        message = Message("kernel_core", "broadcast", content, "broadcast")
        self.message_queue.append(message)
        self._deliver_message(message)
        
        return {
            "broadcast_id": message.id,
            "recipients": len(self.nodes),
            "timestamp": message.timestamp
        }
    
    def _establish_channel(self, channel_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Establish a communication channel
        
        Args:
            channel_config: Channel configuration
            
        Returns:
            Channel details
        """
        channel_id = str(uuid.uuid4())
        
        channel = {
            "id": channel_id,
            "type": channel_config.get('type', 'standard'),
            "protocol": channel_config.get('protocol', 'EIRA-1'),
            "encryption": channel_config.get('encryption', 'quantum-secure'),
            "established": datetime.utcnow().isoformat(),
            "status": "active"
        }
        
        logger.info(f"Established channel: {channel_id}")
        
        return channel
    
    def get_network_topology(self) -> Dict[str, Any]:
        """Get current network topology"""
        return {
            "nodes": len(self.nodes),
            "node_list": list(self.nodes.keys()),
            "message_queue_size": len(self.message_queue),
            "delivered_messages": len(self.delivered_messages),
            "network_state": self.network_state
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get EIRA communication status"""
        return {
            "active": True,
            "network_state": self.network_state,
            "registered_nodes": len(self.nodes),
            "queued_messages": len(self.message_queue),
            "delivered_messages": len(self.delivered_messages),
            "protocols": self.protocols
        }
    
    def shutdown(self):
        """Shutdown EIRA communication"""
        logger.info("Shutting down EIRA Communication")
        
        # Flush message queue
        if self.message_queue:
            logger.warning(f"Shutting down with {len(self.message_queue)} undelivered messages")
        
        self.network_state = "offline"
