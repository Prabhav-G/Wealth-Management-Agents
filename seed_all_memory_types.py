
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Assuming environment variables are set for API keys

from database_manager import MongoDBManager
from episodic_memory import episodic_memory
from semantic_memory import memory as semantic_memory
from procedural_memory import procedural_memory

# --- Data Generation ---

def get_client_data():
    """Returns a list of synthetic client data."""
    return [
        # ... (same client data as before) ...
        {
            "client_id": "client_101",
            "profile": {"name": "Alice Johnson", "age": 28, "risk_tolerance": "aggressive"},
            "portfolio": {"total_value": 75000, "holdings": {"stocks": 60000, "crypto": 15000}},
            "goals": [{"name": "Buy a House", "target_amount": 60000, "timeline": "5 years"}]
        },
        {
            "client_id": "client_102",
            "profile": {"name": "Bob Williams", "age": 62, "risk_tolerance": "conservative"},
            "portfolio": {"total_value": 1200000, "holdings": {"bonds": 700000, "stocks": 500000}},
            "goals": [{"name": "Retirement Income", "target_amount": 60000, "timeline": "20 years"}]
        },
        {
            "client_id": "client_103",
            "profile": {"name": "Charlie Brown", "age": 45, "risk_tolerance": "moderate"},
            "portfolio": {"total_value": 850000, "holdings": {"stocks": 500000, "bonds": 350000}},
            "goals": [{"name": "Children's Education", "target_amount": 300000, "timeline": "10 years"}]
        }
    ]

def get_episodic_data(clients):
    """Generates a list of synthetic episodic events."""
    events = []
    for i, client in enumerate(clients):
        client_id = client["client_id"]
        base_time = datetime.now() - timedelta(days=30 * (i + 1))
        events.extend([
            {"client_id": client_id, "event_type": "client_onboarding", "transcript": f"Initial onboarding discussion with {client['profile']['name']}.", "timestamp": base_time},
            {"client_id": client_id, "event_type": "portfolio_creation", "transcript": "Initial portfolio was set up based on risk tolerance.", "timestamp": base_time + timedelta(days=2)},
            {"client_id": client_id, "event_type": "goal_setting", "transcript": "Financial goals were defined and prioritized.", "timestamp": base_time + timedelta(days=3)},
            {"client_id": client_id, "event_type": "market_update", "transcript": "Discussed recent market volatility and its impact on the portfolio.", "timestamp": base_time + timedelta(days=15)}
        ])
    return events

def get_procedural_data():
    """Generates a list of synthetic procedural memories."""
    return [
        {"procedure_name": "new_client_onboarding", "steps": ["Collect client profile", "Assess risk tolerance", "Define initial financial goals", "Propose initial portfolio allocation"], "description": "Standard procedure for onboarding a new client."},
        {"procedure_name": "quarterly_portfolio_review", "steps": ["Analyze portfolio performance", "Review asset allocation", "Check goal alignment", "Propose rebalancing if necessary"], "description": "Procedure for conducting a quarterly review of a client's portfolio."},
        {"procedure_name": "risk_tolerance_reassessment", "steps": ["Administer risk tolerance questionnaire", "Discuss changes in financial situation", "Update client profile", "Adjust portfolio strategy accordingly"], "description": "Procedure to reassess a client's risk tolerance, typically done annually or after major life events."},
        {"procedure_name": "tax_loss_harvesting", "steps": ["Identify assets with unrealized losses", "Verify against 'wash sale' rules", "Sell assets to realize loss", "Reinvest proceeds in a similar but not identical asset"], "description": "Procedure for harvesting tax losses to offset capital gains."},
        {"procedure_name": "retirement_planning_initial", "steps": ["Gather retirement goals and timeline", "Project future expenses", "Analyze current savings rate", "Develop a long-term investment plan"], "description": "Initial procedure for creating a comprehensive retirement plan."},
        {"procedure_name": "education_fund_setup", "steps": ["Estimate future education costs", "Select appropriate savings vehicle (e.g., 529 plan)", "Establish contribution plan", "Select investment options within the plan"], "description": "Procedure for setting up an education savings fund."},
        {"procedure_name": "major_purchase_goal_planning", "steps": ["Define target purchase amount and date", "Calculate required savings rate", "Recommend a suitable savings/investment strategy", "Set up automated contributions"], "description": "Procedure for planning and saving for a major purchase like a house or car."},
        {"procedure_name": "client_offboarding", "steps": ["Finalize all transactions", "Prepare final performance reports", "Transfer assets to new custodian if required", "Archive client records"], "description": "Standard procedure for offboarding a client."},
        {"procedure_name": "compliance_review_of_recommendation", "steps": ["Verify recommendation aligns with client's risk profile", "Check for appropriate disclosures", "Ensure recommendation is suitable and documented", "Log the review for audit purposes"], "description": "Procedure for ensuring a financial recommendation meets compliance standards."},
        {"procedure_name": "asset_allocation_for_aggressive_investor", "steps": ["Allocate 70-80% to equities", "Allocate 10-20% to growth assets like crypto/tech", "Allocate 0-10% to bonds/cash", "Review allocation quarterly"], "description": "A model asset allocation procedure for clients with an aggressive risk tolerance."},
    ]

# --- Seeding Logic ---

def seed_database():
    """Clears and seeds all three memory types in the database."""
    print("Starting database seeding process...")
    db_manager = MongoDBManager()
    client_ids = ["client_101", "client_102", "client_103"]

    # 1. Clear existing data
    print("Clearing existing synthetic data...")
    db_manager.db.semantic_memories.delete_many({"client_id": {"$in": client_ids}})
    db_manager.db.episodic_memories.delete_many({"client_id": {"$in": client_ids}})
    db_manager.db.procedural_memories.delete_many({})
    print("Cleanup complete.")

    # 2. Seed Semantic Memory
    print("\n--- Seeding Semantic Memory ---")
    clients = get_client_data()
    count = 0
    for client in clients:
        for mem_type in ["profile", "portfolio", "goals"]:
            if isinstance(client[mem_type], list):
                for item in client[mem_type]:
                    semantic_memory.create_semantic_memory(client["client_id"], mem_type, item)
                    print(f"  + Created memory: {client['client_id']} - {mem_type}")
                    count += 1
            else:
                semantic_memory.create_semantic_memory(client["client_id"], mem_type, client[mem_type])
                print(f"  + Created memory: {client['client_id']} - {mem_type}")
                count += 1
    print(f"Seeded {count} semantic memories.")

    # 3. Seed Episodic Memory
    print("\n--- Seeding Episodic Memory ---")
    events = get_episodic_data(clients)
    episodic_memory_manager = episodic_memory.EpisodicMemory(db_manager)
    for event in events:
        episodic_memory_manager.add_event(
            client_id=event["client_id"],
            event_type=event["event_type"],
            transcript=event["transcript"],
            timestamp=event["timestamp"]
        )
        print(f"  + Logged event: {event['client_id']} - {event['event_type']}")
    print(f"Seeded {len(events)} episodic memories.")

    # 4. Seed Procedural Memory
    print("\n--- Seeding Procedural Memory ---")
    procedures = get_procedural_data()
    for proc in procedures:
        procedural_memory.create_procedure(
            procedure_name=proc["procedure_name"],
            steps=proc["steps"],
            description=proc["description"]
        )
        print(f"  + Learned procedure: {proc['procedure_name']}")
    print(f"Seeded {len(procedures)} procedural memories.")

    print("\nDatabase seeding complete!")

if __name__ == "__main__":
    # Ensure your .env file is set up before running.
    seed_database()
