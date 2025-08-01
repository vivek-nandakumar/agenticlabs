#!/usr/bin/env python3
"""
Setup PostgreSQL database with sample data for SRE AI Agent
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import random
from datetime import datetime, timedelta
import json

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'sre_agent_db',
    'user': 'viveknandakumar',  # Your system username
    'password': '',  # No password for local setup
    'port': 5432
}

def create_tables(cursor):
    """Create tables for SRE monitoring data"""
    
    # System metrics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_metrics (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT NOW(),
            cpu_usage DECIMAL(5,2),
            memory_usage DECIMAL(5,2),
            disk_usage DECIMAL(5,2),
            network_latency DECIMAL(10,2),
            service_name VARCHAR(100),
            environment VARCHAR(20)
        )
    """)
    
    # Alerts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT NOW(),
            alert_name VARCHAR(200),
            severity VARCHAR(20),
            status VARCHAR(20),
            description TEXT,
            service_name VARCHAR(100),
            environment VARCHAR(20)
        )
    """)
    
    # Incidents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id SERIAL PRIMARY KEY,
            incident_id VARCHAR(50),
            title VARCHAR(200),
            description TEXT,
            severity VARCHAR(20),
            status VARCHAR(20),
            created_at TIMESTAMP DEFAULT NOW(),
            resolved_at TIMESTAMP,
            assigned_to VARCHAR(100),
            service_name VARCHAR(100),
            environment VARCHAR(20)
        )
    """)
    
    # Performance metrics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT NOW(),
            service_name VARCHAR(100),
            endpoint VARCHAR(200),
            response_time DECIMAL(10,2),
            error_rate DECIMAL(5,2),
            throughput DECIMAL(10,2),
            environment VARCHAR(20)
        )
    """)
    
    # Automated actions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automated_actions (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT NOW(),
            action_type VARCHAR(100),
            description TEXT,
            status VARCHAR(20),
            incident_id VARCHAR(50),
            service_name VARCHAR(100),
            environment VARCHAR(20)
        )
    """)
    
    # JIRA tickets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jira_tickets (
            id SERIAL PRIMARY KEY,
            ticket_id VARCHAR(50),
            title VARCHAR(200),
            description TEXT,
            priority VARCHAR(20),
            status VARCHAR(20),
            created_at TIMESTAMP DEFAULT NOW(),
            resolved_at TIMESTAMP,
            assignee VARCHAR(100),
            incident_id VARCHAR(50)
        )
    """)
    
    # Slack channels table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS slack_channels (
            id SERIAL PRIMARY KEY,
            channel_name VARCHAR(100),
            channel_id VARCHAR(50),
            created_at TIMESTAMP DEFAULT NOW(),
            incident_id VARCHAR(50),
            status VARCHAR(20)
        )
    """)

