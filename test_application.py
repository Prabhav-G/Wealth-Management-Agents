
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
    client_id_to_test = "client_101"

    # This context simulates the initial user request or the situation that
    # triggered the analysis.
    initial_context = {
        "reason_for_analysis": "Client requested a routine annual portfolio review and check-in on financial goals.",
        "specific_focus": "Ensure portfolio alignment with aggressive risk tolerance and progress towards home ownership goal."
    }

    print(f"\nClient ID: {client_id_to_test}")
    print(f"Context: {initial_context['reason_for_analysis']}\n")

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
    # The orchestrator will coordinate the agents to perform their tasks sequentially.
    print("\nExecuting comprehensive analysis... This may take a few moments.")
    try:
        final_report = orchestrator.comprehensive_analysis(client_id_to_test, initial_context)
        print("Analysis complete. Final report has been generated.")
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
