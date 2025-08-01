# 🚀 Production-Level SRE AI Agent

A comprehensive, production-ready Site Reliability Engineering (SRE) AI Agent built with the **agno** framework that follows a complete architecture with **LangGraph Flow orchestration**, **LLM Reasoning Core**, **Observability Adapter Layer**, **Insight Cache**, and **Action Policies & Playbooks**.

## 🏗️ Architecture Overview

The SRE AI Agent follows a sophisticated architecture that enables intelligent, automated operations:

```
┌─────────────────────────────────────────────────────────────────┐
│                    SRE AI Agent Architecture                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────────────────────────┐ │
│  │  LangGraph Flow │───▶│        LLM Reasoning Core           │ │
│  │  Orchestration  │    │  • Normalize & Query Data          │ │
│  │                 │    │  • Retrieve/Store Context          │ │
│  └─────────────────┘    │  • Drive Automated Actions         │ │
│                         └─────────────────────────────────────┘ │
│                                    │                            │
│                                    ▼                            │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              Observability Adapter Layer                   │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │ │
│  │  │ Elastic     │ │ Prometheus  │ │ Vanguard    │          │ │
│  │  │ Adapter     │ │ Adapter     │ │ Adapter     │          │ │
│  │  │ (Logs)      │ │ (Metrics)   │ │ (Events)    │          │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘          │ │
│  │  ┌─────────────┐ ┌─────────────┐                          │ │
│  │  │ Nagios      │ │ Jaeger      │                          │ │
│  │  │ Adapter     │ │ Adapter     │                          │ │
│  │  │ (Health)    │ │ (Traces)    │                          │ │
│  │  └─────────────┘ └─────────────┘                          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                    │                            │
│                                    ▼                            │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                Insight Cache (Redis/SQLite)                │ │
│  │  • Context Retention                                        │ │
│  │  • Knowledge Persistence                                    │ │
│  │  • Historical Analysis                                      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                    │                            │
│                                    ▼                            │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              ACTION POLICIES & PLAYBOOKS                   │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │ │
│  │  │ Summarize   │ │ Propose     │ │ Trigger     │          │ │
│  │  │ Incident    │ │ Remediation │ │ Auto-       │          │ │
│  │  │             │ │             │ │ Rollback    │          │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘          │ │
│  │  ┌─────────────┐ ┌─────────────┐                          │ │
│  │  │ Open Jira   │ │ Open Slack  │                          │ │
│  │  │ Channel     │ │ Channel     │                          │ │
│  │  │             │ │             │                          │ │
│  │  └─────────────┘ └─────────────┘                          │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## ✨ Key Features

### 🧠 **Intelligent Reasoning**
- **Multi-step reasoning** with LangGraph Flow orchestration
- **Chain-of-thought** analysis for complex problems
- **Context-aware** decision making
- **Confidence scoring** for all recommendations

### 🔍 **Comprehensive Observability**
- **Elasticsearch** integration for log analysis
- **Prometheus** integration for metrics and alerting
- **Vanguard** integration for events and SLO burn rates
- **Nagios** integration for health checks
- **Jaeger** integration for distributed tracing

### ⚡ **Automated Actions**
- **Incident summarization** and reporting
- **Automated remediation** suggestions
- **Auto-rollback** capabilities
- **Jira ticket** creation
- **Slack channel** management
- **Service scaling** and restart

### 💾 **Smart Caching & Memory**
- **Insight cache** for context retention
- **Knowledge persistence** across sessions
- **Historical analysis** and trend detection
- **Learning from past incidents**

### 🛡️ **Production Ready**
- **Docker** containerization
- **Kubernetes** deployment ready
- **Health checks** and monitoring
- **Comprehensive API** with OpenAPI docs
- **Security** best practices

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- OpenAI API key

### 1. Clone and Setup
```bash
git clone <repository-url>
cd agentic-sre-demo
export OPENAI_API_KEY="your-openai-api-key"
```

### 2. Deploy with Docker (Recommended)
```bash
# Deploy with full observability stack
./deploy.sh deploy

# Or deploy just the SRE agent
docker-compose up -d sre-agent
```

### 3. Access the API
```bash
# API Documentation
open http://localhost:8000/docs

# Health Check
curl http://localhost:8000/health

# Architecture Status
curl http://localhost:8000/api/architecture/status
```

### 4. Run Demo
```bash
# Run the architecture demo
python demo_sre_agent.py
```

## 📡 API Endpoints

### Core Operations
- `POST /api/health-check` - Comprehensive system health check
- `POST /api/investigate` - Incident investigation with reasoning
- `POST /api/alerts/monitor` - Alert monitoring and correlation
- `POST /api/trends/analyze` - Trend analysis with forecasting
- `POST /api/remediation/suggest` - Remediation suggestions

### Automated Actions
- `POST /api/actions/execute` - Execute automated actions
- `POST /api/reports/generate` - Generate incident reports

### Configuration & Monitoring
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration
- `GET /api/metrics` - System metrics
- `GET /api/architecture/status` - Architecture component status
- `GET /api/insights/{insight_type}` - Get cached insights

## 🔧 Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your-openai-api-key

# Optional
ENVIRONMENT=stage                    # dev, stage, prod
MODEL_NAME=gpt-4o                   # LLM model
REASONING_ENABLED=true              # Enable reasoning
AUTO_REMEDIATION_ENABLED=true       # Enable auto-remediation
REASONING_MIN_STEPS=3               # Min reasoning steps
REASONING_MAX_STEPS=10              # Max reasoning steps
```

