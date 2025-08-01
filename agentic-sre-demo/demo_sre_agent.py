"""
Demo script for the Production-Level SRE AI Agent with Full Architecture

This script demonstrates the SRE agent's capabilities with:
- LangGraph Flow orchestration
- LLM Reasoning Core (using local Llama3 model)
- Observability Adapter Layer
- Insight Cache
- Action Policies & Playbooks
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any

from sre_agent import SREAgent, SREConfig, ActionType

class DemoData:
    """Mock data for demonstration purposes"""
    
    def get_mock_metrics(self) -> Dict[str, Any]:
        return {
            "cpu_usage": {
                "checkout_service": 75.2,
                "payment_service": 45.8,
                "inventory_service": 62.1,
                "user_service": 38.9
            },
            "memory_usage": {
                "checkout_service": 82.5,
                "payment_service": 67.3,
                "inventory_service": 71.8,
                "user_service": 58.2
            },
            "error_rate": {
                "checkout_service": 8.5,
                "payment_service": 2.1,
                "inventory_service": 1.8,
                "user_service": 0.9
            },
            "latency_p95": {
                "checkout_service": 1200,
                "payment_service": 450,
                "inventory_service": 680,
                "user_service": 320
            }
        }
    
    def get_mock_alerts(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "alert_001",
                "severity": "critical",
                "service": "checkout_service",
                "message": "High error rate detected",
                "timestamp": datetime.now().isoformat(),
                "value": 8.5,
                "threshold": 5.0
            },
            {
                "id": "alert_002",
                "severity": "warning",
                "service": "checkout_service",
                "message": "High latency detected",
                "timestamp": datetime.now().isoformat(),
                "value": 1200,
                "threshold": 1000
            },
            {
                "id": "alert_003",
                "severity": "warning",
                "service": "inventory_service",
                "message": "High memory usage",
                "timestamp": datetime.now().isoformat(),
                "value": 71.8,
                "threshold": 70.0
            }
        ]
    
    def get_mock_incidents(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "INC-001",
                "title": "Checkout Service High Error Rate",
                "description": "Checkout service experiencing 8.5% error rate, affecting customer transactions",
                "severity": "high",
                "status": "investigating",
                "created_at": datetime.now().isoformat(),
                "affected_services": ["checkout_service", "payment_service"]
            }
        ]

class MockSREAgent(SREAgent):
    """Mock SRE Agent for demonstration purposes"""
    
    def __init__(self, config: SREConfig):
        super().__init__(config)
        self.demo_data = DemoData()
        
    async def initialize(self):
        """Mock initialization"""
        print("🔧 Initializing SRE Agent with Full Architecture...")
        print("   ✅ LangGraph Flow: Active")
        print("   ✅ LLM Reasoning Core: Active (Local Llama3)")
        print("   ✅ Observability Adapter Layer: Active")
        print("   ✅ Insight Cache: Active")
        print("   ✅ Action Policies & Playbooks: Active")
        print("   ✅ MCP Tools: Connected")
        print("   ✅ Knowledge Base: Initialized")
        print("   ✅ Memory: Active")
        print("   ✅ Storage: Configured")
        print("🎉 SRE Agent initialized successfully!\n")
        
    async def get_architecture_status(self) -> Dict[str, Any]:
        """Get mock architecture status"""
        return {
            "langgraph_flow": {
                "status": "active",
                "workflow_name": "SRE Incident Response",
                "steps": ["data_collection", "analysis", "reasoning", "action_decision", "execution"]
            },
            "llm_reasoning_core": {
                "status": "active",
                "reasoning_enabled": True,
                "model": self.config.model_name,
                "model_type": "local_llama3",
                "reasoning_steps": "3-10"
            },
            "observability_adapter": {
                "status": "active",
                "mcp_servers": 5,
                "adapters": ["elasticsearch", "prometheus", "vanguard", "nagios", "jaeger"]
            },
            "insight_cache": {
                "status": "active",
                "storage_type": "json",
                "cached_insights": ["health_check", "incident_investigation", "trend_analysis"]
            },
            "action_policies": {
                "status": "active",
                "auto_remediation_enabled": True,
                "available_actions": ["summarize_incident", "propose_remediation", "trigger_auto_rollback", "open_jira_ticket", "open_slack_channel"]
            }
        }
        
    async def health_check(self) -> Dict[str, Any]:
        """Mock health check with architecture compliance"""
        print("🔍 Performing System Health Check with Full Architecture...")
        print("   📊 Collecting data from all observability sources...")
        print("   🧠 Applying reasoning to analyze system state (Local Llama3)...")
        print("   💾 Storing insights in cache...")
        print("   ⚡ Evaluating automated actions...")
        
        metrics = self.demo_data.get_mock_metrics()
        issues = []
        
        if metrics["error_rate"]["checkout_service"] > 5.0:
            issues.append("High error rate on checkout service (8.5%)")
        if metrics["latency_p95"]["checkout_service"] > 1000:
            issues.append("High latency on checkout service (1200ms)")
        if metrics["memory_usage"]["inventory_service"] > 70.0:
            issues.append("High memory usage on inventory service (71.8%)")
            
        health_score = 100 - len(issues) * 20
        
        return {
            "timestamp": datetime.now().isoformat(),
            "environment": self.config.environment,
            "health_score": health_score,
            "status": "degraded" if issues else "healthy",
            "issues": issues,
            "metrics_summary": {
                "services_healthy": 4 - len(issues),
                "services_degraded": len(issues),
                "total_services": 4
            },
            "architecture_compliant": True,
            "workflow_result": {
                "data_collection": "completed",
                "analysis": "completed",
                "reasoning": "completed",
                "action_decision": "no_immediate_actions",
                "execution": "skipped"
            }
        }
        
    async def investigate_incident(self, incident_description: str) -> Dict[str, Any]:
        """Mock incident investigation with full architecture"""
        print(f"🔍 Investigating Incident with Full Architecture...")
        print(f"   📝 Incident: {incident_description}")
        print("   📊 Step 1: Data Collection from all sources...")
        print("   🧠 Step 2: Multi-step reasoning analysis (Local Llama3)...")
        print("   🔍 Step 3: Root cause identification...")
        print("   ⚡ Step 4: Action policy evaluation...")
        print("   🎯 Step 5: Remediation planning...")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "incident": incident_description,
            "investigation": {
                "root_cause": "Database connection pool exhaustion",
                "affected_services": ["checkout_service", "payment_service"],
                "business_impact": "Customer transactions failing",
                "resolution_time": "15 minutes",
                "recommendations": [
                    "Scale database connection pool",
                    "Implement connection pooling monitoring",
                    "Add circuit breaker pattern"
                ]
            },
            "architecture_compliant": True,
            "workflow_result": {
                "data_collection": "completed",
                "analysis": "completed", 
                "reasoning": "completed",
                "action_decision": "propose_remediation",
                "execution": "remediation_suggested"
            }
        }
        
    async def monitor_alerts(self) -> Dict[str, Any]:
        """Mock alert monitoring with architecture compliance"""
        print("🚨 Monitoring Alerts with Full Architecture...")
        print("   📊 Collecting alert data from all sources...")
        print("   🧠 Correlating alerts across systems (Local Llama3)...")
        print("   ⚡ Evaluating automated response policies...")
        
        alerts = self.demo_data.get_mock_alerts()
        critical_alerts = [a for a in alerts if a["severity"] == "critical"]
        warnings = [a for a in alerts if a["severity"] == "warning"]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "alerts": {
                "total": len(alerts),
                "critical": len(critical_alerts),
                "warnings": len(warnings),
                "alerts": alerts
            },
            "architecture_compliant": True,
            "workflow_result": {
                "data_collection": "completed",
                "analysis": "completed",
                "reasoning": "completed", 
                "action_decision": "escalate_critical_alerts",
                "execution": "alerts_prioritized"
            }
        }
        
    async def analyze_trends(self, metric: str, timeframe: str = "7d") -> Dict[str, Any]:
        """Mock trend analysis with architecture compliance"""
        print(f"📈 Analyzing Trends with Full Architecture...")
        print(f"   📊 Metric: {metric}")
        print(f"   ⏰ Timeframe: {timeframe}")
        print("   🧠 Applying reasoning for trend analysis (Local Llama3)...")
        print("   🔮 Generating forecasts...")
        
        return {
            "metric": metric,
            "timeframe": timeframe,
            "timestamp": datetime.now().isoformat(),
            "analysis": {
                "trend_direction": "increasing",
                "current_value": 75.2,
                "baseline": 45.0,
                "forecast_24h": 78.5,
                "forecast_7d": 82.1,
                "anomalies_detected": 2,
                "recommendations": [
                    "Monitor closely for next 24 hours",
                    "Consider scaling resources",
                    "Review recent deployments"
                ]
            },
            "architecture_compliant": True,
            "workflow_result": {
                "data_collection": "completed",
                "analysis": "completed",
                "reasoning": "completed",
                "action_decision": "monitor_closely",
                "execution": "forecast_generated"
            }
        }
        
    async def suggest_remediation(self, issue_description: str) -> Dict[str, Any]:
        """Mock remediation suggestion with architecture compliance"""
        print(f"🔧 Suggesting Remediation with Full Architecture...")
        print(f"   📝 Issue: {issue_description}")
        print("   🧠 Analyzing issue with reasoning (Local Llama3)...")
        print("   ⚡ Evaluating automated action policies...")
        print("   🎯 Planning remediation steps...")
        
        return {
            "issue": issue_description,
            "timestamp": datetime.now().isoformat(),
            "remediation_plan": {
                "immediate_actions": [
                    "Restart affected service",
                    "Scale up database connections",
                    "Enable circuit breaker"
                ],
                "long_term_fixes": [
                    "Implement connection pooling monitoring",
                    "Add auto-scaling policies",
                    "Update deployment procedures"
                ],
                "risk_assessment": {
                    "risk_level": "medium",
                    "rollback_plan": "available",
                    "estimated_downtime": "5 minutes"
                },
                "automated_actions": [
                    {
                        "action": "restart_service",
                        "confidence": 0.9,
                        "automated": True
                    },
                    {
                        "action": "scale_connections", 
                        "confidence": 0.8,
                        "automated": True
                    }
                ]
            },
            "architecture_compliant": True,
            "workflow_result": {
                "data_collection": "completed",
                "analysis": "completed",
                "reasoning": "completed",
                "action_decision": "execute_automated_actions",
                "execution": "remediation_planned"
            }
        }
        
    async def execute_automated_action(self, action_type: ActionType, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock automated action execution"""
        print(f"⚡ Executing Automated Action: {action_type.value}")
        print(f"   📋 Parameters: {params}")
        print("   ⚡ Checking action policies...")
        print("   ✅ Action approved by policies...")
        print("   🚀 Executing action...")
        
        if action_type == ActionType.SUMMARIZE_INCIDENT:
            return {
                "success": True,
                "summary": f"Incident {params.get('incident_id', 'unknown')} summary generated",
                "severity": params.get("severity", "medium"),
                "affected_services": params.get("affected_services", [])
            }
        elif action_type == ActionType.PROPOSE_REMEDIATION:
            return {
                "success": True,
                "remediation_steps": [
                    "1. Restart affected service",
                    "2. Scale up resources if needed", 
                    "3. Update monitoring thresholds"
                ],
                "estimated_time": "15 minutes"
            }
        elif action_type == ActionType.TRIGGER_AUTO_ROLLBACK:
            return {
                "success": True,
                "rollback_target": params.get("deployment_id"),
                "status": "rollback_initiated"
            }
        else:
            return {
                "success": True,
                "action_executed": action_type.value,
                "result": "Action completed successfully"
            }

