from typing import Dict
from datetime import datetime
# Use Gemini instead of Fireworks
from gemini_client import GeminiAIClient
# Import the centralized database manager instance
from database_manager import mongo_db_manager
from memory_hub import MemoryHub
from agents import (
    PortfolioManagerAgent,
    TaxOptimizationAgent,
    RiskAssessmentAgent,
    MarketResearchAgent,
    FinancialPlanningAgent,
    ComplianceAgent
)

class FinancialAdvisoryOrchestrator:
    """Orchestrates multi-agent collaboration for comprehensive financial advisory"""

    def __init__(self):
        """Initialize the orchestrator with all agents"""

        # Use Gemini instead of Fireworks
        self.llama_client = GeminiAIClient()  # For backwards compatibility
        # Use the pre-initialized database manager (Fastino or MongoDB)
        self.db_manager = mongo_db_manager
        self.memory_hub = MemoryHub(self.db_manager)  # Pass db_manager to MemoryHub

        # Initialize all agents with the memory hub
        self.portfolio_manager = PortfolioManagerAgent(
            name="Portfolio Manager",
            role="Investment Strategy and Asset Allocation Specialist",
            llama_client=self.llama_client,
            db_manager=self.db_manager,
            memory_hub=self.memory_hub
        )

        self.tax_optimizer = TaxOptimizationAgent(
            name="Tax Optimization Specialist",
            role="Tax-Loss Harvesting and Tax-Efficient Investment Strategist",
            llama_client=self.llama_client,
            db_manager=self.db_manager,
            memory_hub=self.memory_hub
        )

        self.risk_assessor = RiskAssessmentAgent(
            name="Risk Assessment Specialist",
            role="Risk Profiling and Portfolio Stress Testing Expert",
            llama_client=self.llama_client,
            db_manager=self.db_manager,
            memory_hub=self.memory_hub
        )

        self.market_researcher = MarketResearchAgent(
            name="Market Research Analyst",
            role="Economic Trends and Sector Analysis Expert",
            llama_client=self.llama_client,
            db_manager=self.db_manager,
            memory_hub=self.memory_hub
        )

        self.financial_planner = FinancialPlanningAgent(
            name="Financial Planning Specialist",
            role="Goal Tracking and Milestone Planning Expert",
            llama_client=self.llama_client,
            db_manager=self.db_manager,
            memory_hub=self.memory_hub
        )

        self.compliance_officer = ComplianceAgent(
            name="Compliance Officer",
            role="Regulatory Adherence and Documentation Specialist",
            llama_client=self.llama_client,
            db_manager=self.db_manager,
            memory_hub=self.memory_hub
        )

        print("✓ Financial Advisory System initialized with all 6 agents and Memory Hub")

    def comprehensive_analysis(self, client_data: Dict) -> Dict[str, str]:
        """Conduct comprehensive analysis using a collaborative, structured workflow."""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE FINANCIAL ANALYSIS - COLLABORATIVE WORKFLOW")
        print("=" * 60)

        results = {}
        context = {
            'client_profile': client_data.get('profile', {}),
            'client_portfolio': client_data.get('portfolio', {}),
            'client_goals': client_data.get('goals', []),
            'tax_info': client_data.get('tax_info', {})
        }
        client_id = context['client_profile'].get('user_id')

        # --- PHASE 1: FOUNDATIONAL INSIGHTS (Independent, Upstream) ---

        print("\n[1/6] Conducting Market Research (Context Provider)...")
        market_analysis = self.market_researcher.analyze_market_trends()
        results['market_research'] = market_analysis
        context['market_analysis'] = market_analysis
        self.memory_hub.episodic.add_event(client_id, market_analysis, agent_source="market_researcher",
                                            event_type="market_analysis")
        print("✓ Market Research complete")

        print("\n[2/6] Conducting Risk Assessment (Context Provider)...")
        risk_profile = self.risk_assessor.conduct_risk_assessment(
            portfolio=context['client_portfolio'],
            client_profile=context['client_profile']
        )
        results['risk_assessment'] = risk_profile
        context['risk_profile'] = risk_profile
        self.memory_hub.episodic.add_event(client_id, risk_profile, agent_source="risk_assessor",
                                            event_type="risk_assessment")
        print("✓ Risk Assessment complete")

        # --- PHASE 2: STRATEGY FORMULATION (Collaborative, Downstream) ---

        print("\n[3/6] Analyzing Portfolio (Using Market & Risk Context)...")
        portfolio_analysis = self.portfolio_manager.analyze_portfolio(
            portfolio_data=context['client_portfolio'],
            context=context
        )
        results['portfolio_analysis'] = portfolio_analysis
        context['portfolio_recommendations'] = portfolio_analysis
        self.memory_hub.episodic.add_event(client_id, portfolio_analysis, agent_source="portfolio_manager",
                                            event_type="portfolio_analysis")
        print("✓ Portfolio Analysis complete")

        print("\n[4/6] Creating Financial Plan (Using Risk & Portfolio Context)...")
        financial_plan = self.financial_planner.create_financial_plan(
            client_data=context['client_profile'],
            goals=context['client_goals'],
            context=context
        )
        results['financial_plan'] = financial_plan
        context['financial_plan'] = financial_plan
        self.memory_hub.episodic.add_event(client_id, financial_plan, agent_source="financial_planner",
                                            event_type="financial_planning")
        print("✓ Financial Planning complete")

        print("\n[5/6] Identifying Tax Opportunities...")
        tax_optimization = self.tax_optimizer.identify_tax_opportunities(
            portfolio=context['client_portfolio'],
            tax_info=context['tax_info']
        )
        results['tax_optimization'] = tax_optimization
        self.memory_hub.episodic.add_event(client_id, tax_optimization, agent_source="tax_optimizer",
                                            event_type="tax_optimization")
        print("✓ Tax Optimization complete")

        # --- PHASE 3: FINAL REVIEW ---

        print("\n[6/6] Performing Compliance Review...")
        final_recommendation = {
            'client_id': client_id,
            'recommendations': results
        }
        compliance_review = self.compliance_officer.review_recommendation(
            recommendation=final_recommendation
        )
        results['compliance_review'] = compliance_review
        self.memory_hub.episodic.add_event(client_id, compliance_review, agent_source="compliance_officer",
                                            event_type="compliance_review")
        print("✓ Compliance Review complete")

        print("\n" + "=" * 60)
        print("✓ COMPREHENSIVE ANALYSIS COMPLETE!")
        print("=" * 60)
        return results

    def generate_report(self, results: Dict[str, str], output_file: str = "financial_report.md"):
        """Generate comprehensive report from analysis"""
        report = f"""# Comprehensive Financial Advisory Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Risk Assessment
{results.get('risk_assessment', 'N/A')}

---

## Portfolio Analysis
{results.get('portfolio_analysis', 'N/A')}

---

## Tax Optimization Opportunities
{results.get('tax_optimization', 'N/A')}

---

## Market Research & Trends
{results.get('market_research', 'N/A')}

---

## Financial Planning
{results.get('financial_plan', 'N/A')}

---

## Compliance Review
{results.get('compliance_review', 'N/A')}

---

*This report is for informational purposes only and does not constitute financial advice. 
Please consult with licensed financial professionals before making investment decisions.*
"""

        with open(output_file, 'w') as f:
            f.write(report)

        print(f"\n✓ Report saved to {output_file}")
        return report
