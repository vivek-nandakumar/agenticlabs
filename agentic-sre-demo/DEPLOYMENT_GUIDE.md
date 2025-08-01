# SRE AI Agent Deployment Guide

This guide provides step-by-step instructions for deploying and using the Production-Level SRE AI Agent in your environment.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ or Docker
- OpenAI API key (or other supported LLM provider)
- Access to your MCP servers (Elasticsearch, Prometheus, Vanguard, Nagios, Jaeger)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd sre-agent
```

### 2. Set Environment Variables
```bash
export OPENAI_API_KEY="your-openai-api-key"
export ENVIRONMENT="stage"  # or "dev"
```

### 3. Deploy with Docker (Recommended)
```bash
# Deploy all services
./deploy.sh deploy

# Or manually with docker-compose
docker-compose up -d
```

### 4. Access the Services
- **SRE Agent API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

## 🔧 Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your-openai-api-key

# Optional
ENVIRONMENT=stage                    # dev, stage, or prod
MODEL_NAME=gpt-4o                   # LLM model to use
LOG_LEVEL=INFO                      # Logging level
POSTGRES_PASSWORD=sre_password      # Database password
GRAFANA_PASSWORD=admin              # Grafana admin password
```

### MCP Server Configuration
The agent is pre-configured for your infrastructure:

**Development Environment:**
- Elasticsearch: `https://mcp-elasticsearch-onprem.sadc-tlmy-dev01.carbon.lowes.com/sse`
- Prometheus: `https://mcp-metrics-onprem.sadc-tlmy-dev01.carbon.lowes.com/sse`
- Jaeger: `https://mcp-jaeger-onprem.sadc-tlmy-stg01.carbon.lowes.com/sse`

**Staging Environment:**
- Elasticsearch: `https://mcp-elasticsearch-onprem.sadc-tlmy-stg01.carbon.lowes.com/sse`
- Prometheus: `https://mcp-metrics-onprem.sadc-tlmy-stg01.carbon.lowes.com/sse`
- Vanguard: `https://mcp-vanguard.sadc-tlmy-stg01.carbon.lowes.com/sse`
- Nagios: `https://mcp-nagios.sadc-metrics-tlmy-stg01.carbon.lowes.com/sse`
- Jaeger: `https://mcp-jaeger-onprem.sadc-tlmy-stg01.carbon.lowes.com/sse`

## 📡 API Usage

### Health Check
```bash
curl -X POST "http://localhost:8000/api/health-check" \
  -H "Content-Type: application/json" \
  -d '{"environment": "stage", "include_details": true}'
```

### Incident Investigation
```bash
curl -X POST "http://localhost:8000/api/investigate" \
  -H "Content-Type: application/json" \
  -d '{
    "incident_description": "High error rate on checkout service, 500 errors increasing over last 30 minutes",
    "priority": "high",
    "include_traces": true
  }'
```

### Alert Monitoring
```bash
curl -X POST "http://localhost:8000/api/alerts/monitor" \
  -H "Content-Type: application/json" \
  -d '{
    "severity_filter": "critical",
    "time_window": "1h",
    "include_acknowledged": false
  }'
```

### Trend Analysis
```bash
curl -X POST "http://localhost:8000/api/trends/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "metric": "cpu_usage",
    "timeframe": "7d",
    "include_forecast": true
  }'
```

### Remediation Suggestions
```bash
curl -X POST "http://localhost:8000/api/remediation/suggest" \
  -H "Content-Type: application/json" \
  -d '{
    "issue_description": "Database connection pool exhausted, causing timeouts",
    "urgency": "high",
    "include_rollback_plan": true
  }'
```

## 🐳 Docker Deployment

### Single Container
```bash
# Build and run
docker build -t sre-agent .
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY="your-key" \
  -e ENVIRONMENT="stage" \
  --name sre-agent \
  sre-agent
```

### Full Stack with Docker Compose
```bash
# Deploy all services
docker-compose up -d

# Scale the SRE agent
docker-compose up -d --scale sre-agent=3

# View logs
docker-compose logs -f sre-agent

# Stop services
docker-compose down
```

### Production Deployment
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# With custom configuration
ENVIRONMENT=prod \
OPENAI_API_KEY="your-key" \
docker-compose -f docker-compose.prod.yml up -d
```

## 🔍 Monitoring & Observability

### Built-in Monitoring
The SRE agent includes comprehensive monitoring:

- **Health Checks**: Automatic health monitoring with Docker health checks
- **Metrics**: Prometheus metrics endpoint at `/api/metrics`
- **Logging**: Structured logging with configurable levels
- **Dashboards**: Grafana dashboards for visualization

### External Monitoring
- **Prometheus**: Scrapes agent metrics every 30 seconds
- **Grafana**: Pre-configured dashboards for agent performance
- **Elasticsearch**: Log aggregation and analysis
- **Alerting**: Integration with your existing alerting systems

### Key Metrics
- Agent uptime and health
- Total investigations performed
- Active alerts count
- MCP connection status
- Response times for API calls

## 🧪 Testing

### Run Tests
```bash
# Activate virtual environment
source .venv/bin/activate

