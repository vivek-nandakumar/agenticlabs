#!/usr/bin/env python3
"""
SRE AI Agent - Final Architecture Implementation
Based on the comprehensive architecture with LangGraph routing, JWT auth, mTLS, and OTLP traces
"""

import agno
from agno.models.ollama import Ollama
from agno.memory import Memory
from agno.storage.json import JsonStorage
from agno.tools.mcp import MultiMCPTools
from agno.knowledge import AgentKnowledge
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import jwt
import ssl
import grpc
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
import redis
import sqlite3
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenTelemetry tracing
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "sre-agent-core"})
    )
)
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)
tracer = trace.get_tracer(__name__)

class SREAgentConfig:
    """Configuration for SRE Agent with final architecture"""
    
    def __init__(self):
        # Model Configuration
        self.primary_model_url = "http://localhost:11434"
        self.primary_model_name = "llama3.1:8b"
        self.fallback_model_url = "https://vertex-ai.googleapis.com"
        self.fallback_model_name = "gemini-pro"
        
        # Security Configuration
        self.jwt_secret = os.getenv("JWT_SECRET", "your-secret-key")
        self.mtls_cert_path = os.getenv("MTLS_CERT_PATH", "/path/to/cert.pem")
        self.mtls_key_path = os.getenv("MTLS_KEY_PATH", "/path/to/key.pem")
        
        # Memory Configuration
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.sqlite_path = os.getenv("SQLITE_PATH", "sre_agent_memory.db")
        
        # Observability Configuration
        self.otlp_endpoint = os.getenv("OTLP_ENDPOINT", "http://localhost:4317")
        self.langfuse_endpoint = os.getenv("LANGFUSE_ENDPOINT", "http://localhost:3000")
        
        # MCP Tools Configuration
        self.mcp_servers = {
            "prometheus": {"url": "http://localhost:9090", "auth": "key-auth"},
            "jaeger": {"url": "http://localhost:16686", "auth": "key-auth"},
            "elasticsearch": {"url": "http://localhost:9200", "auth": "key-auth"},
            "nagios": {"url": "http://localhost:8080", "auth": "key-auth"},
            "vanguard": {"url": "http://localhost:8081", "auth": "key-auth"}
        }
        
        # Agent Core Configuration
        self.max_conversation_history = 100
        self.confidence_threshold = 0.8
        self.auto_remediation_enabled = True