def insert_sample_data(cursor):
    """Insert sample data into all tables"""
    
    # Sample services and environments
    services = ['web-api', 'auth-service', 'payment-gateway', 'user-service', 'notification-service']
    environments = ['production', 'staging', 'development']
    severities = ['critical', 'high', 'medium', 'low']
    statuses = ['open', 'resolved', 'in_progress', 'closed']
    
    # Insert system metrics (last 24 hours)
    print("Inserting system metrics...")
    for i in range(100):
        timestamp = datetime.now() - timedelta(hours=i)
        cursor.execute("""
            INSERT INTO system_metrics (timestamp, cpu_usage, memory_usage, disk_usage, 
                                      network_latency, service_name, environment)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            timestamp,
            random.uniform(20, 95),
            random.uniform(30, 90),
            random.uniform(40, 85),
            random.uniform(10, 500),
            random.choice(services),
            random.choice(environments)
        ))
    
    # Insert alerts
    print("Inserting alerts...")
    alert_types = [
        ('High CPU Usage', 'CPU usage exceeded 90%'),
        ('Memory Leak Detected', 'Memory usage growing steadily'),
        ('Service Down', 'Service not responding to health checks'),
        ('High Error Rate', 'Error rate exceeded 5%'),
        ('Slow Response Time', 'Response time exceeded 2 seconds'),
        ('Disk Space Low', 'Disk usage exceeded 85%'),
        ('Network Latency High', 'Network latency exceeded 200ms')
    ]
    
    for i in range(50):
        alert_type, description = random.choice(alert_types)
        cursor.execute("""
            INSERT INTO alerts (timestamp, alert_name, severity, status, description, 
                              service_name, environment)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            datetime.now() - timedelta(hours=random.randint(1, 72)),
            alert_type,
            random.choice(severities),
            random.choice(['active', 'resolved']),
            description,
            random.choice(services),
            random.choice(environments)
        ))
    
    # Insert incidents
    print("Inserting incidents...")
    incident_types = [
        ('Service Outage', 'Complete service failure affecting all users'),
        ('Performance Degradation', 'Service responding slowly to requests'),
        ('Security Alert', 'Potential security vulnerability detected'),
        ('Data Loss', 'Data corruption or loss detected'),
        ('Infrastructure Issue', 'Hardware or network infrastructure problem'),
        ('Deployment Failure', 'New deployment causing issues'),
        ('Third-party Service Down', 'External service dependency failure')
    ]
    
    for i in range(20):
        incident_type, description = random.choice(incident_types)
        created_at = datetime.now() - timedelta(hours=random.randint(1, 168))
        resolved_at = created_at + timedelta(hours=random.randint(1, 8)) if random.choice([True, False]) else None
        
        cursor.execute("""
            INSERT INTO incidents (incident_id, title, description, severity, status, 
                                created_at, resolved_at, assigned_to, service_name, environment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            f"INC-{i+1:03d}",
            incident_type,
            description,
            random.choice(severities),
            random.choice(statuses),
            created_at,
            resolved_at,
            random.choice(['SRE Team', 'DevOps Team', 'On-call Engineer']),
            random.choice(services),
            random.choice(environments)
        ))
    
    # Insert performance metrics
    print("Inserting performance metrics...")
    endpoints = [
        '/api/users', '/api/orders', '/api/payments', '/api/auth', '/api/notifications',
        '/health', '/metrics', '/api/products', '/api/cart', '/api/search'
    ]
    
    for i in range(200):
        cursor.execute("""
            INSERT INTO performance_metrics (timestamp, service_name, endpoint, 
                                          response_time, error_rate, throughput, environment)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            datetime.now() - timedelta(minutes=i*30),
            random.choice(services),
            random.choice(endpoints),
            random.uniform(50, 2000),
            random.uniform(0, 10),
            random.uniform(100, 5000),
            random.choice(environments)
        ))
    
    # Insert automated actions
    print("Inserting automated actions...")
    action_types = [
        ('Auto-scaling', 'Automatically scaled service based on load'),
        ('Restart Service', 'Automatically restarted failing service'),
        ('Rollback Deployment', 'Rolled back to previous stable version'),
        ('Clear Cache', 'Cleared application cache to resolve issues'),
        ('Update Configuration', 'Updated service configuration'),
        ('Create JIRA Ticket', 'Created incident ticket automatically'),
        ('Create Slack Channel', 'Created incident communication channel')
    ]
    
    for i in range(30):
        action_type, description = random.choice(action_types)
        cursor.execute("""
            INSERT INTO automated_actions (timestamp, action_type, description, status, 
                                        incident_id, service_name, environment)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            datetime.now() - timedelta(hours=random.randint(1, 48)),
            action_type,
            description,
            random.choice(['success', 'failed', 'in_progress']),
            f"INC-{random.randint(1, 20):03d}",
            random.choice(services),
            random.choice(environments)
        ))
    
    # Insert JIRA tickets
    print("Inserting JIRA tickets...")
    for i in range(15):
        created_at = datetime.now() - timedelta(hours=random.randint(1, 72))
        resolved_at = created_at + timedelta(hours=random.randint(2, 24)) if random.choice([True, False]) else None
        
        cursor.execute("""
            INSERT INTO jira_tickets (ticket_id, title, description, priority, status, 
                                    created_at, resolved_at, assignee, incident_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            f"JIRA-{i+1:03d}",
            f"Incident {i+1} - {random.choice(['Service Outage', 'Performance Issue', 'Security Alert'])}",
            f"Automatically created ticket for incident {i+1}",
            random.choice(['High', 'Medium', 'Low', 'Critical']),
            random.choice(['Open', 'In Progress', 'Resolved', 'Closed']),
            created_at,
            resolved_at,
            random.choice(['SRE Team', 'DevOps Engineer', 'System Admin']),
            f"INC-{random.randint(1, 20):03d}"
        ))
    
    # Insert Slack channels
    print("Inserting Slack channels...")
    for i in range(10):
        cursor.execute("""
            INSERT INTO slack_channels (channel_name, channel_id, created_at, incident_id, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            f"incident-{i+1:03d}",
            f"C{i+1:06d}",
            datetime.now() - timedelta(hours=random.randint(1, 48)),
            f"INC-{random.randint(1, 20):03d}",
            random.choice(['active', 'archived'])
        ))

def main():
    """Main function to set up the database"""
    try:
        # Connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("🗄️  Setting up PostgreSQL database for SRE AI Agent...")
        
        # Create tables
        print("📋 Creating tables...")
        create_tables(cursor)
        
        # Insert sample data
        print("📊 Inserting sample data...")
        insert_sample_data(cursor)
        
        # Verify data
        print("✅ Verifying data...")
        cursor.execute("SELECT COUNT(*) FROM system_metrics")
        metrics_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM alerts")
        alerts_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM incidents")
        incidents_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM performance_metrics")
        perf_count = cursor.fetchone()[0]
        
        print(f"""
🎉 Database setup complete!

📊 Sample data inserted:
- System Metrics: {metrics_count} records
- Alerts: {alerts_count} records  
- Incidents: {incidents_count} records
- Performance Metrics: {perf_count} records
- Automated Actions: 30 records
- JIRA Tickets: 15 records
- Slack Channels: 10 records

🔗 Database: sre_agent_db
📍 Host: localhost:5432
👤 User: {DB_CONFIG['user']}

Ready for Agno agent queries! 🚀
        """)
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 