# Run test suite
python test_sre_agent.py

# Run demo
python demo_sre_agent.py
```

### Test API Endpoints
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test system health check
curl -X POST http://localhost:8000/api/health-check \
  -H "Content-Type: application/json" \
  -d '{"environment": "stage"}'
```

## 🔒 Security

### Security Features
- **Non-root container**: Runs as non-root user in Docker
- **Environment variables**: Sensitive data via environment variables
- **CORS configuration**: Configurable CORS for web access
- **Input validation**: Pydantic models for request validation
- **Rate limiting**: Built-in rate limiting (configurable)

### Best Practices
- Use HTTPS in production
- Implement proper authentication/authorization
- Regular security updates
- Monitor for suspicious activity
- Use secrets management for sensitive data

## 📈 Performance & Scaling

### Performance Optimization
- **Async operations**: All operations are async for better performance
- **Connection pooling**: Efficient MCP server connections
- **Caching**: Redis-based caching for frequently accessed data
- **Background tasks**: Continuous monitoring in background

### Scaling Considerations
- **Horizontal scaling**: Multiple agent instances behind load balancer
- **Database scaling**: Use external database for persistence
- **Cache scaling**: Redis cluster for high availability
- **Monitoring scaling**: Separate monitoring infrastructure

## 🚨 Troubleshooting

### Common Issues

#### 1. MCP Connection Issues
```bash
# Check MCP server connectivity
curl -f https://mcp-elasticsearch-stage.sadc-tlmy-stg01.carbon.lowes.com/sse

# Verify network connectivity
docker exec sre-agent ping mcp-elasticsearch-stage.sadc-tlmy-stg01.carbon.lowes.com
```

#### 2. API Key Issues
```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test OpenAI API
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

#### 3. Docker Issues
```bash
# Check container status
docker ps -a

# View container logs
docker logs sre-agent

# Restart services
docker-compose restart
```

#### 4. Performance Issues
```bash
# Check resource usage
docker stats sre-agent

# Monitor API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
docker-compose up -d

# View detailed logs
docker-compose logs -f sre-agent
```

## 📚 Additional Resources

### Documentation
- [agno Framework Documentation](https://github.com/agno-agi/agno)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)

### Architecture
- [System Architecture Diagram](https://app.eraser.io/workspace/TXlvKwP25tLWjFXgKHzI?origin=share)

### Support
- **Issues**: Create an issue on GitHub
- **Documentation**: Check the docs folder
- **Examples**: See the examples folder
- **Community**: Join our Discord/Slack

## 🎯 Use Cases

### 1. Proactive Monitoring
- Continuous health checks across all services
- Early detection of potential issues
- Automated alert correlation and prioritization

### 2. Incident Response
- Automated root cause analysis
- Multi-source data correlation
- Actionable remediation recommendations

### 3. Capacity Planning
- Trend analysis and forecasting
- Resource utilization insights
- Scaling recommendations

### 4. Post-Incident Analysis
- Automated incident report generation
- Lessons learned documentation
- Process improvement suggestions

## 🔄 Integration Examples

### Slack Integration
```python
import requests

def send_slack_alert(message):
    webhook_url = "your-slack-webhook-url"
    payload = {"text": message}
    requests.post(webhook_url, json=payload)

# Example usage
send_slack_alert("🚨 SRE Agent detected critical issue: High error rate on checkout service")
```

### PagerDuty Integration
```python
import requests

def create_pagerduty_incident(title, description):
    api_key = "your-pagerduty-api-key"
    headers = {
        "Authorization": f"Token token={api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "incident": {
            "type": "incident",
            "title": title,
            "service": {"id": "your-service-id"},
            "body": {"type": "incident_body", "details": description}
        }
    }
    requests.post("https://api.pagerduty.com/incidents", headers=headers, json=payload)
```

### Jira Integration
```python
from jira import JIRA

def create_jira_ticket(summary, description):
    jira = JIRA(server="your-jira-server", basic_auth=("username", "password"))
    issue_dict = {
        "project": "SRE",
        "summary": summary,
        "description": description,
        "issuetype": {"name": "Incident"}
    }
    new_issue = jira.create_issue(fields=issue_dict)
    return new_issue.key
```

---

**Built with ❤️ using [agno](https://github.com/agno-agi/agno) framework** 