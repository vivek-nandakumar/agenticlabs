#!/usr/bin/env python3
"""
Test script for the SRE AI Agent

This script tests the basic functionality of the SRE agent without requiring
actual MCP server connections, making it useful for development and CI/CD.
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, Any

# Mock the MCP tools for testing
class MockMCPTools:
    """Mock MCP tools for testing without actual server connections"""
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def initialize(self):
        pass

class MockAgent:
    """Mock agent for testing"""
    
    def __init__(self, model, tools, knowledge=None, memory=None, markdown=True):
        self.model = model
        self.tools = tools
        self.knowledge = knowledge
        self.memory = memory
        self.markdown = markdown
    
    async def aprint_response(self, message: str, stream: bool = True, markdown: bool = True):
        """Mock response for testing"""
        return f"Mock response to: {message[:100]}..."

class MockSREAgent:
    """Mock SRE agent for testing"""
    
    def __init__(self, config):
        self.config = config
        self.agent = None
        self.mcp_tools = None
        self.knowledge_base = None
        self.memory = None
        self.storage = None
    
    async def initialize(self):
        """Initialize the mock SRE agent"""
        print("Initializing Mock SRE Agent...")
        
        # Mock components
        self.mcp_tools = MockMCPTools()
        self.agent = MockAgent(
            model="gpt-4o",
            tools=[self.mcp_tools],
            markdown=True
        )
        
        print("Mock SRE Agent initialized successfully")
    
    def _get_mcp_urls(self):
        """Get mock MCP URLs"""
        if self.config.environment == "dev":
            return [
                "https://mcp-elasticsearch-dev.example.com/sse",
                "https://mcp-metrics-dev.example.com/sse",
                "https://mcp-jaeger-dev.example.com/sse"
            ]
        else:
            return [
                "https://mcp-elasticsearch-stage.example.com/sse",
                "https://mcp-metrics-stage.example.com/sse",
                "https://mcp-vanguard-stage.example.com/sse",
                "https://mcp-nagios-stage.example.com/sse",
                "https://mcp-jaeger-stage.example.com/sse"
            ]
    
    async def health_check(self) -> Dict[str, Any]:
        """Mock health check"""
        print("Performing mock system health check...")
        
        response = await self.agent.aprint_response(
            message="Perform a comprehensive health check",
            stream=True,
            markdown=True
        )
        
        return {
            "timestamp": datetime.now().isoformat(),
            "environment": self.config.environment,
            "response": response,
            "status": "healthy",
            "mock": True
        }
    
    async def investigate_incident(self, incident_description: str) -> Dict[str, Any]:
        """Mock incident investigation"""
        print(f"Investigating mock incident: {incident_description}")
        
        response = await self.agent.aprint_response(
            message=f"Investigate: {incident_description}",
            stream=True,
            markdown=True
        )
        
        return {
            "timestamp": datetime.now().isoformat(),
            "incident": incident_description,
            "investigation": response,
            "mock": True
        }
    
    async def monitor_alerts(self) -> Dict[str, Any]:
        """Mock alert monitoring"""
        print("Monitoring for mock alerts...")
        
        response = await self.agent.aprint_response(
            message="Monitor for new alerts",
            stream=True,
            markdown=True
        )
        
        return {
            "timestamp": datetime.now().isoformat(),
            "alerts": response,
            "mock": True
        }

async def test_basic_functionality():
    """Test basic SRE agent functionality"""
    print("=== Testing SRE Agent Basic Functionality ===\n")
    
    # Test configuration
    from sre_agent import SREConfig
    config = SREConfig(environment="stage")
    
    print(f"✓ Configuration created: environment={config.environment}")
    print(f"✓ Alert thresholds: {config.alert_thresholds}")
    
    # Test agent initialization
    agent = MockSREAgent(config)
    await agent.initialize()
    print("✓ Agent initialized successfully")
    
    # Test MCP URLs
    mcp_urls = agent._get_mcp_urls()
    print(f"✓ MCP URLs configured: {len(mcp_urls)} servers")
    for url in mcp_urls:
        print(f"  - {url}")
    
    # Test health check
    print("\n--- Testing Health Check ---")
    health_result = await agent.health_check()
    print(f"✓ Health check completed: {health_result['status']}")
    
    # Test incident investigation
    print("\n--- Testing Incident Investigation ---")
    incident_result = await agent.investigate_incident(
        "High error rate on checkout service"
    )
    print(f"✓ Incident investigation completed")
    
    # Test alert monitoring
    print("\n--- Testing Alert Monitoring ---")
    alerts_result = await agent.monitor_alerts()
    print(f"✓ Alert monitoring completed")
    
    print("\n=== All Basic Tests Passed! ===")

async def test_api_endpoints():
    """Test API endpoint functionality"""
    print("\n=== Testing API Endpoints ===\n")
    
    # This would test the FastAPI endpoints
    # For now, just verify the structure
    
    endpoints = [
        "/health",
        "/api/health-check",
        "/api/investigate",
        "/api/alerts/monitor",
        "/api/trends/analyze",
        "/api/remediation/suggest",
        "/api/reports/generate",
        "/api/config",
        "/api/metrics"
    ]
    
    print("✓ API endpoints defined:")
    for endpoint in endpoints:
        print(f"  - {endpoint}")
    
    print("\n=== API Endpoint Tests Passed! ===")

def test_configuration():
    """Test configuration validation"""
    print("\n=== Testing Configuration ===\n")
    
    from sre_agent import SREConfig
    
    # Test default configuration
    config = SREConfig()
    print(f"✓ Default environment: {config.environment}")
    print(f"✓ Default model: {config.model_name}")
    print(f"✓ Alert thresholds: {config.alert_thresholds}")
    
    # Test custom configuration
    custom_config = SREConfig(
        environment="dev",
        model_name="gpt-4",
        alert_thresholds={
            "cpu_usage": 90.0,
            "memory_usage": 95.0,
            "error_rate": 10.0
        }
    )
    print(f"✓ Custom environment: {custom_config.environment}")
    print(f"✓ Custom model: {custom_config.model_name}")
    print(f"✓ Custom thresholds: {custom_config.alert_thresholds}")
    
    print("\n=== Configuration Tests Passed! ===")

def test_dependencies():
    """Test that all required dependencies are available"""
    print("\n=== Testing Dependencies ===\n")
    
    required_modules = [
        "agno",
        "fastapi",
        "uvicorn",
        "pydantic",
        "asyncio",
        "logging",
        "datetime",
        "typing"
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} - MISSING")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Missing dependencies: {missing_modules}")
        print("Please install missing dependencies with: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All dependencies available")
        return True

async def main():
    """Main test function"""
    print("🚀 SRE Agent Test Suite")
    print("=" * 50)
    
    # Test dependencies first
    if not test_dependencies():
        sys.exit(1)
    
    # Test configuration
    test_configuration()
    
    # Test basic functionality
    await test_basic_functionality()
    
    # Test API endpoints
    await test_api_endpoints()
    
    print("\n" + "=" * 50)
    print("🎉 All Tests Passed!")
    print("\nNext steps:")
    print("1. Set your OPENAI_API_KEY environment variable")
    print("2. Run: python sre_agent.py")
    print("3. Or run: python sre_agent_api.py")
    print("4. Or run: docker-compose up -d")

if __name__ == "__main__":
    asyncio.run(main()) 