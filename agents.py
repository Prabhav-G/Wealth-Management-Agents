from typing import List, Dict
from datetime import datetime
import json
from base_agent import BaseFinancialAgent
from memory_hub import MemoryHub


class PortfolioManagerAgent(BaseFinancialAgent):
    """Agent for investment strategy and asset allocation"""

    def __init__(self, name: str, role: str, llama_client, db_manager, memory_hub: MemoryHub):
        super().__init__(name, role, llama_client, db_manager, memory_hub)
    
    def analyze_portfolio(self, portfolio_data: Dict, context: Dict) -> str:
        """Analyze existing portfolio and provide recommendations"""
        system_prompt = """You are an expert Portfolio Manager specializing in investment strategy and asset allocation.
Your expertise includes modern portfolio theory, risk-return optimization, and diversification strategies.
Provide detailed, actionable investment recommendations."""
        
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
        
        # FIXED: Call execute_task with proper keyword arguments
        result = self.execute_task(
            prompt=task,
            system_message=system_prompt,
            max_tokens=1500,
            temperature=0.7
        )
        
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
            content=result,
            agent_source=self.name,
            event_type="portfolio_analysis"
        )
        
        return result


class TaxOptimizationAgent(BaseFinancialAgent):
    """Agent for tax-loss harvesting and tax-efficient strategies"""

    def __init__(self, name: str, role: str, llama_client, db_manager, memory_hub: MemoryHub):
        super().__init__(name, role, llama_client, db_manager, memory_hub)
    
    def identify_tax_opportunities(self, portfolio: Dict, tax_info: Dict) -> str:
        """Identify tax-loss harvesting and optimization opportunities"""
        system_prompt = """You are an expert Tax Optimization Specialist with deep knowledge of tax-loss harvesting,
capital gains management, and tax-efficient strategies. Provide specific, actionable recommendations."""
        
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
        
        result = self.execute_task(
            prompt=task,
            system_message=system_prompt,
            max_tokens=1500,
            temperature=0.6
        )
        
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
            content=result,
            agent_source=self.name,
            event_type="tax_optimization"
        )
        
        return result


class RiskAssessmentAgent(BaseFinancialAgent):
    """Agent for risk profiling and portfolio stress testing"""

    def __init__(self, name: str, role: str, llama_client, db_manager, memory_hub: MemoryHub):
        super().__init__(name, role, llama_client, db_manager, memory_hub)
    
    def conduct_risk_assessment(self, portfolio: Dict, client_profile: Dict) -> str:
        """Conduct comprehensive risk assessment"""
        system_prompt = """You are an expert Risk Assessment Specialist with expertise in portfolio volatility analysis,
stress testing, and risk-adjusted return metrics. Provide comprehensive analysis with clear explanations."""
        
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
        
        result = self.execute_task(
            prompt=task,
            system_message=system_prompt,
            max_tokens=1500,
            temperature=0.6
        )
        
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
            content=result,
            agent_source=self.name,
            event_type="risk_assessment"
        )
        
        return result


class MarketResearchAgent(BaseFinancialAgent):
    """Agent for economic trends and sector analysis"""

    def __init__(self, name: str, role: str, llama_client, db_manager, memory_hub: MemoryHub):
        super().__init__(name, role, llama_client, db_manager, memory_hub)
    
    def analyze_market_trends(self, sector: str = None) -> str:
        """Analyze current market trends and provide insights"""
        system_prompt = """You are an expert Market Research Analyst specializing in macroeconomic trends,
sector analysis, and market cycle identification. Provide data-driven insights and forward-looking perspectives."""
        
        task = f"""Provide current market analysis{"for the " + sector + " sector" if sector else ""}:

Please analyze:
1. Current economic environment and key trends
2. Sector performance and outlook{"(focus on " + sector + ")" if sector else ""}
3. Interest rate impact
4. Inflation considerations
5. Investment opportunities and risks
6. 6-12 month outlook"""
        
        result = self.execute_task(
            prompt=task,
            system_message=system_prompt,
            max_tokens=1500,
            temperature=0.7
        )
        
        # Store market research
        self.db_manager.market_research.insert_one({
            "sector": sector or "general",
            "analysis": result,
            "timestamp": datetime.now()
        })

        # Add to episodic memory (using "general" for non-client-specific research)
        self.memory_hub.episodic.add_event(
            client_id="general",
            content=result,
            agent_source=self.name,
            event_type="market_research"
        )
        
        return result


class FinancialPlanningAgent(BaseFinancialAgent):
    """Agent for goal tracking and milestone planning"""

    def __init__(self, name: str, role: str, llama_client, db_manager, memory_hub: MemoryHub):
        super().__init__(name, role, llama_client, db_manager, memory_hub)
    
    def create_financial_plan(self, client_data: Dict, goals: List[Dict], context: Dict) -> str:
        """Create comprehensive financial plan with milestones"""
        system_prompt = """You are an expert Financial Planning Specialist with expertise in goal-based investing,
retirement planning, and milestone-based financial roadmaps. Create clear, actionable plans."""
        
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
        
        result = self.execute_task(
            prompt=task,
            system_message=system_prompt,
            max_tokens=2000,
            temperature=0.7
        )
        
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
            content=result,
            agent_source=self.name,
            event_type="financial_plan"
        )
        
        return result


class ComplianceAgent(BaseFinancialAgent):
    """Agent for regulatory adherence and documentation"""

    def __init__(self, name: str, role: str, llama_client, db_manager, memory_hub: MemoryHub):
        super().__init__(name, role, llama_client, db_manager, memory_hub)
    
    def review_recommendation(self, recommendation: Dict) -> str:
        """Review recommendations for compliance"""
        system_prompt = """You are an expert Compliance Officer specializing in SEC regulations, FINRA rules,
and fiduciary duty standards. Ensure all recommendations meet regulatory requirements."""
        
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
        
        result = self.execute_task(
            prompt=task,
            system_message=system_prompt,
            max_tokens=1500,
            temperature=0.3
        )
        
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
            content=result,
            agent_source=self.name,
            event_type="compliance_review"
        )
        
        return result