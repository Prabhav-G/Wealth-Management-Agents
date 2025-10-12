from typing import List, Dict
from datetime import datetime
import json
from base_agent import BaseFinancialAgent
from memory_hub import MemoryHub


class PortfolioManagerAgent(BaseFinancialAgent):
    """Agent for investment strategy and asset allocation"""

    def __init__(self, name: str, role: str, llama_client, db_manager, memory_hub: MemoryHub):
        super().__init__(name, role, llama_client, db_manager, memory_hub)
    
    def _create_system_prompt(self) -> str:
        return """You are an expert Portfolio Manager specializing in investment strategy and asset allocation.
Your expertise includes:
- Modern Portfolio Theory and asset allocation strategies
- Risk-return optimization
- Portfolio rebalancing strategies
- Diversification across asset classes
- Investment vehicle selection (stocks, bonds, ETFs, mutual funds)
- Long-term wealth building strategies

Provide detailed, actionable investment recommendations based on client goals and risk tolerance."""
    
    def analyze_portfolio(self, portfolio_data: Dict, context: Dict) -> str:
        """Analyze existing portfolio and provide recommendations"""
        task = f"""Analyze the following portfolio and provide comprehensive recommendations:
        
Portfolio Data:
{json.dumps(portfolio_data, indent=2)}

Context:
{json.dumps(context, indent=2)}

Please provide:
1. Current allocation analysis
2. Risk-adjusted performance assessment
3. Rebalancing recommendations
4. Diversification improvements
5. Expected returns and risk metrics"""
        
        result = self.execute_task(task, {"portfolio_data": portfolio_data, "context": context})
        
        # Store analysis in MongoDB
        self.db_manager.portfolio_data.update_one(
            {"user_id": portfolio_data.get("user_id")},
            {"$set": {
                "analysis": result,
                "analyzed_at": datetime.now(),
                "portfolio_snapshot": portfolio_data
            }},
            upsert=True
        )

        # Add to episodic memory
        self.memory_hub.episodic.add_event(
            client_id=portfolio_data.get("user_id"),
            transcript=result,
            agent_source=self.name,
            event_type="portfolio_analysis"
        )
        
        return result


class TaxOptimizationAgent(BaseFinancialAgent):
    """Agent for tax-loss harvesting and tax-efficient strategies"""

    def __init__(self, name: str, role: str, llama_client, db_manager, memory_hub: MemoryHub):
        super().__init__(name, role, llama_client, db_manager, memory_hub)
    
    def _create_system_prompt(self) -> str:
        return """You are an expert Tax Optimization Specialist with deep knowledge of:
- Tax-loss harvesting strategies
- Capital gains and losses management
- Tax-efficient fund placement (tax-advantaged vs taxable accounts)
- Qualified dividend strategies
- Required Minimum Distribution (RMD) planning
- Tax brackets and marginal tax rate optimization
- Estate tax planning basics

Provide specific, actionable tax optimization strategies while noting that clients should consult with tax professionals."""
    
    def identify_tax_opportunities(self, portfolio: Dict, tax_info: Dict) -> str:
        """Identify tax-loss harvesting and optimization opportunities"""
        task = f"""Identify tax optimization opportunities:

Portfolio Holdings:
{json.dumps(portfolio, indent=2)}

Tax Information:
{json.dumps(tax_info, indent=2)}

Please identify:
1. Tax-loss harvesting opportunities
2. Capital gains optimization strategies
3. Asset location optimization
4. Estimated tax savings
5. Implementation timeline"""
        
        result = self.execute_task(task, {"portfolio": portfolio, "tax_info": tax_info})
        
        # Store tax analysis
        self.db_manager.tax_records.insert_one({
            "user_id": portfolio.get("user_id"),
            "analysis": result,
            "opportunities": portfolio,
            "timestamp": datetime.now()
        })

        # Add to episodic memory
        self.memory_hub.episodic.add_event(
            client_id=portfolio.get("user_id"),
            transcript=result,
            agent_source=self.name,
            event_type="tax_optimization"
        )
        
        return result


class RiskAssessmentAgent(BaseFinancialAgent):
    """Agent for risk profiling and portfolio stress testing"""

    def __init__(self, name: str, role: str, llama_client, db_manager, memory_hub: MemoryHub):
        super().__init__(name, role, llama_client, db_manager, memory_hub)
    
    def _create_system_prompt(self) -> str:
        return """You are an expert Risk Assessment Specialist with expertise in:
- Risk tolerance assessment and profiling
- Portfolio volatility analysis (standard deviation, beta, VaR)
- Stress testing and scenario analysis
- Correlation analysis across assets
- Drawdown analysis
- Risk-adjusted return metrics (Sharpe ratio, Sortino ratio)
- Black swan event preparation

Provide comprehensive risk analysis with clear explanations for non-technical clients."""
    
    def conduct_risk_assessment(self, portfolio: Dict, client_profile: Dict) -> str:
        """Conduct comprehensive risk assessment"""
        task = f"""Conduct a comprehensive risk assessment:

Portfolio:
{json.dumps(portfolio, indent=2)}

Client Profile:
{json.dumps(client_profile, indent=2)}

Please provide:
1. Risk tolerance alignment analysis
2. Portfolio volatility metrics
3. Stress test scenarios (market crash, inflation surge, recession)
4. Concentration risk assessment
5. Risk mitigation recommendations"""
        
        result = self.execute_task(task, {"portfolio": portfolio, "client_profile": client_profile})
        
        # Store risk assessment
        self.db_manager.risk_assessments.insert_one({
            "user_id": client_profile.get("user_id"),
            "assessment": result,
            "risk_score": portfolio.get("risk_score"),
            "timestamp": datetime.now()
        })

        # Add to episodic memory
        self.memory_hub.episodic.add_event(
            client_id=client_profile.get("user_id"),
            transcript=result,
            agent_source=self.name,
            event_type="risk_assessment"
        )
        
        return result


