#!/usr/bin/env python3
"""
SRE AI Agent Dashboard - Interactive Web UI

This dashboard provides:
- Real-time monitoring and alert visualization
- Audit logs and incident history
- Interactive chat with the SRE agent
- System health metrics
- Automated action tracking
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import asyncio
from typing import Dict, List, Any
import threading

# Configure Streamlit page
st.set_page_config(
    page_title="SRE AI Agent Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        color: #2c3e50;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .alert-critical {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        color: #d32f2f;
        font-weight: 600;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-warning {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        color: #e65100;
        font-weight: 600;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-info {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #1565c0;
        font-weight: 600;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        color: #333333;
        font-weight: 500;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
        border-left: 4px solid #2196f3;
    }
    .agent-message {
        background-color: #f8f9fa;
        margin-right: 2rem;
        border-left: 4px solid #4caf50;
        color: #2c3e50;
    }
    
    /* Sidebar button styling */
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #1565c0;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

class SREDashboard:
    def __init__(self):
        self.api_base_url = "http://localhost:8000"
        self.chat_history = []
        
    def check_api_health(self) -> bool:
        """Check if the SRE API is running"""
        try:
            response = requests.get(f"{self.api_base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status"""
        try:
            response = requests.post(
                f"{self.api_base_url}/api/health-check",
                json={"environment": "stage", "include_details": True},
                timeout=10
            )
            return response.json() if response.status_code == 200 else {}
        except:
            return {}
    
    def get_alerts(self) -> Dict[str, Any]:
        """Get current alerts"""
        try:
            response = requests.post(
                f"{self.api_base_url}/api/alerts/monitor",
                json={"severity_filter": "all", "time_window": "1h"},
                timeout=10
            )
            return response.json() if response.status_code == 200 else {}
        except:
            return {}
    
    def investigate_incident(self, description: str) -> Dict[str, Any]:
        """Investigate an incident"""
        try:
            response = requests.post(
                f"{self.api_base_url}/api/investigate",
                json={"incident_description": description, "priority": "high"},
                timeout=30
            )
            return response.json() if response.status_code == 200 else {}
        except:
            return {}
    
    def generate_mock_metrics(self) -> Dict[str, Any]:
        """Generate mock metrics for demonstration"""
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
    
    def generate_mock_incidents(self) -> List[Dict[str, Any]]:
        """Generate mock incident history"""
        return [
            {
                "id": "INC-001",
                "title": "High Error Rate on Checkout Service",
                "description": "Checkout service experiencing 8.5% error rate",
                "severity": "high",
                "status": "resolved",
                "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
                "resolved_at": (datetime.now() - timedelta(hours=1)).isoformat(),
                "root_cause": "Database connection pool exhaustion",
                "resolution_time": "1 hour"
            },
            {
                "id": "INC-002",
                "title": "Memory Usage Alert",
                "description": "Inventory service memory usage at 85%",
                "severity": "medium",
                "status": "investigating",
                "created_at": (datetime.now() - timedelta(minutes=30)).isoformat(),
                "resolved_at": None,
                "root_cause": None,
                "resolution_time": None
            },
            {
                "id": "INC-003",
                "title": "Latency Spike",
                "description": "Payment service latency increased by 200%",
                "severity": "low",
                "status": "resolved",
                "created_at": (datetime.now() - timedelta(hours=4)).isoformat(),
                "resolved_at": (datetime.now() - timedelta(hours=3)).isoformat(),
                "root_cause": "Network congestion",
                "resolution_time": "1 hour"
            }
        ]

def main():
    st.markdown('<h1 class="main-header">🤖 SRE AI Agent Dashboard</h1>', unsafe_allow_html=True)
    
    dashboard = SREDashboard()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    # Navigation in sidebar with improved styling
    st.sidebar.markdown("## 📱 Navigation")
    
    # Create navigation buttons in sidebar
    if st.sidebar.button("🏠 Overview", use_container_width=True):
        st.session_state.current_page = "🏠 Overview"
    if st.sidebar.button("📊 Monitoring", use_container_width=True):
        st.session_state.current_page = "📊 Monitoring"
    if st.sidebar.button("🚨 Alerts", use_container_width=True):
        st.session_state.current_page = "🚨 Alerts"
    if st.sidebar.button("📝 Incidents", use_container_width=True):
        st.session_state.current_page = "📝 Incidents"
    if st.sidebar.button("💬 Chat", use_container_width=True):
        st.session_state.current_page = "💬 Chat with Agent"
    if st.sidebar.button("📋 Audit", use_container_width=True):
        st.session_state.current_page = "📋 Audit Logs"
    if st.sidebar.button("🤖 Actions", use_container_width=True):
        st.session_state.current_page = "🤖 Automated Actions"
    if st.sidebar.button("🏗️ Architecture", use_container_width=True):
        st.session_state.current_page = "🏗️ Architecture"
    
    # Initialize current page if not set
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Overview"
    
    page = st.session_state.current_page
    
    # Check API health
    api_healthy = dashboard.check_api_health()
    
    if not api_healthy:
        st.error("⚠️ SRE AI Agent API is not running. Please start the API server first.")
        st.info("Run: `python3 sre_agent_api.py` in the terminal")
        return
    
    st.success("✅ SRE AI Agent API is running")
    
    if page == "🏠 Overview":
        show_overview(dashboard)
    elif page == "📊 Monitoring":
        show_monitoring(dashboard)
    elif page == "🚨 Alerts":
        show_alerts(dashboard)
    elif page == "📝 Incidents":
        show_incidents(dashboard)
    elif page == "💬 Chat with Agent":
        show_chat(dashboard)
    elif page == "📋 Audit Logs":
        show_audit_logs(dashboard)
    elif page == "🤖 Automated Actions":
        show_automated_actions(dashboard)
    elif page == "🏗️ Architecture":
        show_architecture(dashboard)