async def demo_architecture_components():
    """Demonstrate the architecture components"""
    print("🏗️  SRE AI Agent Architecture Components Demo")
    print("=" * 60)
    
    config = SREConfig(
        environment="stage",
        model_name="llama3.1:8b",  # Using local Llama3 model
        model_url="http://localhost:11434",  # Ollama server URL
        reasoning_enabled=True,
        auto_remediation_enabled=True
    )
    
    agent = MockSREAgent(config)
    await agent.initialize()
    
    # 1. Architecture Status
    print("\n1. 📊 Architecture Component Status")
    print("-" * 40)
    arch_status = await agent.get_architecture_status()
    for component, status in arch_status.items():
        print(f"   {component.replace('_', ' ').title()}: {status['status']}")
        if component == "llm_reasoning_core":
            print(f"   Model: {status['model']} ({status['model_type']})")
    
    # 2. Health Check with Architecture
    print("\n2. 🔍 System Health Check")
    print("-" * 40)
    health_result = await agent.health_check()
    print(f"   Health Score: {health_result['health_score']}/100")
    print(f"   Status: {health_result['status']}")
    print(f"   Issues Found: {len(health_result['issues'])}")
    print(f"   Architecture Compliant: {health_result['architecture_compliant']}")
    
    # 3. Incident Investigation
    print("\n3. 🔍 Incident Investigation")
    print("-" * 40)
    incident_result = await agent.investigate_incident(
        "High error rate on checkout service, 500 errors increasing over last 30 minutes"
    )
    print(f"   Root Cause: {incident_result['investigation']['root_cause']}")
    print(f"   Resolution Time: {incident_result['investigation']['resolution_time']}")
    print(f"   Architecture Compliant: {incident_result['architecture_compliant']}")
    
    # 4. Alert Monitoring
    print("\n4. 🚨 Alert Monitoring")
    print("-" * 40)
    alerts_result = await agent.monitor_alerts()
    print(f"   Total Alerts: {alerts_result['alerts']['total']}")
    print(f"   Critical Alerts: {alerts_result['alerts']['critical']}")
    print(f"   Warnings: {alerts_result['alerts']['warnings']}")
    print(f"   Architecture Compliant: {alerts_result['architecture_compliant']}")
    
    # 5. Trend Analysis
    print("\n5. 📈 Trend Analysis")
    print("-" * 40)
    trend_result = await agent.analyze_trends("cpu_usage", "24h")
    print(f"   Trend Direction: {trend_result['analysis']['trend_direction']}")
    print(f"   Current Value: {trend_result['analysis']['current_value']}%")
    print(f"   Forecast 24h: {trend_result['analysis']['forecast_24h']}%")
    print(f"   Architecture Compliant: {trend_result['architecture_compliant']}")
    
    # 6. Remediation Suggestion
    print("\n6. 🔧 Remediation Suggestion")
    print("-" * 40)
    remediation_result = await agent.suggest_remediation(
        "Database connection pool exhausted, causing timeouts"
    )
    print(f"   Risk Level: {remediation_result['remediation_plan']['risk_assessment']['risk_level']}")
    print(f"   Estimated Downtime: {remediation_result['remediation_plan']['risk_assessment']['estimated_downtime']}")
    print(f"   Automated Actions: {len(remediation_result['remediation_plan']['automated_actions'])}")
    print(f"   Architecture Compliant: {remediation_result['architecture_compliant']}")
    
    # 7. Automated Action Execution
    print("\n7. ⚡ Automated Action Execution")
    print("-" * 40)
    action_result = await agent.execute_automated_action(
        ActionType.SUMMARIZE_INCIDENT,
        {
            "incident_id": "INC-001",
            "severity": "high",
            "confidence": 0.9
        }
    )
    print(f"   Action Success: {action_result['success']}")
    print(f"   Summary: {action_result['summary']}")
    
    print("\n🎉 Architecture Demo Completed Successfully!")
    print("=" * 60)

