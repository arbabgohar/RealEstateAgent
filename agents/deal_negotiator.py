"""
Deal Negotiator Agent for real estate negotiation strategy and offer recommendations.
This agent provides negotiation tactics and optimal offer pricing strategies.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent
from utils.calculations import calculate_max_offer_price, calculate_investment_score
import json

class DealNegotiatorAgent:
    def __init__(self, openai_api_key=None):
        """
        Initialize the Deal Negotiator Agent.
        
        Args:
            openai_api_key (str): OpenAI API key for LLM responses
        """
        self.openai_api_key = openai_api_key
        
        # Define the agent
        self.agent = Agent(
            role="Real Estate Deal Negotiator",
            goal="Develop effective negotiation strategies and recommend optimal offer prices for real estate deals",
            backstory="""You are an expert real estate negotiator with over 20 years of experience closing 
            hundreds of deals. You understand market psychology, seller motivations, and negotiation tactics. 
            You specialize in creating win-win scenarios while maximizing investor returns. Your strategies 
            are based on thorough market analysis, property condition assessment, and understanding of 
            seller circumstances. You provide actionable negotiation advice that helps investors secure 
            properties at optimal prices.""",
            verbose=True,
            allow_delegation=False,
            tools=[
                self.develop_negotiation_strategy,
                self.calculate_optimal_offer,
                self.analyze_seller_motivation,
                self.generate_negotiation_script
            ],
            llm_model="gpt-3.5-turbo" if not openai_api_key else "gpt-4"
        )
    
    def develop_negotiation_strategy(self, property_data, market_conditions):
        """
        Develop a comprehensive negotiation strategy for a property.
        
        Args:
            property_data (str): JSON string of property data
            market_conditions (str): Current market conditions
        
        Returns:
            str: Negotiation strategy analysis
        """
        try:
            if isinstance(property_data, str):
                property_data = json.loads(property_data)
            
            # Analyze property and market factors
            investment_analysis = calculate_investment_score(property_data)
            market_trends = property_data["market_trends"]
            
            strategy = {
                "property_id": property_data["id"],
                "current_price": property_data["price"],
                "negotiation_approach": "",
                "key_factors": [],
                "recommended_strategy": {},
                "risk_assessment": {}
            }
            
            # Determine negotiation approach based on market conditions
            days_on_market = market_trends["days_on_market"]
            price_growth = market_trends["price_growth_1y"]
            
            if days_on_market > 60:
                strategy["negotiation_approach"] = "Aggressive"
                strategy["key_factors"].append("Property has been on market for extended period")
                strategy["key_factors"].append("Seller may be motivated to sell")
            elif days_on_market > 30:
                strategy["negotiation_approach"] = "Moderate"
                strategy["key_factors"].append("Moderate days on market")
                strategy["key_factors"].append("Room for negotiation")
            else:
                strategy["negotiation_approach"] = "Conservative"
                strategy["key_factors"].append("Property is relatively new to market")
                strategy["key_factors"].append("Seller may be less motivated")
            
            # Add market condition factors
            if price_growth > 7:
                strategy["key_factors"].append("Strong market appreciation - sellers may be less flexible")
            elif price_growth < 3:
                strategy["key_factors"].append("Slow market growth - more negotiation room")
            
            # Develop specific strategy
            if strategy["negotiation_approach"] == "Aggressive":
                strategy["recommended_strategy"] = {
                    "initial_offer": property_data["price"] * 0.85,
                    "target_price": property_data["price"] * 0.90,
                    "concessions": ["Request seller to pay closing costs", "Ask for repairs or improvements"],
                    "timeline": "Quick close (15-30 days) in exchange for lower price",
                    "leverage_points": ["Extended time on market", "Market conditions", "Property condition issues"]
                }
            elif strategy["negotiation_approach"] == "Moderate":
                strategy["recommended_strategy"] = {
                    "initial_offer": property_data["price"] * 0.92,
                    "target_price": property_data["price"] * 0.95,
                    "concessions": ["Split closing costs", "Minor repairs"],
                    "timeline": "Standard closing timeline (30-45 days)",
                    "leverage_points": ["Market comparables", "Property features", "Financing terms"]
                }
            else:  # Conservative
                strategy["recommended_strategy"] = {
                    "initial_offer": property_data["price"] * 0.96,
                    "target_price": property_data["price"] * 0.98,
                    "concessions": ["Minimal concessions", "As-is condition"],
                    "timeline": "Flexible closing timeline",
                    "leverage_points": ["Strong offer", "Quick close", "Cash offer potential"]
                }
            
            # Risk assessment
            strategy["risk_assessment"] = {
                "losing_deal_risk": "Low" if strategy["negotiation_approach"] == "Conservative" else "Medium" if strategy["negotiation_approach"] == "Moderate" else "High",
                "market_risk": "Low" if price_growth > 5 else "Medium",
                "timing_risk": "Low" if days_on_market > 30 else "Medium"
            }
            
            return json.dumps(strategy, indent=2)
        except Exception as e:
            return f"Error developing negotiation strategy: {str(e)}"
    
    def calculate_optimal_offer(self, property_data, investment_criteria):
        """
        Calculate optimal offer price based on investment criteria.
        
        Args:
            property_data (str): JSON string of property data
            investment_criteria (str): Investment criteria and goals
        
        Returns:
            str: Optimal offer analysis
        """
        try:
            if isinstance(property_data, str):
                property_data = json.loads(property_data)
            
            # Parse investment criteria
            target_cap_rate = 6.5
            target_cash_on_cash = 6.0
            
            if "high return" in investment_criteria.lower():
                target_cap_rate = 8.0
                target_cash_on_cash = 8.0
            elif "moderate return" in investment_criteria.lower():
                target_cap_rate = 6.5
                target_cash_on_cash = 6.0
            elif "conservative" in investment_criteria.lower():
                target_cap_rate = 5.0
                target_cash_on_cash = 4.0
            
            # Calculate offer prices
            offer_analysis = calculate_max_offer_price(property_data, target_cap_rate, target_cash_on_cash)
            
            # Analyze different offer scenarios
            current_price = property_data["price"]
            scenarios = {
                "conservative_offer": {
                    "price": current_price * 0.98,
                    "probability": "High",
                    "risk": "Low",
                    "expected_return": "Below target"
                },
                "moderate_offer": {
                    "price": offer_analysis["recommended_max_offer"],
                    "probability": "Medium",
                    "risk": "Medium",
                    "expected_return": "At target"
                },
                "aggressive_offer": {
                    "price": current_price * 0.85,
                    "probability": "Low",
                    "risk": "High",
                    "expected_return": "Above target"
                }
            }
            
            # Calculate expected returns for each scenario
            for scenario_name, scenario in scenarios.items():
                if scenario_name == "moderate_offer":
                    scenario["cap_rate"] = target_cap_rate
                    scenario["cash_on_cash"] = target_cash_on_cash
                else:
                    # Simplified calculation for other scenarios
                    scenario["cap_rate"] = target_cap_rate * (current_price / scenario["price"])
                    scenario["cash_on_cash"] = target_cash_on_cash * (current_price / scenario["price"])
            
            result = {
                "property_id": property_data["id"],
                "current_price": current_price,
                "target_returns": {
                    "cap_rate": target_cap_rate,
                    "cash_on_cash": target_cash_on_cash
                },
                "offer_scenarios": scenarios,
                "recommended_approach": self._recommend_offer_approach(scenarios, investment_criteria),
                "negotiation_tips": self._generate_negotiation_tips(scenarios)
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error calculating optimal offer: {str(e)}"
    
    def analyze_seller_motivation(self, property_data, market_data):
        """
        Analyze seller motivation based on property and market data.
        
        Args:
            property_data (str): JSON string of property data
            market_data (str): Market data and trends
        
        Returns:
            str: Seller motivation analysis
        """
        try:
            if isinstance(property_data, str):
                property_data = json.loads(property_data)
            
            market_trends = property_data["market_trends"]
            
            motivation_analysis = {
                "property_id": property_data["id"],
                "seller_motivation_score": 0,
                "motivation_factors": [],
                "negotiation_leverage": [],
                "timing_considerations": []
            }
            
            # Analyze motivation factors
            days_on_market = market_trends["days_on_market"]
            price_growth = market_trends["price_growth_1y"]
            
            # Days on market analysis
            if days_on_market > 90:
                motivation_analysis["seller_motivation_score"] += 30
                motivation_analysis["motivation_factors"].append("Property has been on market for 3+ months")
                motivation_analysis["negotiation_leverage"].append("Extended time on market indicates seller motivation")
            elif days_on_market > 60:
                motivation_analysis["seller_motivation_score"] += 20
                motivation_analysis["motivation_factors"].append("Property has been on market for 2+ months")
                motivation_analysis["negotiation_leverage"].append("Moderate time on market - some flexibility")
            elif days_on_market > 30:
                motivation_analysis["seller_motivation_score"] += 10
                motivation_analysis["motivation_factors"].append("Property has been on market for 1+ month")
            else:
                motivation_analysis["motivation_factors"].append("Property is new to market")
                motivation_analysis["negotiation_leverage"].append("Limited leverage - seller may be patient")
            
            # Market condition analysis
            if price_growth < 3:
                motivation_analysis["seller_motivation_score"] += 15
                motivation_analysis["motivation_factors"].append("Slow market growth may motivate seller")
                motivation_analysis["negotiation_leverage"].append("Market conditions favor buyer")
            elif price_growth > 8:
                motivation_analysis["seller_motivation_score"] -= 10
                motivation_analysis["motivation_factors"].append("Strong market growth - seller may be confident")
                motivation_analysis["negotiation_leverage"].append("Market conditions favor seller")
            
            # Property-specific factors
            if property_data["year_built"] < 2000:
                motivation_analysis["seller_motivation_score"] += 10
                motivation_analysis["motivation_factors"].append("Older property may require more maintenance")
                motivation_analysis["negotiation_leverage"].append("Age-related issues can be negotiation points")
            
            if property_data["hoa_fees"] > 200:
                motivation_analysis["motivation_factors"].append("High HOA fees may limit buyer pool")
                motivation_analysis["negotiation_leverage"].append("HOA fees can be used in negotiations")
            
            # Determine motivation level
            score = motivation_analysis["seller_motivation_score"]
            if score >= 40:
                motivation_analysis["motivation_level"] = "High"
                motivation_analysis["recommendation"] = "Seller appears highly motivated - aggressive negotiation possible"
            elif score >= 20:
                motivation_analysis["motivation_level"] = "Medium"
                motivation_analysis["recommendation"] = "Moderate seller motivation - balanced approach recommended"
            else:
                motivation_analysis["motivation_level"] = "Low"
                motivation_analysis["recommendation"] = "Seller appears patient - conservative approach advised"
            
            return json.dumps(motivation_analysis, indent=2)
        except Exception as e:
            return f"Error analyzing seller motivation: {str(e)}"
    
    def generate_negotiation_script(self, property_data, strategy_type):
        """
        Generate a negotiation script based on strategy type.
        
        Args:
            property_data (str): JSON string of property data
            strategy_type (str): Type of negotiation strategy
        
        Returns:
            str: Negotiation script and talking points
        """
        try:
            if isinstance(property_data, str):
                property_data = json.loads(property_data)
            
            script = {
                "property_id": property_data["id"],
                "strategy_type": strategy_type,
                "opening_script": "",
                "key_talking_points": [],
                "objection_handlers": [],
                "closing_script": ""
            }
            
            if strategy_type.lower() == "aggressive":
                script["opening_script"] = """I've done a thorough analysis of your property and the current market conditions. 
                I'm prepared to make a strong offer that reflects the property's current market value and condition. 
                I can close quickly, which I believe would be beneficial for both of us."""
                
                script["key_talking_points"] = [
                    "Market analysis shows property is overpriced for current conditions",
                    "Property has been on market for extended period",
                    "Quick close provides certainty and convenience",
                    "Cash offer eliminates financing contingencies"
                ]
                
                script["objection_handlers"] = [
                    "If seller mentions other offers: 'I understand, but my offer is clean and ready to close immediately'",
                    "If seller mentions price: 'I've based my offer on recent comparable sales and current market conditions'",
                    "If seller wants to wait: 'The market is showing signs of cooling, and waiting may result in lower offers'"
                ]
                
                script["closing_script"] = """I believe this offer represents fair market value and provides you with a 
                guaranteed sale. I'm ready to move forward immediately if you find the terms acceptable."""
            
            elif strategy_type.lower() == "moderate":
                script["opening_script"] = """Thank you for showing me the property. I'm very interested and have done 
                my research on the market and comparable properties. I'd like to discuss how we can make this work for both parties."""
                
                script["key_talking_points"] = [
                    "Property fits my investment criteria well",
                    "Market comparables support my offer price",
                    "Flexible on closing timeline",
                    "Willing to work with seller on terms"
                ]
                
                script["objection_handlers"] = [
                    "If seller mentions price: 'I'm open to discussing the price, but I need to ensure the numbers work for my investment goals'",
                    "If seller mentions timing: 'I'm flexible on the closing date - what works best for you?'",
                    "If seller mentions condition: 'I'm willing to work with the current condition, but that's reflected in my offer'"
                ]
                
                script["closing_script"] = """I believe we can find common ground that works for both of us. 
                I'm committed to making this deal happen if we can agree on reasonable terms."""
            
            else:  # Conservative
                script["opening_script"] = """I appreciate the opportunity to view your property. It's exactly what 
                I'm looking for, and I'm prepared to make a strong, clean offer that reflects the property's value."""
                
                script["key_talking_points"] = [
                    "Property meets all my criteria perfectly",
                    "Offer is close to asking price",
                    "Clean offer with minimal contingencies",
                    "Ready to proceed quickly"
                ]
                
                script["objection_handlers"] = [
                    "If seller mentions price: 'I understand your position, and I'm willing to discuss a fair compromise'",
                    "If seller mentions other interest: 'I'm ready to move forward immediately with a strong offer'",
                    "If seller mentions timing: 'I can accommodate your preferred timeline'"
                ]
                
                script["closing_script"] = """I'm very serious about this property and ready to move forward. 
                I believe my offer is fair and reflects the property's true value in today's market."""
            
            return json.dumps(script, indent=2)
        except Exception as e:
            return f"Error generating negotiation script: {str(e)}"
    
    def _recommend_offer_approach(self, scenarios, investment_criteria):
        """
        Recommend the best offer approach based on scenarios and criteria.
        
        Args:
            scenarios (dict): Offer scenarios
            investment_criteria (str): Investment criteria
        
        Returns:
            str: Recommended approach
        """
        if "conservative" in investment_criteria.lower():
            return "Use conservative offer to minimize risk and ensure deal completion"
        elif "aggressive" in investment_criteria.lower():
            return "Use aggressive offer to maximize returns, accepting higher risk of losing deal"
        else:
            return "Use moderate offer for balanced risk-reward profile"
    
    def _generate_negotiation_tips(self, scenarios):
        """
        Generate negotiation tips based on offer scenarios.
        
        Args:
            scenarios (dict): Offer scenarios
        
        Returns:
            list: Negotiation tips
        """
        tips = [
            "Always start with your best offer to show seriousness",
            "Be prepared to walk away if terms don't meet your criteria",
            "Use market data to support your offer price",
            "Consider seller's timeline and motivation",
            "Have financing pre-approved to strengthen your position"
        ]
        
        if scenarios["aggressive_offer"]["probability"] == "Low":
            tips.append("Be prepared for counter-offers if using aggressive strategy")
        
        if scenarios["conservative_offer"]["expected_return"] == "Below target":
            tips.append("Consider if conservative approach aligns with investment goals")
        
        return tips
    
    def execute(self, task_description):
        """
        Execute the deal negotiator task.
        
        Args:
            task_description (str): Description of the task to execute
        
        Returns:
            str: Task execution result
        """
        return self.agent.execute(task_description) 