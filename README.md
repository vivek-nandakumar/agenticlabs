# 🤖 SRE AI Agent with PostgreSQL Database

A comprehensive Site Reliability Engineering (SRE) AI Agent that uses natural language to query PostgreSQL databases for monitoring data, built with the Agno framework.

## 🚀 Features

### Core SRE Capabilities
- **System Health Monitoring**: Real-time CPU, memory, disk, and network metrics
- **Alert Management**: Track active alerts by severity and service
- **Incident Investigation**: Query incidents by status, severity, and service
- **Performance Analysis**: Response times, error rates, and throughput metrics
- **Automation Tracking**: Monitor automated actions and their success rates
- **Integration Support**: JIRA tickets and Slack channels for incident management

### Technical Features
- **Natural Language Processing**: Ask questions in plain English
- **PostgreSQL Integration**: Real database with sample SRE data
- **Agno Framework**: Built with modern AI agent framework
- **Interactive Dashboard**: Streamlit web interface for visualization
- **REST API**: FastAPI backend for programmatic access
- **Docker Support**: Containerized deployment ready

## 📊 Database Schema

The PostgreSQL database contains 7 tables with realistic SRE monitoring data:

| Table | Records | Description |
|-------|---------|-------------|
| `system_metrics` | 100 | CPU, memory, disk, network metrics |
| `alerts` | 50 | Active and resolved alerts |
| `incidents` | 20 | Service incidents and outages |
| `performance_metrics` | 200 | Response times and error rates |
| `automated_actions` | 30 | Automation execution logs |
| `jira_tickets` | 15 | Incident tracking tickets |
| `slack_channels` | 10 | Communication channels |

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 14+
- Docker (optional)

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/vivek-nandakumar/agenticlabs.git
cd agenticlabs
```

2. **Set up PostgreSQL:**
```bash
# Install PostgreSQL (macOS)
brew install postgresql@14
brew services start postgresql@14

# Create database
createdb sre_agent_db
```

3. **Install dependencies:**
```bash
cd agentic-sre-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. **Set up the database with sample data:**
```bash
python setup_postgres_db.py
```

## 🚀 Usage

### 1. PostgreSQL Agent (Command Line)

Run the SRE database agent:

```bash
cd agentic-sre-demo
source .venv/bin/activate
python ../simple_postgres_agent.py
```

**Available Options:**
- **Option 1**: Run demo queries (shows all capabilities)
- **Option 2**: Interactive mode (ask your own questions)
- **Option 3**: Custom query (single question)

**Example Queries:**
- "Show me the current system health metrics"
- "What are the active alerts?"
- "List all open incidents"
- "Which services have the highest error rates?"
- "Show me incidents by severity"
- "What's the average response time for each service?"

### 2. Web Dashboard

Start the Streamlit dashboard:

```bash
cd agentic-sre-demo
source .venv/bin/activate
streamlit run sre_dashboard.py
```

**Dashboard Features:**
- **Overview**: System health and key metrics
- **Monitoring**: Real-time performance data
- **Alerts**: Active alert management
- **Incidents**: Incident tracking and investigation
- **Chat**: Interactive SRE agent chat
- **Audit Logs**: Action history and compliance
- **Automated Actions**: Automation policies and execution
- **Architecture**: System architecture visualization

### 3. REST API

Start the FastAPI server:

```bash
cd agentic-sre-demo
source .venv/bin/activate
python sre_agent_api.py
```

**API Endpoints:**
- `GET /health` - System health check
- `GET /metrics` - System metrics
- `GET /alerts` - Active alerts
- `GET /incidents` - Open incidents
- `POST /chat` - Chat with SRE agent