async def demo_api_endpoints():
    """Demonstrate the API endpoints"""
    print("\n🌐 API Endpoints Demo")
    print("=" * 60)
    
    print("Available API Endpoints:")
    print("  GET  /health                           - Basic health check")
    print("  POST /api/health-check                 - Comprehensive health check")
    print("  POST /api/investigate                  - Incident investigation")
    print("  POST /api/alerts/monitor               - Alert monitoring")
    print("  POST /api/trends/analyze               - Trend analysis")
    print("  POST /api/remediation/suggest          - Remediation suggestions")
    print("  POST /api/reports/generate             - Incident report generation")
    print("  POST /api/actions/execute              - Execute automated actions")
    print("  GET  /api/config                       - Get configuration")
    print("  POST /api/config                       - Update configuration")
    print("  GET  /api/metrics                      - System metrics")
    print("  GET  /api/architecture/status          - Architecture status")
    print("  GET  /api/insights/{insight_type}      - Get cached insights")
    print("  GET  /docs                             - API documentation")
    
    print("\nExample API Usage:")
    print("  curl -X POST http://localhost:8000/api/health-check")
    print("  curl -X POST http://localhost:8000/api/investigate \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"incident_description\": \"High error rate on checkout service\"}'")
    
    print("\n📚 API Documentation available at: http://localhost:8000/docs")

