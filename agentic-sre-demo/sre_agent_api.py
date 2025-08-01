#!/usr/bin/env python3
"""
SRE Agent REST API - Final Architecture Implementation
Based on the comprehensive architecture with JWT auth, mTLS, and OTLP traces
"""

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
import jwt
import ssl
import logging
from datetime import datetime, timedelta
import os
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Import the updated SRE agent
from sre_agent import get_sre_agent, SREAgentCore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenTelemetry tracing
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "sre-agent-api"})
    )
)
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)
tracer = trace.get_tracer(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SRE AI Agent API",
    description="REST API for SRE AI Agent with final architecture",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

# Security configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security schemas
security = HTTPBearer()

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    trace_id: str
    span_id: str
    model_used: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    components: Dict[str, bool]
    timestamp: str
    trace_id: str

class IncidentRequest(BaseModel):
    incident_id: str
    description: Optional[str] = None

class AlertRequest(BaseModel):
    severity: Optional[str] = None
    service: Optional[str] = None

class AuthRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

# JWT token management
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# Mock user database (in production, use real database)
USERS_DB = {
    "admin": {
        "username": "admin",
        "password": "admin123",  # In production, use hashed passwords
        "permissions": ["read", "write", "incident", "alert", "action", "metrics", "performance"]
    },
    "sre_engineer": {
        "username": "sre_engineer",
        "password": "sre123",
        "permissions": ["read", "incident", "alert", "metrics", "performance"]
    },
    "viewer": {
        "username": "viewer",
        "password": "view123",
        "permissions": ["read"]
    }
}

# Global SRE agent instance
sre_agent: Optional[SREAgentCore] = None

@app.on_event("startup")
async def startup_event():
    """Initialize the SRE agent on startup"""
    global sre_agent
    try:
        sre_agent = get_sre_agent()
        logger.info("SRE Agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize SRE Agent: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global sre_agent
    if sre_agent:
        sre_agent.cleanup()
        logger.info("SRE Agent cleaned up")

# Authentication endpoints
@app.post("/auth/login", response_model=AuthResponse)
async def login(auth_request: AuthRequest):
    """Login endpoint with JWT token generation"""
    with tracer.start_as_current_span("login") as span:
        span.set_attribute("username", auth_request.username)
        
        user = USERS_DB.get(auth_request.username)
        if not user or user["password"] != auth_request.password:
            span.set_attribute("login_success", False)
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["username"], "permissions": user["permissions"]},
            expires_delta=access_token_expires
        )
        
        span.set_attribute("login_success", True)
        span.set_attribute("user_permissions", str(user["permissions"]))
        
        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

@app.post("/auth/verify")
async def verify_auth(token_data: Dict[str, Any] = Depends(verify_token)):
    """Verify authentication token"""
    with tracer.start_as_current_span("verify_auth") as span:
        span.set_attribute("user_id", token_data.get("sub", "unknown"))
        span.set_attribute("permissions", str(token_data.get("permissions", [])))
        
        return {
            "valid": True,
            "user_id": token_data.get("sub"),
            "permissions": token_data.get("permissions", []),
            "expires_at": token_data.get("exp")
        }

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """System health check with comprehensive component status"""
    with tracer.start_as_current_span("api_health_check") as span:
        try:
            if not sre_agent:
                raise HTTPException(status_code=503, detail="SRE Agent not initialized")
            
            health_result = await sre_agent.health_check()
            
            span.set_attribute("health_status", health_result.get("status", "unknown"))
            span.set_attribute("components_healthy", str(health_result.get("components", {})))
            
            return HealthResponse(
                status=health_result.get("status", "unknown"),
                components=health_result.get("components", {}),
                timestamp=health_result.get("timestamp", datetime.utcnow().isoformat()),
                trace_id=health_result.get("trace_id", span.get_span_context().trace_id)
            )
            
        except Exception as e:
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# Chat endpoint with JWT authentication
@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    token_data: Dict[str, Any] = Depends(verify_token)
):
    """Chat with the SRE agent using natural language"""
    with tracer.start_as_current_span("chat_with_agent") as span:
        span.set_attribute("user_id", token_data.get("sub", "unknown"))
        span.set_attribute("message_length", len(request.message))
        
        try:
            if not sre_agent:
                raise HTTPException(status_code=503, detail="SRE Agent not initialized")
            
            # Create JWT token for agent authentication
            jwt_token = create_access_token(
                data={"sub": token_data.get("sub"), "permissions": token_data.get("permissions", [])}
            )
            
            # Process request with agent
            result = await sre_agent.process_request(request.message, jwt_token)
            
            if "error" in result:
                span.set_attribute("chat_success", False)
                span.set_attribute("error", result["error"])
                raise HTTPException(status_code=400, detail=result["error"])
            
            span.set_attribute("chat_success", True)
            span.set_attribute("model_used", result.get("model_used", "unknown"))
            
            return ChatResponse(
                response=result["response"],
                trace_id=result["trace_id"],
                span_id=result["span_id"],
                model_used=result.get("model_used", "primary"),
                timestamp=datetime.utcnow().isoformat()
            )
            
        except Exception as e:
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