## 🏗️ Architecture

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Dashboard │    │   REST API      │    │  PostgreSQL     │
│   (Streamlit)   │◄──►│   (FastAPI)     │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SRE Agent     │    │   Agno Tools    │    │   Sample Data   │
│   (Natural      │    │   (SQL, MCP)    │    │   (425+ records)│
│    Language)    │    └─────────────────┘    └─────────────────┘
└─────────────────┘
```

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: FastAPI (Python REST API)
- **Database**: PostgreSQL with psycopg2
- **AI Framework**: Agno (Agent framework)
- **LLM**: Ollama with Llama3.1:8b
- **Deployment**: Docker & Docker Compose
- **Monitoring**: Prometheus & Grafana (optional)

## 📈 Sample Data

The database includes realistic SRE monitoring data:

### System Metrics
- CPU usage: 20-95%
- Memory usage: 30-90%
- Disk usage: 40-85%
- Network latency: 10-500ms

### Alerts
- High CPU Usage
- Memory Leak Detected
- Service Down
- High Error Rate
- Slow Response Time
- Disk Space Low
- Network Latency High

### Incidents
- Service Outage
- Performance Degradation
- Security Alert
- Data Loss
- Infrastructure Issue
- Deployment Failure
- Third-party Service Down

### Automated Actions
- Auto-scaling
- Restart Service
- Rollback Deployment
- Clear Cache
- Update Configuration
- Create JIRA Ticket
- Create Slack Channel

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `agentic-sre-demo` directory:

```env
# Database Configuration
DB_HOST=localhost
DB_NAME=sre_agent_db
DB_USER=viveknandakumar
DB_PASSWORD=
DB_PORT=5432

# Model Configuration
MODEL_URL=http://localhost:11434
MODEL_NAME=llama3.1:8b

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Dashboard Configuration
DASHBOARD_PORT=8501
```

### Database Configuration

Update the database configuration in the scripts if needed:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'sre_agent_db',
    'user': 'viveknandakumar',
    'password': '',
    'port': 5432
}
```

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Services Included
- **sre-agent**: Main SRE agent service
- **redis**: Caching layer
- **postgres**: Database
- **prometheus**: Metrics collection
- **grafana**: Visualization
- **elasticsearch**: Log aggregation

## 🧪 Testing

### Run Tests

```bash
cd agentic-sre-demo
source .venv/bin/activate
python test_sre_agent.py
```

### Test Database Queries

```bash
# Test PostgreSQL agent
python simple_postgres_agent.py

# Choose option 1 for demo queries
```

## 📊 Monitoring

### Available Metrics

- **System Health**: CPU, memory, disk, network
- **Performance**: Response times, error rates, throughput
- **Alerts**: Severity distribution, resolution times
- **Incidents**: Status tracking, MTTR, MTBF
- **Automation**: Success rates, execution times

### Dashboard Features

- **Real-time Monitoring**: Live system metrics
- **Alert Management**: Visual alert status
- **Incident Tracking**: Timeline and status
- **Performance Analytics**: Response time trends
- **Automation Insights**: Success/failure rates

## 🔮 Future Enhancements

### Planned Features
- **Machine Learning**: Predictive analytics for incidents
- **Advanced Automation**: Self-healing capabilities
- **Multi-cloud Support**: AWS, GCP, Azure integration
- **Advanced Analytics**: Anomaly detection
- **Mobile App**: iOS/Android dashboard
- **Slack Integration**: Real-time notifications
- **JIRA Integration**: Automated ticket creation

### Technical Improvements
- **Microservices**: Service mesh architecture
- **Kubernetes**: Container orchestration
- **Observability**: Distributed tracing
- **Security**: RBAC and audit logging
- **Scalability**: Horizontal scaling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Agno Framework**: For the AI agent capabilities
- **Streamlit**: For the web dashboard
- **FastAPI**: For the REST API
- **PostgreSQL**: For the database
- **Ollama**: For the local LLM

## 📞 Support

For questions and support:
- **Issues**: [GitHub Issues](https://github.com/vivek-nandakumar/agenticlabs/issues)
- **Discussions**: [GitHub Discussions](https://github.com/vivek-nandakumar/agenticlabs/discussions)

---

**Built with ❤️ for SRE teams everywhere** 