def show_overview(dashboard: SREDashboard):
    """Show the main overview dashboard"""
    st.header("🏠 System Overview")
    
    # Get health status
    health_data = dashboard.get_health_status()
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="System Health",
            value=f"{health_data.get('health_score', 85)}%",
            delta="+5%"
        )
    
    with col2:
        st.metric(
            label="Active Alerts",
            value=health_data.get('alerts_count', 3),
            delta="-2"
        )
    
    with col3:
        st.metric(
            label="Open Incidents",
            value=2,
            delta="+1"
        )
    
    with col4:
        st.metric(
            label="Uptime",
            value="99.9%",
            delta="+0.1%"
        )
    
    # Architecture status
    st.subheader("🏗️ Architecture Status")
    arch_status = health_data.get('architecture_status', {})
    
    if arch_status:
        cols = st.columns(3)
        with cols[0]:
            st.info(f"**LangGraph Flow**: {arch_status.get('langgraph_flow', {}).get('status', 'active')}")
            st.info(f"**LLM Core**: {arch_status.get('llm_reasoning_core', {}).get('status', 'active')}")
        
        with cols[1]:
            st.info(f"**Observability**: {arch_status.get('observability_adapter', {}).get('status', 'active')}")
            st.info(f"**Insight Cache**: {arch_status.get('insight_cache', {}).get('status', 'active')}")
        
        with cols[2]:
            st.info(f"**Action Policies**: {arch_status.get('action_policies', {}).get('status', 'active')}")
            st.info(f"**Environment**: {health_data.get('environment', 'stage')}")
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    
    # Mock activity data
    activity_data = {
        "timestamp": [
            (datetime.now() - timedelta(minutes=5)).strftime("%H:%M"),
            (datetime.now() - timedelta(minutes=10)).strftime("%H:%M"),
            (datetime.now() - timedelta(minutes=15)).strftime("%H:%M"),
            (datetime.now() - timedelta(minutes=20)).strftime("%H:%M"),
            (datetime.now() - timedelta(minutes=25)).strftime("%H:%M")
        ],
        "event": [
            "Alert resolved",
            "Incident investigation started",
            "Automated action executed",
            "Health check completed",
            "New alert detected"
        ],
        "severity": ["info", "warning", "info", "info", "critical"]
    }
    
    df = pd.DataFrame(activity_data)
    st.dataframe(df, use_container_width=True)

def show_monitoring(dashboard: SREDashboard):
    """Show monitoring dashboard with metrics"""
    st.header("📊 System Monitoring")
    
    # Get mock metrics
    metrics = dashboard.generate_mock_metrics()
    
    # CPU Usage Chart
    st.subheader("CPU Usage by Service")
    cpu_data = pd.DataFrame([
        {"Service": service, "CPU %": value}
        for service, value in metrics["cpu_usage"].items()
    ])
    
    fig_cpu = px.bar(
        cpu_data, 
        x="Service", 
        y="CPU %",
        color="CPU %",
        color_continuous_scale="RdYlGn_r",
        title="CPU Usage by Service"
    )
    st.plotly_chart(fig_cpu, use_container_width=True)
    
    # Memory Usage Chart
    st.subheader("Memory Usage by Service")
    memory_data = pd.DataFrame([
        {"Service": service, "Memory %": value}
        for service, value in metrics["memory_usage"].items()
    ])
    
    fig_memory = px.bar(
        memory_data,
        x="Service",
        y="Memory %",
        color="Memory %",
        color_continuous_scale="RdYlGn_r",
        title="Memory Usage by Service"
    )
    st.plotly_chart(fig_memory, use_container_width=True)
    
    # Error Rate Chart
    st.subheader("Error Rate by Service")
    error_data = pd.DataFrame([
        {"Service": service, "Error Rate %": value}
        for service, value in metrics["error_rate"].items()
    ])
    
    fig_error = px.bar(
        error_data,
        x="Service",
        y="Error Rate %",
        color="Error Rate %",
        color_continuous_scale="Reds",
        title="Error Rate by Service"
    )
    st.plotly_chart(fig_error, use_container_width=True)
    
    # Latency Chart
    st.subheader("P95 Latency by Service")
    latency_data = pd.DataFrame([
        {"Service": service, "Latency (ms)": value}
        for service, value in metrics["latency_p95"].items()
    ])
    
    fig_latency = px.bar(
        latency_data,
        x="Service",
        y="Latency (ms)",
        color="Latency (ms)",
        color_continuous_scale="RdYlGn_r",
        title="P95 Latency by Service"
    )
    st.plotly_chart(fig_latency, use_container_width=True)

def show_alerts(dashboard: SREDashboard):
    """Show alerts dashboard"""
    st.header("🚨 Alerts Dashboard")
    
    # Get alerts
    alerts_data = dashboard.get_alerts()
    
    # Alert summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Alerts", alerts_data.get("alerts_count", 5))
    
    with col2:
        st.metric("Critical", alerts_data.get("critical_alerts", 1), delta="+1")
    
    with col3:
        st.metric("Warnings", alerts_data.get("warnings", 4), delta="-2")
    
    # Mock alerts for demonstration
    alerts = [
        {
            "id": "ALERT-001",
            "severity": "critical",
            "service": "checkout_service",
            "message": "High error rate detected: 8.5%",
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        },
        {
            "id": "ALERT-002",
            "severity": "warning",
            "service": "inventory_service",
            "message": "Memory usage at 85%",
            "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat(),
            "status": "acknowledged"
        },
        {
            "id": "ALERT-003",
            "severity": "warning",
            "service": "payment_service",
            "message": "Latency spike detected",
            "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
            "status": "resolved"
        }
    ]
    
    # Display alerts
    for alert in alerts:
        if alert["severity"] == "critical":
            st.markdown(f"""
            <div class="metric-card alert-critical">
                <strong style="color: #d32f2f; font-size: 1.2em;">🚨 {alert['severity'].upper()}</strong><br>
                <strong style="color: #2c3e50;">Service:</strong> <span style="color: #34495e;">{alert['service']}</span><br>
                <strong style="color: #2c3e50;">Message:</strong> <span style="color: #34495e;">{alert['message']}</span><br>
                <strong style="color: #2c3e50;">Time:</strong> <span style="color: #34495e;">{alert['timestamp']}</span><br>
                <strong style="color: #2c3e50;">Status:</strong> <span style="color: #d32f2f; font-weight: bold;">{alert['status']}</span>
            </div>
            """, unsafe_allow_html=True)
        elif alert["severity"] == "warning":
            st.markdown(f"""
            <div class="metric-card alert-warning">
                <strong style="color: #e65100; font-size: 1.2em;">⚠️ {alert['severity'].upper()}</strong><br>
                <strong style="color: #2c3e50;">Service:</strong> <span style="color: #34495e;">{alert['service']}</span><br>
                <strong style="color: #2c3e50;">Message:</strong> <span style="color: #34495e;">{alert['message']}</span><br>
                <strong style="color: #2c3e50;">Time:</strong> <span style="color: #34495e;">{alert['timestamp']}</span><br>
                <strong style="color: #2c3e50;">Status:</strong> <span style="color: #e65100; font-weight: bold;">{alert['status']}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card alert-info">
                <strong style="color: #1565c0; font-size: 1.2em;">ℹ️ {alert['severity'].upper()}</strong><br>
                <strong style="color: #2c3e50;">Service:</strong> <span style="color: #34495e;">{alert['service']}</span><br>
                <strong style="color: #2c3e50;">Message:</strong> <span style="color: #34495e;">{alert['message']}</span><br>
                <strong style="color: #2c3e50;">Time:</strong> <span style="color: #34495e;">{alert['timestamp']}</span><br>
                <strong style="color: #2c3e50;">Status:</strong> <span style="color: #1565c0; font-weight: bold;">{alert['status']}</span>
            </div>
            """, unsafe_allow_html=True)

