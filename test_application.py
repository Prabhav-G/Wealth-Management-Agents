
import os
from orchestrator import FinancialAdvisoryOrchestrator

# Note: Ensure your .env file is populated with the required API keys before running.

def run_test_analysis():
    """
    Runs a complete end-to-end test of the financial advisory orchestrator
    for a single client.
    """
    print("Starting the comprehensive financial analysis test...")

    # --- Configuration ---
    # We'll test the analysis for Alice Johnson, our young, aggressive investor.
    # This dictionary now represents the full client data required by the orchestrator.
    client_data_to_test = {
        "profile": {"name": "Alice Johnson", "age": 28, "risk_tolerance": "aggressive", "user_id": "client_101"},
        "portfolio": {"total_value": 75000, "holdings": {"stocks": 60000, "crypto": 15000}},
        "goals": [{"name": "Buy a House", "target_amount": 60000, "timeline": "5 years"}]
        # We can add tax_info here if needed by the tax agent
    }

    print(f"\nClient: {client_data_to_test['profile']['name']}")
    print(f"Client ID: {client_data_to_test['profile']['user_id']}\n")

    # --- Initialization ---
    # This creates an instance of the main orchestrator, which in turn
    # initializes all the agents and the memory hub.
    try:
        orchestrator = FinancialAdvisoryOrchestrator()
        print("Orchestrator and all agents have been initialized successfully.")
    except Exception as e:
        print(f"Error during initialization: {e}")
        print("Please ensure your .env file is correctly set up with API keys.")
        return

    # --- Execution ---
    # This is the main call that triggers the entire analysis workflow.
    # The orchestrator will coordinate the agents to perform their tasks.
    print("\nExecuting comprehensive analysis... This may take a few moments.")
    try:
        # Correctly call the 'comprehensive_analysis' method with the client_data dictionary.
        analysis_results = orchestrator.comprehensive_analysis(client_data_to_test)
        print("Analysis complete. Generating final report.")

        # --- Report Generation ---
        # The orchestrator can now generate the report from the results.
        final_report = orchestrator.generate_report(analysis_results)

    except Exception as e:
        print(f"An error occurred during the analysis: {e}")
        return

    # --- Results ---
    # Print the final markdown report to the console.
    print("\n--- Generated Financial Report ---")
    print(final_report)
    print("\n-------------------------------------")

    # The report is also saved to 'financial_report.md' by the orchestrator.
    print("\nThe full report has also been saved to 'financial_report.md'.")

if __name__ == "__main__":
    run_test_analysis()