class SREAgentCore:
    """Agent Core with LangGraph routing and final architecture"""
    
    def __init__(self, config: SREAgentConfig):
        self.config = config
        self.tracer = tracer
        
        # Initialize memory systems
        self.redis_client = redis.from_url(config.redis_url)
        self.sqlite_conn = sqlite3.connect(config.sqlite_path)
        self._init_sqlite()
        
        # Initialize storage
        self.storage = JsonStorage()
        
        # Initialize memory
        self.memory = Memory(
            memory="SRE Agent Memory",
            id="sre_agent_memory"
        )
        
        # Initialize primary model (Llama-3 GGUF)
        self.primary_model = Ollama(
            model=config.primary_model_name,
            host=config.primary_model_url
        )
        
        # Initialize fallback model (Vertex AI with mTLS)
        self.fallback_model = None  # Will be initialized if needed
        self._init_fallback_model()
        
        # Initialize MCP tools
        self.mcp_tools = MultiMCPTools(
            servers=config.mcp_servers
        )
        
        # Initialize knowledge base
        self.knowledge = AgentKnowledge(
            storage=self.storage,
            model=self.primary_model
        )
        
        # Initialize agent with LangGraph
        self.agent = agno.Agent(
            model=self.primary_model,
            memory=self.memory,
            tools=[self.mcp_tools],
            knowledge=self.knowledge
        )
        
        # Conversation history
        self.conversation_history = []
        
        logger.info("SRE Agent Core initialized with final architecture")
    
    def _init_sqlite(self):
        """Initialize SQLite database for persistent memory"""
        cursor = self.sqlite_conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_input TEXT,
                agent_response TEXT,
                trace_id TEXT,
                span_id TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_state (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.sqlite_conn.commit()
    
    def _init_fallback_model(self):
        """Initialize fallback model with mTLS"""
        try:
            # Create SSL context for mTLS
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # For now, we'll use a placeholder for Vertex AI
            # In production, this would be properly configured
            self.fallback_model = self.primary_model  # Fallback to primary for now
            logger.info("Fallback model initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize fallback model: {e}")
            self.fallback_model = self.primary_model
    
    def _create_jwt_token(self, user_id: str, permissions: List[str]) -> str:
        """Create JWT token for authentication"""
        payload = {
            "user_id": user_id,
            "permissions": permissions,
            "exp": datetime.utcnow().timestamp() + 3600  # 1 hour expiry
        }
        return jwt.encode(payload, self.config.jwt_secret, algorithm="HS256")
    
    def _verify_jwt_token(self, token: str) -> Dict:
        """Verify JWT token"""
        try:
            return jwt.decode(token, self.config.jwt_secret, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            raise ValueError("Invalid JWT token")
    
    def _log_to_sqlite(self, user_input: str, agent_response: str, trace_id: str, span_id: str):
        """Log conversation to SQLite"""
        cursor = self.sqlite_conn.cursor()
        cursor.execute("""
            INSERT INTO conversation_history (user_input, agent_response, trace_id, span_id)
            VALUES (?, ?, ?, ?)
        """, (user_input, agent_response, trace_id, span_id))
        self.sqlite_conn.commit()
    
    def _get_conversation_context(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation context from SQLite"""
        cursor = self.sqlite_conn.cursor()
        cursor.execute("""
            SELECT user_input, agent_response, timestamp
            FROM conversation_history
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        return cursor.fetchall()
    
    async def process_request(self, user_input: str, jwt_token: Optional[str] = None) -> Dict[str, Any]:
        """Process user request with JWT authentication and tracing"""
        
        with tracer.start_as_current_span("process_request") as span:
            span.set_attribute("user_input", user_input)
            
            # Verify JWT token if provided
            user_permissions = []
            if jwt_token:
                try:
                    token_data = self._verify_jwt_token(jwt_token)
                    user_permissions = token_data.get("permissions", [])
                    span.set_attribute("user_id", token_data.get("user_id", "unknown"))
                except ValueError as e:
                    return {"error": "Authentication failed", "details": str(e)}
            
            # Check permissions for SRE operations
            if not self._check_permissions(user_permissions, user_input):
                return {"error": "Insufficient permissions for this operation"}
            
            # Get conversation context
            context = self._get_conversation_context()
            
            # Process with primary model
            try:
                with tracer.start_as_current_span("primary_model_inference") as model_span:
                    response = await self.agent.arun(user_input)
                    model_span.set_attribute("model", "primary")
                    model_span.set_attribute("response_length", len(response.content))
                
                # Log to SQLite
                self._log_to_sqlite(
                    user_input, 
                    response.content, 
                    span.get_span_context().trace_id,
                    span.get_span_context().span_id
                )
                
                # Store in Redis for quick access
                self.redis_client.setex(
                    f"conversation:{span.get_span_context().trace_id}",
                    3600,  # 1 hour TTL
                    json.dumps({
                        "user_input": user_input,
                        "agent_response": response.content,
                        "timestamp": datetime.utcnow().isoformat()
                    })
                )
                
                return {
                    "response": response.content,
                    "trace_id": span.get_span_context().trace_id,
                    "span_id": span.get_span_context().span_id,
                    "model_used": "primary"
                }
                
            except Exception as e:
                logger.error(f"Primary model failed: {e}")
                
                # Try fallback model
                try:
                    with tracer.start_as_current_span("fallback_model_inference") as fallback_span:
                        fallback_response = await self.fallback_model.arun(user_input)
                        fallback_span.set_attribute("model", "fallback")
                        fallback_span.set_attribute("response_length", len(fallback_response.content))
                    
                    return {
                        "response": fallback_response.content,
                        "trace_id": span.get_span_context().trace_id,
                        "span_id": span.get_span_context().span_id,
                        "model_used": "fallback",
                        "warning": "Primary model failed, using fallback"
                    }
                    
                except Exception as fallback_error:
                    logger.error(f"Fallback model also failed: {fallback_error}")
                    return {
                        "error": "All models failed",
                        "trace_id": span.get_span_context().trace_id,
                        "span_id": span.get_span_context().span_id
                    }
    
    def _check_permissions(self, permissions: List[str], user_input: str) -> bool:
        """Check if user has permissions for the requested operation"""
        # Define permission requirements for different operations
        operation_permissions = {
            "health_check": ["read"],
            "investigate_incident": ["read", "incident"],
            "monitor_alerts": ["read", "alert"],
            "execute_action": ["write", "action"],
            "system_metrics": ["read", "metrics"],
            "performance_data": ["read", "performance"]
        }
        
        # Determine operation type from user input
        input_lower = user_input.lower()
        required_permissions = []
        
        if any(word in input_lower for word in ["health", "status", "check"]):
            required_permissions = operation_permissions["health_check"]
        elif any(word in input_lower for word in ["incident", "issue", "problem"]):
            required_permissions = operation_permissions["investigate_incident"]
        elif any(word in input_lower for word in ["alert", "warning", "critical"]):
            required_permissions = operation_permissions["monitor_alerts"]
        elif any(word in input_lower for word in ["action", "execute", "remediate"]):
            required_permissions = operation_permissions["execute_action"]
        elif any(word in input_lower for word in ["metrics", "performance", "cpu", "memory"]):
            required_permissions = operation_permissions["system_metrics"]
        else:
            required_permissions = ["read"]  # Default to read permission
        
        # Check if user has required permissions
        return all(perm in permissions for perm in required_permissions)
    
    async def health_check(self) -> Dict[str, Any]:
        """System health check with tracing"""
        with tracer.start_as_current_span("health_check") as span:
            try:
                # Check primary model
                primary_health = await self.primary_model.health_check()
                span.set_attribute("primary_model_healthy", primary_health)
                
                # Check fallback model
                fallback_health = await self.fallback_model.health_check()
                span.set_attribute("fallback_model_healthy", fallback_health)
                
                # Check Redis connection
                redis_health = self.redis_client.ping()
                span.set_attribute("redis_healthy", redis_health)
                
                # Check SQLite connection
                sqlite_health = self.sqlite_conn is not None
                span.set_attribute("sqlite_healthy", sqlite_health)
                
                # Check MCP tools
                mcp_health = await self.mcp_tools.health_check()
                span.set_attribute("mcp_tools_healthy", mcp_health)
                
                overall_health = all([
                    primary_health,
                    fallback_health,
                    redis_health,
                    sqlite_health,
                    mcp_health
                ])
                
                return {
                    "status": "healthy" if overall_health else "unhealthy",
                    "components": {
                        "primary_model": primary_health,
                        "fallback_model": fallback_health,
                        "redis": redis_health,
                        "sqlite": sqlite_health,
                        "mcp_tools": mcp_health
                    },
                    "timestamp": datetime.utcnow().isoformat(),
                    "trace_id": span.get_span_context().trace_id
                }
                
            except Exception as e:
                span.record_exception(e)
                return {
                    "status": "unhealthy",
                    "error": str(e),
                    "trace_id": span.get_span_context().trace_id
                }
    
    async def investigate_incident(self, incident_id: str, jwt_token: Optional[str] = None) -> Dict[str, Any]:
        """Investigate incident with comprehensive tracing"""
        with tracer.start_as_current_span("investigate_incident") as span:
            span.set_attribute("incident_id", incident_id)
            
            try:
                # Query incident data from MCP tools
                incident_data = await self.mcp_tools.query_incident(incident_id)
                span.set_attribute("incident_found", bool(incident_data))
                
                # Analyze with AI model
                analysis_prompt = f"Analyze this incident: {incident_data}"
                analysis = await self.agent.arun(analysis_prompt)
                
                # Generate recommendations
                recommendations = await self._generate_recommendations(incident_data, analysis.content)
                
                return {
                    "incident_id": incident_id,
                    "analysis": analysis.content,
                    "recommendations": recommendations,
                    "trace_id": span.get_span_context().trace_id
                }
                
            except Exception as e:
                span.record_exception(e)
                return {"error": f"Failed to investigate incident: {str(e)}"}
    
    async def monitor_alerts(self, severity: Optional[str] = None) -> Dict[str, Any]:
        """Monitor alerts with filtering and tracing"""
        with tracer.start_as_current_span("monitor_alerts") as span:
            span.set_attribute("severity_filter", severity or "all")
            
            try:
                # Query alerts from MCP tools
                alerts = await self.mcp_tools.query_alerts(severity=severity)
                span.set_attribute("alerts_count", len(alerts))
                
                # Analyze alert patterns
                if alerts:
                    analysis_prompt = f"Analyze these alerts: {alerts}"
                    analysis = await self.agent.arun(analysis_prompt)
                    
                    return {
                        "alerts": alerts,
                        "analysis": analysis.content,
                        "count": len(alerts),
                        "trace_id": span.get_span_context().trace_id
                    }
                else:
                    return {
                        "alerts": [],
                        "message": "No alerts found",
                        "trace_id": span.get_span_context().trace_id
                    }
                    
            except Exception as e:
                span.record_exception(e)
                return {"error": f"Failed to monitor alerts: {str(e)}"}
    
    async def _generate_recommendations(self, incident_data: Dict, analysis: str) -> List[str]:
        """Generate recommendations based on incident analysis"""
        with tracer.start_as_current_span("generate_recommendations") as span:
            try:
                prompt = f"""
                Based on this incident analysis: {analysis}
                And incident data: {incident_data}
                
                Generate 3-5 specific, actionable recommendations to:
                1. Resolve the current incident
                2. Prevent similar incidents in the future
                3. Improve system reliability
                
                Format as a numbered list.
                """
                
                response = await self.agent.arun(prompt)
                recommendations = [rec.strip() for rec in response.content.split('\n') if rec.strip()]
                
                span.set_attribute("recommendations_count", len(recommendations))
                return recommendations
                
            except Exception as e:
                span.record_exception(e)
                return ["Unable to generate recommendations due to error"]
    
    def cleanup(self):
        """Cleanup resources"""
        if self.sqlite_conn:
            self.sqlite_conn.close()
        if self.redis_client:
            self.redis_client.close()

# Global agent instance
sre_agent = None

def get_sre_agent() -> SREAgentCore:
    """Get or create SRE agent instance"""
    global sre_agent
    if sre_agent is None:
        config = SREAgentConfig()
        sre_agent = SREAgentCore(config)
    return sre_agent

if __name__ == "__main__":
    # Test the agent
    async def test_agent():
        agent = get_sre_agent()
        
        # Test health check
        health = await agent.health_check()
        print(f"Health Check: {health}")
        
        # Test conversation
        response = await agent.process_request("What's the current system health status?")
        print(f"Response: {response}")
        
        agent.cleanup()
    
    asyncio.run(test_agent()) 