#!/usr/bin/env python3
"""
SRE AI Agent with PostgreSQL Database Querying Capabilities
Uses Agno to create an intelligent agent that can query SRE monitoring data
"""

import agno
from agno.models.ollama import Ollama
from agno.tools.sql import SQLTools
from agno.storage.postgres import PostgresStorage
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime, timedelta

class SREDatabaseAgent:
    """SRE AI Agent that can query PostgreSQL database for monitoring data"""
    
    def __init__(self):
        # Database configuration
        self.db_config = {
            'host': 'localhost',
            'database': 'sre_agent_db',
            'user': 'viveknandakumar',
            'password': '',
            'port': 5432
        }
        
        # Create SQL tool for database queries
        self.sql_tool = SQLTools(
            connection_string=f"postgresql://{self.db_config['user']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
        )
        
        # Create Agno agent with PostgreSQL capabilities
        self.agent = agno.Agent(
            model=Ollama(model="llama3.1:8b"),
            tools=[self.sql_tool],
            storage=PostgresStorage(config=agno.Config(postgres_url=f"postgresql://{self.db_config['user']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"))
        )
        
        # Sample queries for demonstration
        self.sample_queries = [
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
    
    def run_query(self, query: str):
        """Run a natural language query against the database"""
        try:
            print(f"🤖 SRE Agent: Processing query: '{query}'")
            print("=" * 60)
            
            # Run the agent with the query
            response = self.agent.run(query)
            
            print(f"📊 Results:")
            print(response.content)
            print("=" * 60)
            
            return response.content
            
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
        print("🚀 Running Demo Queries...")
        print("=" * 60)
        
        for i, query in enumerate(self.sample_queries, 1):
            print(f"\n🔍 Query {i}: {query}")
            self.run_query(query)
            print("\n" + "-" * 40)
    
    def interactive_mode(self):
        """Run the agent in interactive mode"""
        print("🤖 SRE Database Agent - Interactive Mode")
        print("=" * 50)
        print("Type your questions about the SRE monitoring data.")
        print("Examples:")
        for query in self.sample_queries[:5]:
            print(f"  • {query}")
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
    
    print("🤖 SRE Database Agent with Agno")
    print("=" * 50)
    
    # Create the agent
    agent = SREDatabaseAgent()
    
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