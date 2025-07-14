"""
Investment Agent for real estate investment analysis and scoring.
This agent calculates key investment metrics and provides detailed financial analysis.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent
from utils.calculations import (
    calculate_investment_score,
    calculate_cap_rate,
    calculate_cash_on_cash_return,
    calculate_roi,
    calculate_max_offer_price
)
import json

class InvestmentAgent:
    def __init__(self, openai_api_key=None):
        """
        Initialize the Investment Agent.
        
        Args:
            openai_api_key (str): OpenAI API key for LLM responses
        """
        self.openai_api_key = openai_api_key
        
        # Define the agent
        self.agent = Agent(
            role="Real Estate Investment Analyst",
            goal="Analyze investment potential and calculate key financial metrics for real estate properties",
            backstory="""You are a senior real estate investment analyst with expertise in financial modeling, 
            risk assessment, and investment strategy. You have analyzed thousands of properties and helped 
            investors make profitable decisions. Your specialty is calculating accurate ROI, cap rates, and 
            cash-on-cash returns while considering market conditions, property characteristics, and investment 
            goals. You provide clear, actionable investment advice backed by solid financial analysis.""",
            verbose=True,
            allow_delegation=False,
            tools=[
                self.calculate_investment_metrics,
                self.analyze_investment_potential,
                self.calculate_offer_price,
                self.assess_investment_risk
            ],
            llm_model="gpt-3.5-turbo" if not openai_api_key else "gpt-4"
        )
    
    def calculate_investment_metrics(self, property_data):
        """
        Calculate comprehensive investment metrics for a property.
        
        Args:
            property_data (str): JSON string of property data
        
        Returns:
            str: JSON string of calculated metrics
        """
        try:
            if isinstance(property_data, str):
                property_data = json.loads(property_data)
            
            # Calculate all investment metrics
            investment_analysis = calculate_investment_score(property_data)
            
            # Add additional calculations
            annual_rental_income = property_data["rental_income"] * 12
            cap_rate = calculate_cap_rate(annual_rental_income, property_data["price"])
            
            # Calculate different scenarios
            scenarios = {
                "conservative": {
                    "down_payment": 25,
                    "interest_rate": 6.0,
                    "appreciation": 2.0
                },
                "moderate": {
                    "down_payment": 20,
                    "interest_rate": 5.5,
                    "appreciation": 3.0
                },
                "aggressive": {
                    "down_payment": 15,
                    "interest_rate": 5.0,
                    "appreciation": 4.0
                }
            }
            
            scenario_analysis = {}
            for scenario_name, params in scenarios.items():
                scenario_analysis[scenario_name] = calculate_investment_score(
                    property_data, 
                    down_payment_percent=params["down_payment"]
                )
                scenario_analysis[scenario_name]["roi"] = calculate_roi(
                    scenario_analysis[scenario_name]["metrics"]["annual_cash_flow"],
                    property_data["price"] * (params["down_payment"] / 100) + 5000,
                    params["appreciation"]
                )
            
            result = {
                "property_id": property_data["id"],
                "basic_metrics": investment_analysis,
                "scenario_analysis": scenario_analysis,
                "summary": self._generate_metrics_summary(investment_analysis, scenario_analysis)
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error calculating investment metrics: {str(e)}"
    
    def analyze_investment_potential(self, property_data, investment_goals):
        """
        Analyze investment potential based on specific goals.
        
        Args:
            property_data (str): JSON string of property data
            investment_goals (str): Investment goals (cash flow, appreciation, etc.)
        
        Returns:
            str: Investment potential analysis
        """
        try:
            if isinstance(property_data, str):
                property_data = json.loads(property_data)
            
            investment_analysis = calculate_investment_score(property_data)
            metrics = investment_analysis["metrics"]
            
            analysis = {
                "property_id": property_data["id"],
                "investment_goals": investment_goals,
                "potential_assessment": {},
                "recommendations": []
            }
            
            # Assess potential based on goals
            if "cash flow" in investment_goals.lower():
                if metrics["cash_on_cash"] >= 6:
                    analysis["potential_assessment"]["cash_flow"] = "Excellent"
                    analysis["recommendations"].append("Strong cash flow potential - suitable for income-focused investors")
                elif metrics["cash_on_cash"] >= 4:
                    analysis["potential_assessment"]["cash_flow"] = "Good"
                    analysis["recommendations"].append("Moderate cash flow - consider for balanced portfolio")
                else:
                    analysis["potential_assessment"]["cash_flow"] = "Poor"
                    analysis["recommendations"].append("Low cash flow - better for appreciation-focused strategy")
            
            if "appreciation" in investment_goals.lower():
                price_growth = property_data["market_trends"]["price_growth_1y"]
                if price_growth >= 7:
                    analysis["potential_assessment"]["appreciation"] = "Excellent"
                    analysis["recommendations"].append("Strong appreciation potential - growing market")
                elif price_growth >= 4:
                    analysis["potential_assessment"]["appreciation"] = "Good"
                    analysis["recommendations"].append("Steady appreciation expected")
                else:
                    analysis["potential_assessment"]["appreciation"] = "Limited"
                    analysis["recommendations"].append("Limited appreciation potential - focus on cash flow")
            
            if "roi" in investment_goals.lower():
                roi = investment_analysis["metrics"]["roi"]
                if roi >= 12:
                    analysis["potential_assessment"]["roi"] = "Excellent"
                    analysis["recommendations"].append("High ROI potential - strong overall returns")
                elif roi >= 8:
                    analysis["potential_assessment"]["roi"] = "Good"
                    analysis["recommendations"].append("Solid ROI - meets typical investor targets")
                else:
                    analysis["potential_assessment"]["roi"] = "Below Target"
                    analysis["recommendations"].append("ROI below typical targets - consider alternatives")
            
            # Overall assessment
            total_score = investment_analysis["total_score"]
            if total_score >= 80:
                analysis["overall_potential"] = "Excellent"
                analysis["recommendations"].append("Strong buy recommendation - meets multiple investment criteria")
            elif total_score >= 60:
                analysis["overall_potential"] = "Good"
                analysis["recommendations"].append("Good investment opportunity - worth serious consideration")
            elif total_score >= 40:
                analysis["overall_potential"] = "Fair"
                analysis["recommendations"].append("Moderate potential - proceed with caution")
            else:
                analysis["overall_potential"] = "Poor"
                analysis["recommendations"].append("Limited potential - consider other opportunities")
            
            return json.dumps(analysis, indent=2)
        except Exception as e:
            return f"Error analyzing investment potential: {str(e)}"
    
    def calculate_offer_price(self, property_data, target_returns):
        """
        Calculate optimal offer price based on target returns.
        
        Args:
            property_data (str): JSON string of property data
            target_returns (str): Target return requirements
        
        Returns:
            str: Offer price analysis
        """
        try:
            if isinstance(property_data, str):
                property_data = json.loads(property_data)
            
            # Parse target returns (simplified parsing)
            target_cap_rate = 6.5  # Default
            target_cash_on_cash = 6.0  # Default
            
            if "cap rate" in target_returns.lower():
                # Extract cap rate from string (simplified)
                if "8" in target_returns:
                    target_cap_rate = 8.0
                elif "7" in target_returns:
                    target_cap_rate = 7.0
                elif "6" in target_returns:
                    target_cap_rate = 6.0
            
            if "cash on cash" in target_returns.lower():
                # Extract cash on cash from string (simplified)
                if "8" in target_returns:
                    target_cash_on_cash = 8.0
                elif "7" in target_returns:
                    target_cash_on_cash = 7.0
                elif "6" in target_returns:
                    target_cash_on_cash = 6.0
            
            offer_analysis = calculate_max_offer_price(property_data, target_cap_rate, target_cash_on_cash)
            
            # Add negotiation strategy
            current_price = property_data["price"]
            recommended_offer = offer_analysis["recommended_max_offer"]
            
            if recommended_offer < current_price * 0.9:
                negotiation_strategy = "Aggressive - Offer significantly below asking"
            elif recommended_offer < current_price * 0.95:
                negotiation_strategy = "Moderate - Offer 5-10% below asking"
            else:
                negotiation_strategy = "Conservative - Offer close to asking price"
            
            result = {
                "property_id": property_data["id"],
                "current_price": current_price,
                "offer_analysis": offer_analysis,
                "negotiation_strategy": negotiation_strategy,
                "recommended_offer_range": {
                    "min": recommended_offer * 0.95,
                    "max": recommended_offer,
                    "optimal": recommended_offer
                }
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error calculating offer price: {str(e)}"
    
    def assess_investment_risk(self, property_data):
        """
        Assess investment risk factors for a property.
        
        Args:
            property_data (str): JSON string of property data
        
        Returns:
            str: Risk assessment analysis
        """
        try:
            if isinstance(property_data, str):
                property_data = json.loads(property_data)
            
            risk_factors = {
                "market_risk": "Low",
                "property_risk": "Low",
                "financial_risk": "Low",
                "overall_risk": "Low"
            }
            
            risk_details = {
                "market_risk_factors": [],
                "property_risk_factors": [],
                "financial_risk_factors": [],
                "mitigation_strategies": []
            }
            
            # Assess market risk
            market_trends = property_data["market_trends"]
            if market_trends["days_on_market"] > 45:
                risk_factors["market_risk"] = "High"
                risk_details["market_risk_factors"].append("Property has been on market for extended period")
            elif market_trends["days_on_market"] > 30:
                risk_factors["market_risk"] = "Medium"
                risk_details["market_risk_factors"].append("Moderate days on market")
            
            if market_trends["price_growth_1y"] < 2:
                risk_factors["market_risk"] = "Medium"
                risk_details["market_risk_factors"].append("Low price appreciation")
            
            # Assess property risk
            property_age = 2024 - property_data["year_built"]
            if property_age > 30:
                risk_factors["property_risk"] = "Medium"
                risk_details["property_risk_factors"].append("Older property may require more maintenance")
            elif property_age > 20:
                risk_factors["property_risk"] = "Low"
                risk_details["property_risk_factors"].append("Property age is reasonable")
            
            # Assess financial risk
            investment_analysis = calculate_investment_score(property_data)
            if investment_analysis["metrics"]["cash_on_cash"] < 4:
                risk_factors["financial_risk"] = "Medium"
                risk_details["financial_risk_factors"].append("Low cash-on-cash return")
            
            if investment_analysis["metrics"]["cap_rate"] < 4:
                risk_factors["financial_risk"] = "Medium"
                risk_details["financial_risk_factors"].append("Low cap rate")
            
            # Determine overall risk
            risk_scores = {"Low": 1, "Medium": 2, "High": 3}
            avg_risk_score = sum(risk_scores[risk] for risk in risk_factors.values()) / len(risk_factors)
            
            if avg_risk_score <= 1.5:
                risk_factors["overall_risk"] = "Low"
            elif avg_risk_score <= 2.5:
                risk_factors["overall_risk"] = "Medium"
            else:
                risk_factors["overall_risk"] = "High"
            
            # Generate mitigation strategies
            if risk_factors["market_risk"] != "Low":
                risk_details["mitigation_strategies"].append("Conduct thorough market research and comparable analysis")
            
            if risk_factors["property_risk"] != "Low":
                risk_details["mitigation_strategies"].append("Schedule comprehensive property inspection")
            
            if risk_factors["financial_risk"] != "Low":
                risk_details["mitigation_strategies"].append("Consider conservative financing and reserve funds")
            
            result = {
                "property_id": property_data["id"],
                "risk_assessment": risk_factors,
                "risk_details": risk_details,
                "recommendation": self._generate_risk_recommendation(risk_factors["overall_risk"])
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error assessing investment risk: {str(e)}"
    
    def _generate_metrics_summary(self, investment_analysis, scenario_analysis):
        """
        Generate a summary of investment metrics.
        
        Args:
            investment_analysis (dict): Basic investment analysis
            scenario_analysis (dict): Scenario-based analysis
        
        Returns:
            dict: Summary of key metrics
        """
        metrics = investment_analysis["metrics"]
        
        summary = {
            "investment_score": investment_analysis["total_score"],
            "grade": "A" if investment_analysis["total_score"] >= 80 else "B" if investment_analysis["total_score"] >= 60 else "C" if investment_analysis["total_score"] >= 40 else "D",
            "key_metrics": {
                "cap_rate": f"{metrics['cap_rate']:.2f}%",
                "cash_on_cash": f"{metrics['cash_on_cash']:.2f}%",
                "roi": f"{metrics['roi']:.2f}%",
                "annual_cash_flow": f"${metrics['annual_cash_flow']:,.0f}"
            },
            "best_scenario": max(scenario_analysis.keys(), key=lambda x: scenario_analysis[x]["total_score"]),
            "worst_scenario": min(scenario_analysis.keys(), key=lambda x: scenario_analysis[x]["total_score"])
        }
        
        return summary
    
    def _generate_risk_recommendation(self, overall_risk):
        """
        Generate risk-based recommendation.
        
        Args:
            overall_risk (str): Overall risk level
        
        Returns:
            str: Risk-based recommendation
        """
        if overall_risk == "Low":
            return "Property presents low risk - suitable for most investors"
        elif overall_risk == "Medium":
            return "Property has moderate risk - proceed with due diligence"
        else:
            return "Property has high risk - consider carefully or look for alternatives"
    
    def execute(self, task_description):
        """
        Execute the investment agent task.
        
        Args:
            task_description (str): Description of the task to execute
        
        Returns:
            str: Task execution result
        """
        return self.agent.execute(task_description) 