class MarketResearchAgent(BaseFinancialAgent):
    """Agent for economic trends and sector analysis"""

    def __init__(self, name: str, role: str, llama_client, db_manager, memory_hub: MemoryHub):
        super().__init__(name, role, llama_client, db_manager, memory_hub)
    
    def _create_system_prompt(self) -> str:
        return """You are an expert Market Research Analyst specializing in:
- Macroeconomic trend analysis
- Sector rotation strategies
- Industry and sector performance analysis
- Market cycle identification
- Economic indicator interpretation (GDP, inflation, unemployment, interest rates)
- Global market dynamics
- Emerging market opportunities

Provide data-driven insights and forward-looking market perspectives."""
    
    def analyze_market_trends(self, sector: str = None) -> str:
        """Analyze current market trends and provide insights"""
        task = f"""Provide current market analysis{"for the " + sector + " sector" if sector else ""}:

Please analyze:
1. Current economic environment and key trends
2. Sector performance and outlook{"(focus on " + sector + ")" if sector else ""}
3. Interest rate impact
4. Inflation considerations
5. Investment opportunities and risks
6. 6-12 month outlook"""
        
        result = self.execute_task(task, {"sector": sector, "timestamp": datetime.now().isoformat()})
        
        # Store market research
        self.db_manager.market_research.insert_one({
            "sector": sector or "general",
            "analysis": result,
            "timestamp": datetime.now()
        })

        # Add to episodic memory
        self.memory_hub.episodic.add_event(
            client_id="general",
            transcript=result,
            agent_source=self.name,
            event_type="market_research"
        )
        
        return result


class FinancialPlanningAgent(BaseFinancialAgent):
    """Agent for goal tracking and milestone planning"""

    def __init__(self, name: str, role: str, llama_client, db_manager, memory_hub: MemoryHub):
        super().__init__(name, role, llama_client, db_manager, memory_hub)
    
    def _create_system_prompt(self) -> str:
        return """You are an expert Financial Planning Specialist with expertise in:
- Comprehensive financial planning
- Goal-based investing strategies
- Retirement planning and projections
- Education funding (529 plans, etc.)
- Major purchase planning
- Cash flow analysis and budgeting
- Net worth tracking
- Milestone-based financial roadmaps

Create clear, actionable financial plans with realistic timelines and measurable milestones."""
    
    def create_financial_plan(self, client_data: Dict, goals: List[Dict], context: Dict) -> str:
        """Create comprehensive financial plan with milestones"""
        task = f"""Create a comprehensive financial plan:

Client Data:
{json.dumps(client_data, indent=2)}

Financial Goals:
{json.dumps(goals, indent=2)}

Context:
{json.dumps(context, indent=2)}

Please provide:
1. Current financial situation assessment
2. Goal prioritization and timeline
3. Savings and investment requirements
4. Milestone-based action plan
5. Progress tracking recommendations
6. Contingency planning"""
        
        result = self.execute_task(task, {"client_data": client_data, "goals": goals, "context": context})
        
        # Store financial plan
        self.db_manager.financial_plans.insert_one({
            "user_id": client_data.get("user_id"),
            "plan": result,
            "goals": goals,
            "created_at": datetime.now()
        })

        # Add to episodic memory
        self.memory_hub.episodic.add_event(
            client_id=client_data.get("user_id"),
            transcript=result,
            agent_source=self.name,
            event_type="financial_plan"
        )
        
        return result


class ComplianceAgent(BaseFinancialAgent):
    """Agent for regulatory adherence and documentation"""

    def __init__(self, name: str, role: str, llama_client, db_manager, memory_hub: MemoryHub):
        super().__init__(name, role, llama_client, db_manager, memory_hub)
    
    def _create_system_prompt(self) -> str:
        return """You are an expert Compliance Officer specializing in:
- SEC regulations and compliance
- FINRA rules and guidelines
- Fiduciary duty standards
- Investment advisor regulations
- Documentation requirements
- Risk disclosure protocols
- KYC (Know Your Customer) procedures
- Anti-money laundering (AML) compliance

Ensure all recommendations meet regulatory requirements and proper disclosures are made."""
    
    def review_recommendation(self, recommendation: Dict) -> str:
        """Review recommendations for compliance"""
        task = f"""Review the following recommendation for compliance:

Recommendation:
{json.dumps(recommendation, indent=2)}

Please verify:
1. Regulatory compliance (SEC, FINRA)
2. Appropriate risk disclosures
3. Suitability for client
4. Documentation requirements
5. Required client acknowledgments
6. Any compliance concerns or flags"""
        
        result = self.execute_task(task, {"recommendation": recommendation})
        
        # Store compliance review
        self.db_manager.compliance_logs.insert_one({
            "recommendation": recommendation,
            "review": result,
            "reviewed_at": datetime.now(),
            "status": "reviewed"
        })

        # Add to episodic memory
        self.memory_hub.episodic.add_event(
            client_id=recommendation.get("client_id"),
            transcript=result,
            agent_source=self.name,
            event_type="compliance_review"
        )
        
        return result