# Incident investigation endpoint
@app.post("/incidents/investigate")
async def investigate_incident(
    request: IncidentRequest,
    token_data: Dict[str, Any] = Depends(verify_token)
):
    """Investigate a specific incident"""
    with tracer.start_as_current_span("investigate_incident") as span:
        span.set_attribute("incident_id", request.incident_id)
        span.set_attribute("user_id", token_data.get("sub", "unknown"))
        
        try:
            if not sre_agent:
                raise HTTPException(status_code=503, detail="SRE Agent not initialized")
            
            # Check permissions
            if "incident" not in token_data.get("permissions", []):
                raise HTTPException(status_code=403, detail="Insufficient permissions for incident investigation")
            
            # Create JWT token for agent authentication
            jwt_token = create_access_token(
                data={"sub": token_data.get("sub"), "permissions": token_data.get("permissions", [])}
            )
            
            result = await sre_agent.investigate_incident(request.incident_id, jwt_token)
            
            if "error" in result:
                span.set_attribute("investigation_success", False)
                span.set_attribute("error", result["error"])
                raise HTTPException(status_code=400, detail=result["error"])
            
            span.set_attribute("investigation_success", True)
            
            return {
                "incident_id": request.incident_id,
                "analysis": result.get("analysis", ""),
                "recommendations": result.get("recommendations", []),
                "trace_id": result.get("trace_id", span.get_span_context().trace_id),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=f"Incident investigation failed: {str(e)}")

# Alert monitoring endpoint
@app.get("/alerts/monitor")
async def monitor_alerts(
    severity: Optional[str] = None,
    token_data: Dict[str, Any] = Depends(verify_token)
):
    """Monitor alerts with optional severity filtering"""
    with tracer.start_as_current_span("monitor_alerts") as span:
        span.set_attribute("severity_filter", severity or "all")
        span.set_attribute("user_id", token_data.get("sub", "unknown"))
        
        try:
            if not sre_agent:
                raise HTTPException(status_code=503, detail="SRE Agent not initialized")
            
            # Check permissions
            if "alert" not in token_data.get("permissions", []):
                raise HTTPException(status_code=403, detail="Insufficient permissions for alert monitoring")
            
            # Create JWT token for agent authentication
            jwt_token = create_access_token(
                data={"sub": token_data.get("sub"), "permissions": token_data.get("permissions", [])}
            )
            
            result = await sre_agent.monitor_alerts(severity)
            
            if "error" in result:
                span.set_attribute("monitoring_success", False)
                span.set_attribute("error", result["error"])
                raise HTTPException(status_code=400, detail=result["error"])
            
            span.set_attribute("monitoring_success", True)
            span.set_attribute("alerts_count", result.get("count", 0))
            
            return {
                "alerts": result.get("alerts", []),
                "analysis": result.get("analysis", ""),
                "count": result.get("count", 0),
                "trace_id": result.get("trace_id", span.get_span_context().trace_id),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=f"Alert monitoring failed: {str(e)}")