async def demo_configuration_options():
    """Demonstrate configuration options"""
    print("\n⚙️  Configuration Options Demo")
    print("=" * 60)
    
    print("Environment Configuration:")
    print("  - Environment: dev/stage/prod")
    print("  - Model: llama3.1:8b (Local Llama3 via Ollama)")
    print("  - Model URL: http://localhost:11434 (Ollama server)")
    print("  - Reasoning: enabled/disabled")
    print("  - Auto-remediation: enabled/disabled")
    print("  - Reasoning steps: 3-10")
    
    print("\nMCP Server Configuration:")
    print("  - Elasticsearch: Log analysis")
    print("  - Prometheus: Metrics and alerting")
    print("  - Vanguard: Events and SLO burn rates")
    print("  - Nagios: Health checks")
    print("  - Jaeger: Distributed tracing")
    
    print("\nAction Policies:")
    print("  - Auto-remediation threshold: 80% confidence")
    print("  - Max auto-actions per incident: 3")
    print("  - Available actions: summarize, remediate, rollback, jira, slack")
    
    print("\nLocal Model Setup:")
    print("  1. Install Ollama: https://ollama.ai/")
    print("  2. Pull Llama3 model: ollama pull llama3.1:8b")
    print("  3. Start Ollama server: ollama serve")
    print("  4. Verify connection: curl http://localhost:11434/api/tags")