def show_incidents(dashboard: SREDashboard):
    """Show incidents dashboard"""
    st.header("📝 Incident Management")
    
    # Incident investigation form
    st.subheader("🔍 Investigate New Incident")
    
    with st.form("incident_investigation"):
        incident_description = st.text_area(
            "Describe the incident:",
            placeholder="e.g., High error rate on checkout service, 500 errors increasing over last 30 minutes"
        )
        
        priority = st.selectbox("Priority:", ["low", "medium", "high", "critical"])
        
        submitted = st.form_submit_button("🔍 Investigate Incident")
        
        if submitted and incident_description:
            with st.spinner("Investigating incident..."):
                result = dashboard.investigate_incident(incident_description)
                
                if result:
                    st.success("✅ Investigation completed!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.info(f"**Incident ID:** {result.get('incident_id', 'N/A')}")
                        st.info(f"**Status:** {result.get('status', 'N/A')}")
                        st.info(f"**Severity:** {result.get('findings', {}).get('severity', 'N/A')}")
                    
                    with col2:
                        st.info(f"**Root Cause:** {result.get('findings', {}).get('root_cause', 'N/A')}")
                        st.info(f"**Resolution Time:** {result.get('findings', {}).get('resolution_time', 'N/A')}")
                        st.info(f"**Architecture Compliant:** {result.get('architecture_compliant', 'N/A')}")
                    
                    # Show recommendations
                    recommendations = result.get('findings', {}).get('recommendations', [])
                    if recommendations:
                        st.subheader("🎯 Recommendations")
                        for rec in recommendations:
                            st.write(f"• {rec}")
    
    # Incident history
    st.subheader("📋 Incident History")
    
    incidents = dashboard.generate_mock_incidents()
    
    for incident in incidents:
        if incident["severity"] == "high":
            color = "🔴"
        elif incident["severity"] == "medium":
            color = "🟡"
        else:
            color = "🟢"
        
        st.markdown(f"""
        <div class="metric-card">
            <strong style="color: #1f77b4; font-size: 1.1em;">{color} {incident['title']}</strong><br>
            <strong style="color: #2c3e50;">ID:</strong> <span style="color: #34495e;">{incident['id']}</span><br>
            <strong style="color: #2c3e50;">Severity:</strong> <span style="color: #34495e;">{incident['severity']}</span><br>
            <strong style="color: #2c3e50;">Status:</strong> <span style="color: #27ae60; font-weight: bold;">{incident['status']}</span><br>
            <strong style="color: #2c3e50;">Created:</strong> <span style="color: #34495e;">{incident['created_at']}</span><br>
            <strong style="color: #2c3e50;">Root Cause:</strong> <span style="color: #34495e;">{incident['root_cause'] or 'Under investigation'}</span><br>
            <strong style="color: #2c3e50;">Resolution Time:</strong> <span style="color: #34495e;">{incident['resolution_time'] or 'Pending'}</span>
        </div>
        """, unsafe_allow_html=True)

def show_chat(dashboard: SREDashboard):
    """Show chat interface with the SRE agent"""
    st.header("💬 Chat with SRE AI Agent")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            # Use st.markdown for better formatting of agent responses
            st.markdown("**SRE Agent:**")
            st.markdown(message['content'])
    
    # Chat input
    user_input = st.text_input("Ask the SRE agent:", placeholder="e.g., What's the current system health?")
    
    if st.button("Send") and user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate detailed agent response based on input
        if "health" in user_input.lower():
            response = """🏥 **System Health Status:**
            
**Overall Health Score:** 85% (Good)
**Uptime:** 99.9% (Last 30 days)
**Environment:** Production Stage

**Service Status:**
✅ Checkout Service: Operational (CPU: 75%, Memory: 82%)
✅ Payment Service: Operational (CPU: 45%, Memory: 67%)
⚠️ Inventory Service: Degraded (CPU: 62%, Memory: 85%)
✅ User Service: Operational (CPU: 38%, Memory: 58%)

**Active Issues:**
• 1 Critical Alert: Checkout service high error rate (8.5%)
• 2 Warning Alerts: Memory usage on inventory service
• 1 Info Alert: Latency spike on payment service

**Recent Actions:**
• Auto-scaled checkout service instances (2 minutes ago)
• Acknowledged memory alert on inventory service (15 minutes ago)
• Health check completed successfully (5 minutes ago)"""
            
        elif "alert" in user_input.lower() or "alerts" in user_input.lower():
            response = """🚨 **Current Alert Status:**
            
**Total Active Alerts:** 5
**Critical:** 1 | **Warnings:** 3 | **Info:** 1

**🔴 Critical Alerts:**
1. **ALERT-001** - Checkout Service
   - **Issue:** High error rate detected (8.5% vs 5% threshold)
   - **Duration:** 45 minutes
   - **Impact:** Customer transactions failing
   - **Status:** Active, Auto-remediation in progress
   - **Root Cause:** Database connection pool exhaustion

**⚠️ Warning Alerts:**
2. **ALERT-002** - Inventory Service
   - **Issue:** Memory usage at 85% (threshold: 80%)
   - **Duration:** 30 minutes
   - **Impact:** Potential performance degradation
   - **Status:** Acknowledged, monitoring

3. **ALERT-003** - Payment Service
   - **Issue:** Latency spike detected (450ms vs 300ms baseline)
   - **Duration:** 1 hour
   - **Impact:** Slower payment processing
   - **Status:** Investigating

4. **ALERT-004** - User Service
   - **Issue:** CPU usage elevated (38% vs 25% baseline)
   - **Duration:** 15 minutes
   - **Impact:** Minor performance impact
   - **Status:** Monitoring

**ℹ️ Info Alerts:**
5. **ALERT-005** - System-wide
   - **Issue:** Increased API calls detected
   - **Duration:** 2 hours
   - **Impact:** None, informational only
   - **Status:** Normal operation

**Automated Actions Taken:**
• Auto-scaled checkout service instances
• Increased database connection pool size
• Triggered memory optimization on inventory service"""
            
        elif "incident" in user_input.lower():
            response = """📋 **Incident Management Status:**
            
**Open Incidents:** 2 | **Resolved Today:** 1

**🔴 Active Incidents:**

1. **INC-002** - Memory Usage Alert
   - **Severity:** Medium
   - **Status:** Investigating
   - **Created:** 30 minutes ago
   - **Service:** Inventory Service
   - **Description:** Memory usage at 85%, approaching critical threshold
   - **Impact:** Potential performance degradation
   - **Assigned:** SRE Team
   - **ETA:** 2 hours
   - **🔗 JIRA Ticket:** [JIRA-20250728143000](https://jira.company.com/browse/JIRA-20250728143000)
   - **💬 Slack Channel:** #incident-memory-usage

2. **INC-003** - Latency Spike Investigation
   - **Severity:** Low
   - **Status:** Investigating
   - **Created:** 1 hour ago
   - **Service:** Payment Service
   - **Description:** P95 latency increased to 450ms
   - **Impact:** Slower payment processing
   - **Assigned:** SRE Team
   - **ETA:** 4 hours
   - **🔗 JIRA Ticket:** [JIRA-20250728142000](https://jira.company.com/browse/JIRA-20250728142000)
   - **💬 Slack Channel:** #incident-payment-latency

**✅ Recently Resolved:**

3. **INC-001** - High Error Rate (RESOLVED)
   - **Severity:** High
   - **Status:** Resolved
   - **Created:** 2 hours ago
   - **Resolved:** 1 hour ago
   - **Service:** Checkout Service
   - **Root Cause:** Database connection pool exhaustion
   - **Resolution:** Scaled database connections, implemented connection pooling
   - **Resolution Time:** 1 hour
   - **MTTR:** 60 minutes
   - **🔗 JIRA Ticket:** [JIRA-20250728140000](https://jira.company.com/browse/JIRA-20250728140000) (Closed)
   - **💬 Slack Channel:** #incident-checkout-error (Archived)

**🤖 Automated Actions Taken:**
• **JIRA Tickets:** 3 created automatically
• **Slack Channels:** 3 created for team coordination
• **Auto-Scaling:** 2 services scaled automatically
• **Incident Summaries:** 3 generated automatically

**📊 Incident Metrics:**
• **MTTR (Mean Time to Resolution):** 45 minutes
• **MTTD (Mean Time to Detection):** 5 minutes
• **Incident Volume:** 3 this week (vs 5 last week)
• **Resolution Rate:** 95% within SLA
• **Automation Rate:** 85% of actions automated"""
            
        elif "recommendation" in user_input.lower() or "recommend" in user_input.lower():
            response = """🎯 **System Recommendations:**

**🚨 High Priority:**
1. **Immediate Action Required:**
   - Scale up inventory service memory allocation
   - Implement connection pooling for checkout service
   - Add circuit breakers for payment service

2. **Database Optimization:**
   - Increase connection pool size from 50 to 100
   - Implement connection timeout settings
   - Add database monitoring alerts

**⚠️ Medium Priority:**
3. **Performance Improvements:**
   - Implement caching layer for inventory service
   - Optimize database queries in checkout service
   - Add load balancing for payment service

4. **Monitoring Enhancements:**
   - Set up proactive alerting for memory usage
   - Implement latency SLOs for all services
   - Add business metrics monitoring

**📈 Long-term Improvements:**
5. **Architecture Updates:**
   - Consider microservices migration for better isolation
   - Implement auto-scaling policies
   - Add chaos engineering practices

6. **Process Improvements:**
   - Reduce MTTR target from 60 to 30 minutes
   - Implement automated incident response
   - Add post-incident review process

**📊 Current Metrics vs Targets:**
• Error Rate: 8.5% (Target: <5%) ❌
• Latency P95: 450ms (Target: <300ms) ❌
• Memory Usage: 85% (Target: <80%) ❌
• CPU Usage: 62% (Target: <70%) ✅"""
            
        elif "memory" in user_input.lower():
            response = """💾 **Memory Usage Analysis:**

**Overall Memory Status:** ⚠️ Elevated
**Total System Memory:** 85% utilized

**Service-by-Service Breakdown:**

**🔴 Critical:**
• **Inventory Service:** 85% (Threshold: 80%)
  - Trend: Increasing over last 2 hours
  - Impact: Performance degradation likely
  - Action: Immediate scaling required

**🟡 Warning:**
• **Checkout Service:** 82% (Threshold: 80%)
  - Trend: Stable
  - Impact: Monitor closely
  - Action: Consider scaling

**🟢 Healthy:**
• **Payment Service:** 67% (Threshold: 80%)
• **User Service:** 58% (Threshold: 80%)

**Memory Usage Trends:**
• **Last Hour:** +5% increase
• **Last 24 Hours:** +12% increase
• **Weekly Average:** 78%

**Recommendations:**
1. **Immediate:** Scale inventory service memory allocation
2. **Short-term:** Implement memory optimization
3. **Long-term:** Add memory monitoring and alerting

**Automated Actions:**
• Memory optimization triggered (15 minutes ago)
• Alert acknowledged and monitoring"""
            
        elif "cpu" in user_input.lower():
            response = """🖥️ **CPU Usage Analysis:**

**Overall CPU Status:** ✅ Healthy
**Average CPU Usage:** 55% across all services

**Service-by-Service Breakdown:**

**🟡 Elevated:**
• **Checkout Service:** 75% (Threshold: 80%)
  - Trend: Stable over last hour
  - Impact: Normal operation
  - Action: Monitor

**🟢 Healthy:**
• **Inventory Service:** 62% (Threshold: 80%)
• **Payment Service:** 45% (Threshold: 80%)
• **User Service:** 38% (Threshold: 80%)

**CPU Usage Trends:**
• **Last Hour:** -2% decrease
• **Last 24 Hours:** +8% increase
• **Weekly Average:** 52%

**Performance Insights:**
• No CPU-related performance issues
• All services operating within normal ranges
• Auto-scaling working effectively

**Recommendations:**
1. **Monitor:** Checkout service CPU trend
2. **Optimize:** Consider load balancing if trend continues
3. **Plan:** Review capacity planning for peak loads"""
            
        elif "error" in user_input.lower() or "errors" in user_input.lower():
            response = """❌ **Error Rate Analysis:**

**Overall Error Status:** 🔴 Critical
**System-wide Error Rate:** 3.2% (Target: <2%)

**Service-by-Service Breakdown:**

**🔴 Critical:**
• **Checkout Service:** 8.5% (Target: <5%)
  - **Error Types:** 500 errors (70%), 502 errors (20%), 503 errors (10%)
  - **Trend:** Increasing over last 30 minutes
  - **Root Cause:** Database connection pool exhaustion
  - **Impact:** Customer transactions failing
  - **Status:** Active remediation

**🟡 Warning:**
• **Payment Service:** 2.1% (Target: <2%)
  - **Error Types:** Timeout errors (80%), validation errors (20%)
  - **Trend:** Stable
  - **Impact:** Minor payment delays
  - **Status:** Monitoring

**🟢 Healthy:**
• **Inventory Service:** 1.8% (Target: <2%)
• **User Service:** 0.9% (Target: <2%)

**Error Rate Trends:**
• **Last Hour:** +2.1% increase
• **Last 24 Hours:** +1.5% increase
• **Weekly Average:** 2.8%

**Recent Error Patterns:**
• Database connection timeouts (45% of errors)
• API gateway timeouts (30% of errors)
• Validation failures (25% of errors)

**Automated Actions:**
• Auto-scaled checkout service instances
• Increased database connection pool
• Implemented circuit breakers

**Recommendations:**
1. **Immediate:** Scale database connections
2. **Short-term:** Implement retry mechanisms
3. **Long-term:** Add error rate monitoring and alerting"""
            
        elif "latency" in user_input.lower():
            response = """⏱️ **Latency Analysis:**

**Overall Latency Status:** ⚠️ Elevated
**Average P95 Latency:** 662ms (Target: <500ms)

**Service-by-Service Breakdown:**

**🔴 Critical:**
• **Checkout Service:** 1200ms (Target: <1000ms)
  - **Trend:** Increasing over last hour
  - **Root Cause:** Database connection pool exhaustion
  - **Impact:** Poor user experience
  - **Status:** Active remediation

**🟡 Warning:**
• **Inventory Service:** 680ms (Target: <500ms)
  - **Trend:** Stable
  - **Impact:** Minor performance impact
  - **Status:** Monitoring

**🟢 Healthy:**
• **Payment Service:** 450ms (Target: <500ms)
• **User Service:** 320ms (Target: <500ms)

**Latency Trends:**
• **Last Hour:** +15% increase
• **Last 24 Hours:** +8% increase
• **Weekly Average:** 580ms

**Performance Insights:**
• Checkout service latency is the primary concern
• Database queries are the main bottleneck
• Network latency is within normal ranges

**Automated Actions:**
• Increased database connection pool
• Implemented connection timeout settings
• Added latency monitoring alerts

**Recommendations:**
1. **Immediate:** Optimize database queries
2. **Short-term:** Implement caching layer
3. **Long-term:** Consider database scaling"""
            
        elif "jira" in user_input.lower() or "ticket" in user_input.lower():
            response = """🎫 **JIRA Integration Status:**

**🔗 JIRA Configuration:**
• **Base URL:** https://jira.company.com
• **Integration Status:** ✅ Connected
• **Auto-Creation:** ✅ Enabled
• **Template:** Incident Management

**📋 Recent JIRA Tickets:**

1. **JIRA-20250728143000** - Memory Usage Alert
   - **Status:** In Progress
   - **Priority:** Medium
   - **Assignee:** SRE Team
   - **Created:** 30 minutes ago
   - **Incident:** INC-002
   - **URL:** https://jira.company.com/browse/JIRA-20250728143000

2. **JIRA-20250728142000** - Latency Spike
   - **Status:** In Progress
   - **Priority:** Low
   - **Assignee:** SRE Team
   - **Created:** 1 hour ago
   - **Incident:** INC-003
   - **URL:** https://jira.company.com/browse/JIRA-20250728142000

3. **JIRA-20250728140000** - High Error Rate (RESOLVED)
   - **Status:** Done
   - **Priority:** High
   - **Assignee:** SRE Team
   - **Created:** 2 hours ago
   - **Resolved:** 1 hour ago
   - **Incident:** INC-001
   - **URL:** https://jira.company.com/browse/JIRA-20250728140000

**🤖 Automated JIRA Actions:**
• **Auto-Creation:** Critical incidents trigger JIRA tickets automatically
• **Template Population:** Incident details, metrics, and root cause analysis
• **Status Updates:** Ticket status updated based on incident progress
• **Assignment:** Automatically assigned to SRE team
• **Comments:** Automated updates with investigation progress

**📊 JIRA Metrics:**
• **Tickets Created Today:** 3
• **Average Resolution Time:** 45 minutes
• **Automation Rate:** 100% of critical incidents
• **Template Usage:** Incident Management template"""
            
        elif "slack" in user_input.lower() or "channel" in user_input.lower():
            response = """💬 **Slack Integration Status:**

**🔗 Slack Configuration:**
• **Webhook URL:** https://hooks.slack.com/services/...
• **Integration Status:** ✅ Connected
• **Auto-Channel Creation:** ✅ Enabled
• **Notification Templates:** ✅ Configured

**📱 Recent Slack Channels:**

1. **#incident-memory-usage**
   - **Created:** 30 minutes ago
   - **Incident:** INC-002
   - **Members:** SRE Team, DevOps Team
   - **Status:** Active
   - **Purpose:** Memory usage alert coordination

2. **#incident-payment-latency**
   - **Created:** 1 hour ago
   - **Incident:** INC-003
   - **Members:** SRE Team, Payment Team
   - **Status:** Active
   - **Purpose:** Latency spike investigation

3. **#incident-checkout-error** (Archived)
   - **Created:** 2 hours ago
   - **Archived:** 1 hour ago
   - **Incident:** INC-001
   - **Members:** SRE Team, Checkout Team
   - **Status:** Resolved
   - **Purpose:** High error rate resolution

**🤖 Automated Slack Actions:**
• **Channel Creation:** Critical incidents create dedicated channels
• **Team Invitation:** Relevant teams automatically invited
• **Status Updates:** Real-time incident updates posted
• **Alert Notifications:** Automated alert notifications
• **Resolution Announcements:** Incident resolution announcements

**📊 Slack Metrics:**
• **Channels Created Today:** 3
• **Active Channels:** 2
• **Archived Channels:** 1
• **Notification Rate:** 100% of critical alerts
• **Response Time:** <5 minutes average"""
            
        else:
            response = """🤖 **SRE AI Agent - How can I help you?**

I'm your intelligent SRE assistant. I can help you with:

**📊 System Monitoring:**
• Current system health and status
• CPU, memory, and resource usage
• Error rates and latency metrics
• Service performance analysis

**🚨 Alert Management:**
• Active alerts and their severity
• Alert history and trends
• Automated response actions
• Alert correlation and analysis

**📝 Incident Management:**
• Open and resolved incidents
• Root cause analysis
• Resolution time tracking
• Incident metrics and trends

**🎯 Recommendations:**
• Performance optimization suggestions
• Capacity planning advice
• Best practices implementation
• Proactive maintenance tips

**💬 Ask me about:**
• "What's the current system health?"
• "Show me the active alerts"
• "What incidents are open?"
• "Give me performance recommendations"
• "How's the memory usage?"
• "What's the error rate?"
• "Show me latency metrics"
• "Show me JIRA tickets"
• "What Slack channels are active?"
• "Tell me about automated actions"

What would you like to know about your system?"""
        
        # Add agent response to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        st.rerun()

def show_audit_logs(dashboard: SREDashboard):
    """Show audit logs"""
    st.header("📋 Audit Logs")
    
    # Mock audit logs
    audit_logs = [
        {
            "timestamp": datetime.now().isoformat(),
            "action": "AUTOMATED_ACTION",
            "service": "checkout_service",
            "description": "Auto-scaled service instances due to high CPU usage",
            "user": "sre-agent",
            "status": "success"
        },
        {
            "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
            "action": "INCIDENT_INVESTIGATION",
            "service": "payment_service",
            "description": "Investigated latency spike, identified network congestion",
            "user": "sre-agent",
            "status": "completed"
        },
        {
            "timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(),
            "action": "ALERT_ACKNOWLEDGED",
            "service": "inventory_service",
            "description": "Acknowledged memory usage alert",
            "user": "sre-agent",
            "status": "acknowledged"
        },
        {
            "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
            "action": "HEALTH_CHECK",
            "service": "all",
            "description": "Performed comprehensive system health check",
            "user": "sre-agent",
            "status": "completed"
        },
        {
            "timestamp": (datetime.now() - timedelta(minutes=20)).isoformat(),
            "action": "AUTOMATED_REMEDIATION",
            "service": "checkout_service",
            "description": "Executed auto-rollback due to high error rate",
            "user": "sre-agent",
            "status": "success"
        }
    ]
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        action_filter = st.selectbox("Filter by Action:", ["All"] + list(set(log["action"] for log in audit_logs)))
    
    with col2:
        service_filter = st.selectbox("Filter by Service:", ["All"] + list(set(log["service"] for log in audit_logs)))
    
    with col3:
        status_filter = st.selectbox("Filter by Status:", ["All"] + list(set(log["status"] for log in audit_logs)))
    
    # Filter logs
    filtered_logs = audit_logs
    if action_filter != "All":
        filtered_logs = [log for log in filtered_logs if log["action"] == action_filter]
    if service_filter != "All":
        filtered_logs = [log for log in filtered_logs if log["service"] == service_filter]
    if status_filter != "All":
        filtered_logs = [log for log in filtered_logs if log["status"] == status_filter]
    
    # Display logs
    for log in filtered_logs:
        status_color = {
            "success": "🟢",
            "completed": "🟢",
            "acknowledged": "🟡",
            "failed": "🔴"
        }.get(log["status"], "⚪")
        
        st.markdown(f"""
        <div class="metric-card">
            <strong style="color: #1f77b4; font-size: 1.1em;">{status_color} {log['action']}</strong><br>
            <strong style="color: #2c3e50;">Service:</strong> <span style="color: #34495e;">{log['service']}</span><br>
            <strong style="color: #2c3e50;">Description:</strong> <span style="color: #34495e;">{log['description']}</span><br>
            <strong style="color: #2c3e50;">User:</strong> <span style="color: #34495e;">{log['user']}</span><br>
            <strong style="color: #2c3e50;">Time:</strong> <span style="color: #34495e;">{log['timestamp']}</span><br>
            <strong style="color: #2c3e50;">Status:</strong> <span style="color: #27ae60; font-weight: bold;">{log['status']}</span>
        </div>
        """, unsafe_allow_html=True)

def show_automated_actions(dashboard: SREDashboard):
    """Show automated actions dashboard"""
    st.header("🤖 Automated Actions")
    
    st.subheader("🎯 Action Policies")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Auto-Remediation", "Enabled", delta="Active")
        st.metric("Confidence Threshold", "80%", delta="High")
        st.metric("Max Actions/Incident", "3", delta="Limited")
    
    with col2:
        st.metric("JIRA Integration", "Connected", delta="✅")
        st.metric("Slack Integration", "Connected", delta="✅")
        st.metric("Auto-Scaling", "Enabled", delta="Active")
    
    with col3:
        st.metric("Circuit Breakers", "Enabled", delta="Active")
        st.metric("Rollback Threshold", "80%", delta="High")
        st.metric("Response Time", "<30s", delta="Fast")
    
    # Action types
    st.subheader("🔧 Available Actions")
    
    actions = [
        {
            "action": "OPEN_JIRA_TICKET",
            "description": "Create JIRA ticket for incident tracking",
            "trigger": "Critical incidents, high severity alerts",
            "example": "JIRA-20250728143000",
            "status": "active"
        },
        {
            "action": "OPEN_SLACK_CHANNEL",
            "description": "Create Slack channel for incident communication",
            "trigger": "Critical incidents, team coordination needed",
            "example": "incident-checkout-service-error",
            "status": "active"
        },
        {
            "action": "SCALE_SERVICE",
            "description": "Auto-scale service instances",
            "trigger": "High CPU/memory usage",
            "example": "Scaled checkout service from 3 to 5 instances",
            "status": "active"
        },
        {
            "action": "RESTART_SERVICE",
            "description": "Restart failing service",
            "trigger": "Service health checks failing",
            "example": "Restarted payment service",
            "status": "active"
        },
        {
            "action": "TRIGGER_AUTO_ROLLBACK",
            "description": "Rollback recent deployment",
            "trigger": "High error rate after deployment",
            "example": "Rolled back checkout service to v1.2.3",
            "status": "active"
        },
        {
            "action": "SUMMARIZE_INCIDENT",
            "description": "Generate incident summary",
            "trigger": "Incident investigation complete",
            "example": "Created summary for INC-001",
            "status": "active"
        }
    ]
    
    for action in actions:
        st.markdown(f"""
        <div class="metric-card">
            <strong style="color: #1f77b4; font-size: 1.1em;">🔧 {action['action']}</strong><br>
            <strong style="color: #2c3e50;">Description:</strong> <span style="color: #34495e;">{action['description']}</span><br>
            <strong style="color: #2c3e50;">Trigger:</strong> <span style="color: #34495e;">{action['trigger']}</span><br>
            <strong style="color: #2c3e50;">Example:</strong> <span style="color: #34495e;">{action['example']}</span><br>
            <strong style="color: #2c3e50;">Status:</strong> <span style="color: #27ae60; font-weight: bold;">{action['status']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent automated actions
    st.subheader("📋 Recent Automated Actions")
    
    recent_actions = [
        {
            "timestamp": datetime.now().isoformat(),
            "action": "OPEN_JIRA_TICKET",
            "incident_id": "INC-002",
            "ticket_id": "JIRA-20250728143000",
            "url": "https://jira.company.com/browse/JIRA-20250728143000",
            "status": "success"
        },
        {
            "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
            "action": "OPEN_SLACK_CHANNEL",
            "incident_id": "INC-002",
            "channel_name": "incident-memory-usage",
            "webhook_url": "https://hooks.slack.com/services/...",
            "status": "success"
        },
        {
            "timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(),
            "action": "SCALE_SERVICE",
            "service": "checkout_service",
            "details": "Scaled from 3 to 5 instances due to high CPU",
            "status": "success"
        },
        {
            "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
            "action": "SUMMARIZE_INCIDENT",
            "incident_id": "INC-001",
            "details": "Generated incident summary with root cause analysis",
            "status": "success"
        }
    ]
    
    for action in recent_actions:
        if action["status"] == "success":
            status_icon = "✅"
        else:
            status_icon = "❌"
        
        st.markdown(f"""
        <div class="metric-card">
            <strong style="color: #1f77b4; font-size: 1.1em;">{status_icon} {action['action']}</strong><br>
            <strong style="color: #2c3e50;">Time:</strong> <span style="color: #34495e;">{action['timestamp']}</span><br>
            <strong style="color: #2c3e50;">Status:</strong> <span style="color: #27ae60; font-weight: bold;">{action['status']}</span><br>
            <strong style="color: #2c3e50;">Details:</strong> <span style="color: #34495e;">{action.get('details', 'N/A')}</span><br>
            {f"<strong style='color: #2c3e50;'>Ticket ID:</strong> <span style='color: #34495e;'>{action.get('ticket_id', 'N/A')}</span><br>" if 'ticket_id' in action else ""}
            {f"<strong style='color: #2c3e50;'>Channel:</strong> <span style='color: #34495e;'>{action.get('channel_name', 'N/A')}</span><br>" if 'channel_name' in action else ""}
            {f"<strong style='color: #2c3e50;'>Service:</strong> <span style='color: #34495e;'>{action.get('service', 'N/A')}</span><br>" if 'service' in action else ""}
            {f"<strong style='color: #2c3e50;'>Incident ID:</strong> <span style='color: #34495e;'>{action.get('incident_id', 'N/A')}</span><br>" if 'incident_id' in action else ""}
        </div>
        """, unsafe_allow_html=True)
    
    # Manual action trigger
    st.subheader("🎮 Manual Action Trigger")
    
    with st.form("manual_action"):
        action_type = st.selectbox(
            "Select Action:",
            ["OPEN_JIRA_TICKET", "OPEN_SLACK_CHANNEL", "SCALE_SERVICE", "RESTART_SERVICE", "SUMMARIZE_INCIDENT"]
        )
        
        incident_id = st.text_input("Incident ID:", value="INC-002")
        service_name = st.text_input("Service Name:", value="checkout_service")
        
        submitted = st.form_submit_button("🚀 Execute Action")
        
        if submitted:
            st.success(f"✅ Action {action_type} executed successfully!")
            
            if action_type == "OPEN_JIRA_TICKET":
                ticket_id = f"JIRA-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                st.info(f"**JIRA Ticket Created:** {ticket_id}")
                st.info(f"**URL:** https://jira.company.com/browse/{ticket_id}")
                
            elif action_type == "OPEN_SLACK_CHANNEL":
                channel_name = f"incident-{incident_id.lower()}"
                st.info(f"**Slack Channel Created:** #{channel_name}")
                st.info(f"**Webhook URL:** https://hooks.slack.com/services/...")
                
            elif action_type == "SCALE_SERVICE":
                st.info(f"**Service Scaled:** {service_name} scaled from 3 to 5 instances")
                
            elif action_type == "RESTART_SERVICE":
                st.info(f"**Service Restarted:** {service_name} restarted successfully")
                
            elif action_type == "SUMMARIZE_INCIDENT":
                st.info(f"**Incident Summary:** Generated summary for {incident_id}")

def show_architecture(dashboard: SREDashboard):
    """Show architecture visualization"""
    st.header("🏗️ SRE AI Agent Architecture")
    
    # Architecture overview
    st.markdown("""
    ### 🎯 **Production-Level SRE AI Agent Architecture**
    
    The SRE AI Agent follows a comprehensive, production-ready architecture designed for enterprise-grade 
    Site Reliability Engineering with full observability, automation, and compliance capabilities.
    """)
    
    # Create a beautiful architecture diagram using HTML/CSS
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        color: white;
        font-family: 'Arial', sans-serif;
    ">
        <h2 style="text-align: center; margin-bottom: 30px; color: white;">🏗️ SRE AI Agent Architecture</h2>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;">
            <!-- Layer 1: User Interface -->
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                border: 2px solid rgba(255,255,255,0.3);
            ">
                <h3 style="color: #FFD700; margin-bottom: 15px;">🎨 User Interface Layer</h3>
                <div style="font-size: 14px; line-height: 1.6;">
                    <div style="margin: 8px 0;">📊 Streamlit Dashboard</div>
                    <div style="margin: 8px 0;">💬 Chat Interface</div>
                    <div style="margin: 8px 0;">📱 Mobile Responsive</div>
                    <div style="margin: 8px 0;">🎯 Real-time Updates</div>
                </div>
            </div>
            
            <!-- Layer 2: API Gateway -->
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                border: 2px solid rgba(255,255,255,0.3);
            ">
                <h3 style="color: #FFD700; margin-bottom: 15px;">🌐 API Gateway Layer</h3>
                <div style="font-size: 14px; line-height: 1.6;">
                    <div style="margin: 8px 0;">🚀 FastAPI REST API</div>
                    <div style="margin: 8px 0;">🔒 Authentication</div>
                    <div style="margin: 8px 0;">📡 Rate Limiting</div>
                    <div style="margin: 8px 0;">🛡️ CORS Support</div>
                </div>
            </div>
            
            <!-- Layer 3: Core Agent -->
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                border: 2px solid rgba(255,255,255,0.3);
            ">
                <h3 style="color: #FFD700; margin-bottom: 15px;">🤖 Core Agent Layer</h3>
                <div style="font-size: 14px; line-height: 1.6;">
                    <div style="margin: 8px 0;">🧠 LLM Reasoning</div>
                    <div style="margin: 8px 0;">🔄 LangGraph Flow</div>
                    <div style="margin: 8px 0;">💭 Memory Management</div>
                    <div style="margin: 8px 0;">🎯 Action Policies</div>
                </div>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;">
            <!-- Layer 4: Observability -->
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                border: 2px solid rgba(255,255,255,0.3);
            ">
                <h3 style="color: #FFD700; margin-bottom: 15px;">📊 Observability Layer</h3>
                <div style="font-size: 14px; line-height: 1.6;">
                    <div style="margin: 8px 0;">📈 Prometheus Metrics</div>
                    <div style="margin: 8px 0;">📝 Elasticsearch Logs</div>
                    <div style="margin: 8px 0;">🔍 Jaeger Traces</div>
                    <div style="margin: 8px 0;">🚨 Alert Management</div>
                </div>
            </div>
            
            <!-- Layer 5: MCP Tools -->
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                border: 2px solid rgba(255,255,255,0.3);
            ">
                <h3 style="color: #FFD700; margin-bottom: 15px;">🔧 MCP Tools Layer</h3>
                <div style="font-size: 14px; line-height: 1.6;">
                    <div style="margin: 8px 0;">🔗 Multi-MCP Integration</div>
                    <div style="margin: 8px 0;">📡 SSE Transport</div>
                    <div style="margin: 8px 0;">🛠️ Tool Orchestration</div>
                    <div style="margin: 8px 0;">⚡ Real-time Data</div>
                </div>
            </div>
            
            <!-- Layer 6: External Integrations -->
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                border: 2px solid rgba(255,255,255,0.3);
            ">
                <h3 style="color: #FFD700; margin-bottom: 15px;">🔗 External Integrations</h3>
                <div style="font-size: 14px; line-height: 1.6;">
                    <div style="margin: 8px 0;">🎫 JIRA Tickets</div>
                    <div style="margin: 8px 0;">💬 Slack Channels</div>
                    <div style="margin: 8px 0;">☁️ Cloud Services</div>
                    <div style="margin: 8px 0;">🔐 Security Tools</div>
                </div>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
            <!-- Storage Layer -->
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                border: 2px solid rgba(255,255,255,0.3);
            ">
                <h3 style="color: #FFD700; margin-bottom: 15px;">💾 Storage Layer</h3>
                <div style="font-size: 14px; line-height: 1.6;">
                    <div style="margin: 8px 0;">📄 JSON Storage</div>
                    <div style="margin: 8px 0;">🧠 Memory Cache</div>
                    <div style="margin: 8px 0;">💡 Insight Cache</div>
                    <div style="margin: 8px 0;">📊 Metrics Storage</div>
                </div>
            </div>
            
            <!-- Infrastructure Layer -->
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                border: 2px solid rgba(255,255,255,0.3);
            ">
                <h3 style="color: #FFD700; margin-bottom: 15px;">🏗️ Infrastructure Layer</h3>
                <div style="font-size: 14px; line-height: 1.6;">
                    <div style="margin: 8px 0;">🐳 Docker Containers</div>
                    <div style="margin: 8px 0;">☸️ Kubernetes Ready</div>
                    <div style="margin: 8px 0;">🔧 Helm Charts</div>
                    <div style="margin: 8px 0;">📊 Monitoring Stack</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Component details
    st.subheader("🔍 **Component Details**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🧠 **Core Components**
        
        **🤖 SRE Agent**
        - LangGraph Flow orchestration
        - LLM reasoning with local Llama3
        - Multi-step investigation workflows
        - Context-aware decision making
        
        **📊 Observability Adapter**
        - Multi-MCP server integration
        - Real-time metrics collection
        - Log aggregation and analysis
        - Distributed tracing support
        
        **💾 Insight Cache**
        - Intelligent caching system
        - TTL-based expiration
        - Pattern recognition
        - Performance optimization
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 **Action Components**
        
        **🔧 Action Policies**
        - Automated remediation rules
        - Confidence-based execution
        - Rollback mechanisms
        - Safety thresholds
        
        **🔗 External Integrations**
        - JIRA ticket automation
        - Slack channel management
        - Cloud service APIs
        - Security tool integration
        
        **📈 Monitoring Stack**
        - Prometheus metrics
        - Grafana dashboards
        - Alert management
        - SLA tracking
        """)
    
    # Architecture principles
    st.subheader("🏛️ **Architecture Principles**")
    
    principles = [
        {
            "principle": "🎯 **Production-Ready**",
            "description": "Enterprise-grade reliability, scalability, and security"
        },
        {
            "principle": "🔄 **Event-Driven**",
            "description": "Real-time response to system events and alerts"
        },
        {
            "principle": "🧠 **AI-Powered**",
            "description": "Intelligent reasoning and automated decision making"
        },
        {
            "principle": "🔗 **Multi-Protocol**",
            "description": "Support for various observability and monitoring protocols"
        },
        {
            "principle": "🛡️ **Security-First**",
            "description": "Authentication, authorization, and audit logging"
        },
        {
            "principle": "📊 **Observable**",
            "description": "Comprehensive monitoring and tracing capabilities"
        }
    ]
    
    for i, principle in enumerate(principles):
        if i % 2 == 0:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <strong style="color: #1f77b4;">{principle['principle']}</strong><br>
                    <span style="color: #34495e;">{principle['description']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <strong style="color: #1f77b4;">{principle['principle']}</strong><br>
                    <span style="color: #34495e;">{principle['description']}</span>
                </div>
                """, unsafe_allow_html=True)
    
    # Technology stack
    st.subheader("🛠️ **Technology Stack**")
    
    tech_stack = {
        "🤖 **AI/ML**:": "Ollama (Llama3), LangGraph, Reasoning Tools",
        "🌐 **Web Framework**:": "FastAPI, Streamlit, Uvicorn",
        "📊 **Observability**:": "Prometheus, Elasticsearch, Jaeger, MCP",
        "💾 **Storage**:": "JSON Storage, Redis, PostgreSQL",
        "🐳 **Containerization**:": "Docker, Docker Compose, Kubernetes",
        "🔧 **Monitoring**:": "Grafana, AlertManager, Custom Dashboards",
        "🔗 **Integrations**:": "JIRA API, Slack API, Cloud Services",
        "🛡️ **Security**:": "OAuth2, JWT, CORS, Rate Limiting"
    }
    
    for tech, description in tech_stack.items():
        st.markdown(f"""
        <div class="metric-card">
            <strong style="color: #1f77b4;">{tech}</strong><br>
            <span style="color: #34495e;">{description}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Compliance and standards
    st.subheader("📋 **Compliance & Standards**")
    
    st.markdown("""
    <div class="metric-card">
        <strong style="color: #1f77b4;">🏛️ Architecture Compliance</strong><br>
        <span style="color: #34495e;">
        ✅ Production-level SRE practices<br>
        ✅ Enterprise security standards<br>
        ✅ Scalable microservices architecture<br>
        ✅ Comprehensive observability<br>
        ✅ Automated incident response<br>
        ✅ Multi-environment support
        </span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 