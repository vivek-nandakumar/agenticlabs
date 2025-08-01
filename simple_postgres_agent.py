#!/usr/bin/env python3
"""
Simple SRE AI Agent with PostgreSQL Database Querying
Uses direct SQL queries with natural language processing
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime, timedelta
import re

class SimpleSREDatabaseAgent:
    """Simple SRE AI Agent that can query PostgreSQL database for monitoring data"""
    
    def __init__(self):
        # Database configuration
        self.db_config = {
            'host': 'localhost',
            'database': 'sre_agent_db',
            'user': 'viveknandakumar',
            'password': '',
            'port': 5432
        }
        
        # Predefined queries for common SRE questions
        self.query_patterns = {
            'system_health': {
                'keywords': ['system health', 'metrics', 'cpu', 'memory', 'disk'],
                'query': """
                    SELECT service_name, 
                           AVG(cpu_usage) as avg_cpu,
                           AVG(memory_usage) as avg_memory,
                           AVG(disk_usage) as avg_disk,
                           AVG(network_latency) as avg_latency,
                           environment
                    FROM system_metrics 
                    WHERE timestamp >= NOW() - INTERVAL '24 hours'
                    GROUP BY service_name, environment
                    ORDER BY avg_cpu DESC
                    LIMIT 10
                """
            },
            'active_alerts': {
                'keywords': ['active alerts', 'alerts', 'alert'],
                'query': """
                    SELECT alert_name, severity, status, description, 
                           service_name, environment, timestamp
                    FROM alerts 
                    WHERE status = 'active'
                    ORDER BY timestamp DESC
                    LIMIT 20
                """
            },
            'open_incidents': {
                'keywords': ['open incidents', 'incidents', 'incident'],
                'query': """
                    SELECT incident_id, title, severity, status, 
                           service_name, environment, created_at
                    FROM incidents 
                    WHERE status IN ('open', 'in_progress')
                    ORDER BY created_at DESC
                    LIMIT 15
                """
            },
            'performance_metrics': {
                'keywords': ['performance', 'response time', 'error rate', 'throughput'],
                'query': """
                    SELECT service_name, endpoint,
                           AVG(response_time) as avg_response_time,
                           AVG(error_rate) as avg_error_rate,
                           AVG(throughput) as avg_throughput,
                           environment
                    FROM performance_metrics 
                    WHERE timestamp >= NOW() - INTERVAL '1 hour'
                    GROUP BY service_name, endpoint, environment
                    ORDER BY avg_response_time DESC
                    LIMIT 10
                """
            },
            'automated_actions': {
                'keywords': ['automated actions', 'actions', 'automation'],
                'query': """
                    SELECT action_type, description, status, 
                           service_name, environment, timestamp
                    FROM automated_actions 
                    WHERE timestamp >= NOW() - INTERVAL '24 hours'
                    ORDER BY timestamp DESC
                    LIMIT 15
                """
            },
            'jira_tickets': {
                'keywords': ['jira', 'tickets', 'ticket'],
                'query': """
                    SELECT ticket_id, title, priority, status, 
                           assignee, created_at
                    FROM jira_tickets 
                    WHERE created_at >= NOW() - INTERVAL '7 days'
                    ORDER BY created_at DESC
                    LIMIT 10
                """
            },
            'slack_channels': {
                'keywords': ['slack', 'channels', 'channel'],
                'query': """
                    SELECT channel_name, status, created_at, incident_id
                    FROM slack_channels 
                    WHERE status = 'active'
                    ORDER BY created_at DESC
                    LIMIT 10
                """
            },
            'high_error_rates': {
                'keywords': ['error rate', 'high error', 'errors'],
                'query': """
                    SELECT service_name, endpoint,
                           AVG(error_rate) as avg_error_rate,
                           COUNT(*) as data_points
                    FROM performance_metrics 
                    WHERE timestamp >= NOW() - INTERVAL '6 hours'
                    GROUP BY service_name, endpoint
                    HAVING AVG(error_rate) > 2.0
                    ORDER BY avg_error_rate DESC
                    LIMIT 10
                """
            },
            'incidents_by_severity': {
                'keywords': ['severity', 'critical', 'high', 'medium', 'low'],
                'query': """
                    SELECT severity, COUNT(*) as count,
                           COUNT(CASE WHEN status = 'resolved' THEN 1 END) as resolved,
                           COUNT(CASE WHEN status IN ('open', 'in_progress') THEN 1 END) as active
                    FROM incidents 
                    WHERE created_at >= NOW() - INTERVAL '30 days'
                    GROUP BY severity
                    ORDER BY 
                        CASE severity 
                            WHEN 'critical' THEN 1 
                            WHEN 'high' THEN 2 
                            WHEN 'medium' THEN 3 
                            WHEN 'low' THEN 4 
                        END
                """
            },
            'service_response_times': {
                'keywords': ['response time', 'average response', 'latency'],
                'query': """
                    SELECT service_name,
                           AVG(response_time) as avg_response_time,
                           MIN(response_time) as min_response_time,
                           MAX(response_time) as max_response_time,
                           COUNT(*) as data_points
                    FROM performance_metrics 
                    WHERE timestamp >= NOW() - INTERVAL '24 hours'
                    GROUP BY service_name
                    ORDER BY avg_response_time DESC
                    LIMIT 10
                """
            }
        }
    
    def get_matching_query(self, user_input):
        """Find the best matching query based on user input"""
        user_input_lower = user_input.lower()
        
        best_match = None
        best_score = 0
        
        for pattern_name, pattern_data in self.query_patterns.items():
            score = 0
            for keyword in pattern_data['keywords']:
                if keyword in user_input_lower:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = pattern_name
        
        return best_match
    
    def run_query(self, user_input):
        """Run a natural language query against the database"""
        try:
            print(f"🤖 SRE Agent: Processing query: '{user_input}'")
            print("=" * 60)
            
            # Find the best matching query
            pattern_name = self.get_matching_query(user_input)
            
            if not pattern_name:
                print("❌ Sorry, I couldn't understand your query. Try asking about:")
                for pattern_name, pattern_data in self.query_patterns.items():
                    print(f"  • {', '.join(pattern_data['keywords'])}")
                return None
            
            # Execute the query
            query = self.query_patterns[pattern_name]['query']
            print(f"📊 Executing query for: {pattern_name}")
            
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            if not results:
                print("📭 No data found for this query.")
                return None
            
            # Format and display results
            print(f"📈 Found {len(results)} results:")
            print("-" * 40)
            
            for i, row in enumerate(results, 1):
                print(f"{i}. {dict(row)}")
            
            cursor.close()
            conn.close()
            
            print("=" * 60)
            return results
            
        except Exception as e:
            print(f"❌ Error running query: {e}")
            return None
    
    def get_database_info(self):
        """Get information about the database tables and data"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Get table information
            cursor.execute("""
                SELECT table_name, 
                       (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
                FROM information_schema.tables t
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            
            tables = cursor.fetchall()
            
            print("🗄️  Database Information:")
            print("=" * 40)
            
            for table_name, column_count in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
                print(f"📋 {table_name}: {row_count} rows, {column_count} columns")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"❌ Error getting database info: {e}")
    
    def run_demo_queries(self):
        """Run a series of demo queries to showcase capabilities"""
        demo_queries = [
            "Show me the current system health metrics",
            "What are the active alerts?",
            "List all open incidents",
            "Show me performance metrics for the last hour",
            "What automated actions were taken recently?",
            "Show me JIRA tickets created today",
            "What Slack channels are active?",
            "Which services have the highest error rates?",
            "Show me incidents by severity",
            "What's the average response time for each service?"
        ]
        
        print("🚀 Running Demo Queries...")
        print("=" * 60)
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n🔍 Query {i}: {query}")
            self.run_query(query)
            print("\n" + "-" * 40)
    
    def interactive_mode(self):
        """Run the agent in interactive mode"""
        print("🤖 SRE Database Agent - Interactive Mode")
        print("=" * 50)
        print("Type your questions about the SRE monitoring data.")
        print("Examples:")
        print("  • Show me the current system health metrics")
        print("  • What are the active alerts?")
        print("  • List all open incidents")
        print("  • Which services have the highest error rates?")
        print("  • Show me incidents by severity")
        print("Type 'quit' to exit")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n💬 Your question: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input:
                    self.run_query(user_input)
                else:
                    print("Please enter a question.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function to run the SRE Database Agent"""
    
    print("🤖 Simple SRE Database Agent")
    print("=" * 50)
    
    # Create the agent
    agent = SimpleSREDatabaseAgent()
    
    # Show database information
    agent.get_database_info()
    
    print("\n" + "=" * 50)
    print("Choose an option:")
    print("1. Run demo queries")
    print("2. Interactive mode")
    print("3. Custom query")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            agent.run_demo_queries()
        elif choice == "2":
            agent.interactive_mode()
        elif choice == "3":
            query = input("Enter your query: ").strip()
            if query:
                agent.run_query(query)
            else:
                print("No query provided.")
        else:
            print("Invalid choice. Running demo queries...")
            agent.run_demo_queries()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 