async def main():
    """Main demo function"""
    print("🚀 SRE AI Agent - Full Architecture Demo (Local Llama3)")
    print("=" * 60)
    print("This demo showcases the production-level SRE AI Agent with:")
    print("  ✅ LangGraph Flow orchestration")
    print("  ✅ LLM Reasoning Core (Local Llama3)")
    print("  ✅ Observability Adapter Layer")
    print("  ✅ Insight Cache")
    print("  ✅ Action Policies & Playbooks")
    print("  ✅ MCP Integration")
    print("  ✅ Automated Remediation")
    print("  ✅ Comprehensive API")
    print("=" * 60)
    
    # Run architecture demo
    await demo_architecture_components()
    
    # Run API demo
    await demo_api_endpoints()
    
    # Run configuration demo
    await demo_configuration_options()
    
    print("\n🎯 Next Steps:")
    print("  1. Install Ollama: https://ollama.ai/")
    print("  2. Pull Llama3 model: ollama pull llama3.1:8b")
    print("  3. Start Ollama server: ollama serve")
    print("  4. Deploy with Docker: ./deploy.sh deploy")
    print("  5. Access the API: http://localhost:8000/docs")
    print("  6. Monitor with Grafana: http://localhost:3000")
    print("  7. View architecture diagram: https://app.eraser.io/workspace/TXlvKwP25tLWjFXgKHzI")
    
    print("\n🏆 Production-Ready SRE AI Agent with Full Architecture Compliance!")

if __name__ == "__main__":
    asyncio.run(main()) 