# System metrics endpoint
@app.get("/metrics/system")
async def get_system_metrics(
    token_data: Dict[str, Any] = Depends(verify_token)
):
    """Get system metrics"""
    with tracer.start_as_current_span("get_system_metrics") as span:
        span.set_attribute("user_id", token_data.get("sub", "unknown"))
        
        try:
            if not sre_agent:
                raise HTTPException(status_code=503, detail="SRE Agent not initialized")
            
            # Check permissions
            if "metrics" not in token_data.get("permissions", []):
                raise HTTPException(status_code=403, detail="Insufficient permissions for system metrics")
            
            # Mock system metrics for now
            metrics = {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "disk_usage": 23.1,
                "network_latency": 12.5,
                "active_connections": 1250,
                "error_rate": 0.02
            }
            
            span.set_attribute("metrics_retrieved", True)
            
            return {
                "metrics": metrics,
                "timestamp": datetime.utcnow().isoformat(),
                "trace_id": span.get_span_context().trace_id
            }
            
        except Exception as e:
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=f"Failed to get system metrics: {str(e)}")

# Performance data endpoint
@app.get("/performance/data")
async def get_performance_data(
    service: Optional[str] = None,
    timeframe: Optional[str] = "1h",
    token_data: Dict[str, Any] = Depends(verify_token)
):
    """Get performance data for services"""
    with tracer.start_as_current_span("get_performance_data") as span:
        span.set_attribute("service", service or "all")
        span.set_attribute("timeframe", timeframe)
        span.set_attribute("user_id", token_data.get("sub", "unknown"))
        
        try:
            if not sre_agent:
                raise HTTPException(status_code=503, detail="SRE Agent not initialized")
            
            # Check permissions
            if "performance" not in token_data.get("permissions", []):
                raise HTTPException(status_code=403, detail="Insufficient permissions for performance data")
            
            # Mock performance data
            performance_data = {
                "response_times": {
                    "p50": 150,
                    "p95": 450,
                    "p99": 1200
                },
                "throughput": 1250,
                "error_rate": 0.015,
                "availability": 99.95
            }
            
            span.set_attribute("performance_data_retrieved", True)
            
            return {
                "service": service or "all",
                "timeframe": timeframe,
                "data": performance_data,
                "timestamp": datetime.utcnow().isoformat(),
                "trace_id": span.get_span_context().trace_id
            }
            
        except Exception as e:
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=f"Failed to get performance data: {str(e)}")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "SRE AI Agent API - Final Architecture",
        "version": "2.0.0",
        "architecture": "LangGraph + JWT + mTLS + OTLP",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "auth": "/auth/login",
            "incidents": "/incidents/investigate",
            "alerts": "/alerts/monitor",
            "metrics": "/metrics/system",
            "performance": "/performance/data"
        },
        "documentation": "/docs"
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with tracing"""
    with tracer.start_as_current_span("http_exception") as span:
        span.set_attribute("status_code", exc.status_code)
        span.set_attribute("detail", exc.detail)
        span.set_attribute("path", str(request.url))
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code,
                "timestamp": datetime.utcnow().isoformat(),
                "trace_id": span.get_span_context().trace_id
            }
        )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions with tracing"""
    with tracer.start_as_current_span("general_exception") as span:
        span.record_exception(exc)
        span.set_attribute("path", str(request.url))
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(exc),
                "timestamp": datetime.utcnow().isoformat(),
                "trace_id": span.get_span_context().trace_id
            }
        )

if __name__ == "__main__":
    # Run the API server
    uvicorn.run(
        "sre_agent_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 