"""
Market Analyst Agent for real estate property search and market analysis.
This agent searches for properties based on criteria and provides market insights.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent
from backend.data.mock_listings import get_properties_by_criteria
from utils.calculations import calculate_investment_score
import json

class MarketAnalystAgent:
    def __init__(self, openai_api_key=None):
        """
        Initialize the Market Analyst Agent.
        
        Args:
            openai_api_key (str): OpenAI API key for LLM responses
        """
        self.openai_api_key = openai_api_key
        
        # Define the agent
        self.agent = Agent(
            role="Real Estate Market Analyst",
            goal="Find and analyze the best investment properties based on location, budget, and property type criteria",
            backstory="""You are an experienced real estate market analyst with over 15 years of experience 
            in property investment analysis. You specialize in identifying high-potential investment properties 
            and providing detailed market insights. You have a deep understanding of market trends, property 
            valuation, and investment metrics. Your analysis helps investors make informed decisions about 
            property acquisitions.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.search_properties, self.analyze_property, self.get_market_insights],
            llm_model="gpt-3.5-turbo" if not openai_api_key else "gpt-4"
        )
    
    def search_properties(self, city, max_price, property_type):
        """
        Search for properties based on criteria.
        
        Args:
            city (str): City name
            max_price (int): Maximum price
            property_type (str): Type of property
        
        Returns:
            str: JSON string of found properties
        """
        try:
            properties = get_properties_by_criteria(
                city=city,
                max_price=max_price,
                property_type=property_type
            )
            
            # Add investment scores to properties
            for prop in properties:
                investment_analysis = calculate_investment_score(prop)
                prop["investment_analysis"] = investment_analysis
            
            return json.dumps(properties, indent=2)
        except Exception as e:
            return f"Error searching properties: {str(e)}"
    
    def analyze_property(self, property_id):
        """
        Analyze a specific property in detail.
        
        Args:
            property_id (str): Property ID to analyze
        
        Returns:
            str: Detailed property analysis
        """
        try:
            from backend.data.mock_listings import get_property_by_id
            property_data = get_property_by_id(property_id)
            
            if not property_data:
                return "Property not found."
            
            # Calculate investment metrics
            investment_analysis = calculate_investment_score(property_data)
            
            analysis = {
                "property": property_data,
                "investment_analysis": investment_analysis,
                "recommendations": self._generate_property_recommendations(property_data, investment_analysis)
            }
            
            return json.dumps(analysis, indent=2)
        except Exception as e:
            return f"Error analyzing property: {str(e)}"
    
    def get_market_insights(self, city):
        """
        Get market insights for a specific city.
        
        Args:
            city (str): City name
        
        Returns:
            str: Market insights and trends
        """
        try:
            properties = get_properties_by_criteria(city=city)
            
            if not properties:
                return f"No properties found for {city}."
            
            # Calculate market statistics
            avg_price = sum(p["price"] for p in properties) / len(properties)
            avg_cap_rate = sum(calculate_investment_score(p)["metrics"]["cap_rate"] for p in properties) / len(properties)
            avg_days_on_market = sum(p["market_trends"]["days_on_market"] for p in properties) / len(properties)
            
            insights = {
                "city": city,
                "total_properties": len(properties),
                "average_price": round(avg_price, 2),
                "average_cap_rate": round(avg_cap_rate, 2),
                "average_days_on_market": round(avg_days_on_market, 1),
                "price_range": {
                    "min": min(p["price"] for p in properties),
                    "max": max(p["price"] for p in properties)
                },
                "market_trends": {
                    "avg_price_growth": sum(p["market_trends"]["price_growth_1y"] for p in properties) / len(properties),
                    "avg_rent_growth": sum(p["market_trends"]["rent_growth_1y"] for p in properties) / len(properties)
                }
            }
            
            return json.dumps(insights, indent=2)
        except Exception as e:
            return f"Error getting market insights: {str(e)}"
    
    def _generate_property_recommendations(self, property_data, investment_analysis):
        """
        Generate recommendations for a property.
        
        Args:
            property_data (dict): Property information
            investment_analysis (dict): Investment analysis results
        
        Returns:
            dict: Property recommendations
        """
        score = investment_analysis["total_score"]
        metrics = investment_analysis["metrics"]
        
        recommendations = {
            "investment_grade": "A" if score >= 80 else "B" if score >= 60 else "C" if score >= 40 else "D",
            "recommendation": "",
            "strengths": [],
            "concerns": [],
            "suggested_actions": []
        }
        
        # Determine recommendation based on score
        if score >= 80:
            recommendations["recommendation"] = "Strong Buy - Excellent investment opportunity"
        elif score >= 60:
            recommendations["recommendation"] = "Buy - Good investment potential"
        elif score >= 40:
            recommendations["recommendation"] = "Hold - Consider with caution"
        else:
            recommendations["recommendation"] = "Avoid - Poor investment potential"
        
        # Identify strengths
        if metrics["cap_rate"] >= 6:
            recommendations["strengths"].append("Strong cap rate")
        if metrics["cash_on_cash"] >= 6:
            recommendations["strengths"].append("Good cash-on-cash return")
        if property_data["year_built"] >= 2010:
            recommendations["strengths"].append("Relatively new property")
        if property_data["market_trends"]["price_growth_1y"] >= 5:
            recommendations["strengths"].append("Strong price appreciation")
        
        # Identify concerns
        if metrics["cap_rate"] < 4:
            recommendations["concerns"].append("Low cap rate")
        if metrics["cash_on_cash"] < 4:
            recommendations["concerns"].append("Low cash-on-cash return")
        if property_data["market_trends"]["days_on_market"] > 30:
            recommendations["concerns"].append("Property has been on market for extended period")
        
        # Suggest actions
        if score >= 60:
            recommendations["suggested_actions"].append("Schedule property inspection")
            recommendations["suggested_actions"].append("Review comparable sales")
            recommendations["suggested_actions"].append("Prepare offer strategy")
        else:
            recommendations["suggested_actions"].append("Continue searching for better opportunities")
            recommendations["suggested_actions"].append("Consider different property types or locations")
        
        return recommendations
    
    def execute(self, task_description):
        """
        Execute the market analyst task.
        
        Args:
            task_description (str): Description of the task to execute
        
        Returns:
            str: Task execution result
        """
        return self.agent.execute(task_description) 