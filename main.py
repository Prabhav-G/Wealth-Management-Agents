from orchestrator import FinancialAdvisoryOrchestrator
from datetime import datetime, timedelta

# The .env file is now loaded by the database_manager singleton
# when it is first imported.

def main():
    """Main execution function"""

    print("=" * 60)
    print("FINANCIAL ADVISORY SYSTEM - FIREWORKS AI")
    print("=" * 60)

    # Sample client data
    sample_client_data = {
        "profile": {
            "user_id": "client_001",
            "name": "John Doe",
            "age": 45,
            "income": 150000,
            "risk_tolerance": "moderate",
            "investment_timeline": "15 years"
        },
        "portfolio": {
            "user_id": "client_001",
            "total_value": 500000,
            "holdings": {
                "stocks": 300000,
                "bonds": 150000,
                "cash": 50000
            },
            "risk_score": 6.5
        },
        "tax_info": {
            "tax_bracket": "24%",
            "state": "California",
            "filing_status": "married_joint"
        },
        "goals": [
            {
                "name": "Retirement",
                "target_amount": 2000000,
                "timeline": "15 years",
                "priority": "high"
            },
            {
                "name": "College Fund",
                "target_amount": 200000,
                "timeline": "8 years",
                "priority": "medium"
            }
        ]
    }

    try:
        # Initialize orchestrator
        orchestrator = FinancialAdvisoryOrchestrator()

        # Run comprehensive analysis
        results = orchestrator.comprehensive_analysis(sample_client_data)

        # Generate report
        orchestrator.generate_report(results)

        # Demonstrate memory systems
        print("\n" + "=" * 60)
        print("DEMONSTRATING MEMORY SYSTEMS")
        print("=" * 60)

        client_id = sample_client_data["profile"]["user_id"]

        # 1. Retrieve recent events from episodic memory
        print(f"\nEpisodic Memory - Retrieving recent events for client '{client_id}'...")
        recent_events = orchestrator.memory_hub.episodic.retrieve_memories(
            client_id=client_id,
            query="Recent financial analysis events",
            top_k=5
        )

        print(f"\nFound {len(recent_events)} recent events:")
        for event in recent_events:
            print(f"- Event: {event.get('event_type', 'N/A')}")
            print(f"  Summary: {event.get('event_summary', '')[:120]}...")
            print(f"  Timestamp: {event.get('timestamp')}")
            print(f"  Adjusted Score: {event.get('adjusted_score', 'N/A'):.4f}")

        # 2. Get a timeline of events
        print(f"\nEpisodic Memory - Reconstructing event timeline for client '{client_id}'...")
        start_date = datetime.utcnow() - timedelta(days=1)
        end_date = datetime.utcnow()
        timeline = orchestrator.memory_hub.episodic.get_client_timeline(client_id, start_date, end_date)

        print(f"\nFound {len(timeline)} events in the last 24 hours:")
        for event in timeline:
            print(f"- {event['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - {event['event_type']} ({event['agent_source']})")

        print("\n" + "=" * 60)
        print("✓ FINANCIAL ADVISORY SYSTEM DEMO COMPLETE")
        print("=" * 60)

    except Exception as e:
        import traceback
        print(f"\n✗ Error: {e}")
        traceback.print_exc()
        print("\nPlease check:")
        print("1. Your fw_3ZhDcC6YgP5yvHmqYwiagMPx and VOYAGE_API_KEY are set in .env file")
        print("2. MongoDB is running and accessible")
        print("3. All dependencies are installed (pip install -r requirements.txt)")


if __name__ == "__main__":
    main()