### MCP Server Configuration
The agent is pre-configured for your observability stack:
- **Elasticsearch**: `https://mcp-elasticsearch-onprem.sadc-tlmy-{env}.carbon.lowes.com/sse`
- **Prometheus**: `https://mcp-metrics-onprem.sadc-tlmy-{env}.carbon.lowes.com/sse`
- **Vanguard**: `https://mcp-vanguard.sadc-tlmy-stg01.carbon.lowes.com/sse`
- **Nagios**: `https://mcp-nagios.sadc-metrics-tlmy-stg01.carbon.lowes.com/sse`
- **Jaeger**: `https://mcp-jaeger-onprem.sadc-tlmy-stg01.carbon.lowes.com/sse`

## 🏗️ Architecture Components

### 1. LangGraph Flow Orchestration
- **Multi-step reasoning** workflows
- **Conditional routing** based on analysis
- **Parallel execution** of data collection
- **State management** across workflow steps

### 2. LLM Reasoning Core
- **Chain-of-thought** reasoning
- **Context-aware** decision making
- **Confidence scoring** for actions
- **Multi-model** support (GPT-4, Claude, etc.)

### 3. Observability Adapter Layer
- **Normalized data** from multiple sources
- **Real-time** data collection
- **Correlation** across systems
- **Historical** data analysis

### 4. Insight Cache
- **Context retention** across sessions
- **Knowledge persistence** in JSON storage
- **TTL-based** cache management
- **Historical** trend analysis

### 5. Action Policies & Playbooks
- **Policy-based** action approval
- **Confidence thresholds** for automation
- **Risk assessment** for actions
- **Rollback** procedures

## 📊 Monitoring & Observability

### Built-in Monitoring
- **Health checks** for all components
- **Performance metrics** collection
- **Error tracking** and alerting
- **Architecture status** monitoring

### Integration with Your Stack
- **Prometheus** metrics export
- **Grafana** dashboards
- **Elasticsearch** log shipping
- **Jaeger** distributed tracing

## 🔒 Security

### Security Features
- **Non-root** container execution
- **Environment variable** configuration
- **API authentication** ready
- **HTTPS** support for production
- **Secrets management** integration

### Best Practices
- **Principle of least privilege**
- **Regular security updates**
- **Audit logging**
- **Network isolation**

## 🧪 Testing

### Test Coverage
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sre_agent

# Run specific test
pytest test_sre_agent.py::test_health_check
```

### Demo Scenarios
```bash
# Run architecture demo
python demo_sre_agent.py

# Test API endpoints
curl -X POST http://localhost:8000/api/health-check
```

## 📈 Performance

### Optimization Features
- **Async/await** for I/O operations
- **Connection pooling** for MCP servers
- **Caching** for frequently accessed data
- **Background tasks** for monitoring

### Scalability
- **Horizontal scaling** ready
- **Load balancing** support
- **Resource limits** configuration
- **Auto-scaling** policies

## 🤝 Contributing

### Development Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python sre_agent_api.py
```

### Code Quality
```bash
# Format code
black .
isort .

# Lint code
flake8
mypy .

# Run tests
pytest
```

## 📚 Documentation

### Additional Resources
- **API Documentation**: http://localhost:8000/docs
- **Architecture Diagram**: https://app.eraser.io/workspace/TXlvKwP25tLWjFXgKHzI
- **agno Framework**: https://github.com/agno-ai/agno
- **MCP Protocol**: https://modelcontextprotocol.io/

### Examples
- **Basic Usage**: `examples/basic_usage.py`
- **Advanced Workflows**: `examples/advanced_workflows.py`
- **Custom Actions**: `examples/custom_actions.py`

## 🆘 Troubleshooting

### Common Issues

#### Agent Not Initializing
```bash
# Check OpenAI API key
echo $OPENAI_API_KEY

# Check MCP server connectivity
curl -f https://mcp-elasticsearch-onprem.sadc-tlmy-stg01.carbon.lowes.com/sse
```

#### Performance Issues
```bash
# Check resource usage
docker stats sre-agent

# Check logs
docker logs sre-agent
```

#### Architecture Components
```bash
# Check architecture status
curl http://localhost:8000/api/architecture/status

# Check individual components
curl http://localhost:8000/api/insights/health_check
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **agno** framework for the multi-agent system capabilities
- **Model Context Protocol (MCP)** for observability integration
- **OpenAI** for the LLM capabilities
- **FuzzyLabs** for the SRE agent inspiration

---

**🏆 Production-Ready SRE AI Agent with Full Architecture Compliance!**

For support, questions, or contributions, please open an issue or reach out to the development team. 