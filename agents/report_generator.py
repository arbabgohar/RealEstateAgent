"""
Report Generator Agent for creating professional real estate investment reports and email drafts.
This agent compiles analysis results into comprehensive reports and generates offer emails.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent
from datetime import datetime
import json

class ReportGeneratorAgent:
    def __init__(self, openai_api_key=None):
        """
        Initialize the Report Generator Agent.
        
        Args:
            openai_api_key (str): OpenAI API key for LLM responses
        """
        self.openai_api_key = openai_api_key
        
        # Define the agent
        self.agent = Agent(
            role="Real Estate Report Generator",
            goal="Create professional investment reports and generate compelling offer emails for real estate deals",
            backstory="""You are a senior real estate analyst and communications expert with extensive experience 
            in creating professional investment reports and negotiation communications. You have a talent for 
            presenting complex financial data in clear, actionable formats that help investors make informed 
            decisions. Your reports are known for their accuracy, clarity, and professional presentation. 
            You excel at crafting persuasive offer emails that balance professionalism with negotiation strategy.""",
            verbose=True,
            allow_delegation=False,
            tools=[
                self.generate_investment_report,
                self.create_offer_email,
                self.generate_executive_summary,
                self.create_comparative_analysis
            ],
            llm_model="gpt-3.5-turbo" if not openai_api_key else "gpt-4"
        )
    
    def generate_investment_report(self, property_data, market_analysis, investment_analysis, negotiation_strategy):
        """
        Generate a comprehensive investment report.
        
        Args:
            property_data (str): JSON string of property data
            market_analysis (str): Market analysis results
            investment_analysis (str): Investment analysis results
            negotiation_strategy (str): Negotiation strategy results
        
        Returns:
            str: Comprehensive investment report
        """
        try:
            if isinstance(property_data, str):
                property_data = json.loads(property_data)
            if isinstance(market_analysis, str):
                market_analysis = json.loads(market_analysis)
            if isinstance(investment_analysis, str):
                investment_analysis = json.loads(investment_analysis)
            if isinstance(negotiation_strategy, str):
                negotiation_strategy = json.loads(negotiation_strategy)
            
            report = {
                "report_id": f"REP_{property_data['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "generated_date": datetime.now().strftime("%B %d, %Y"),
                "property_summary": self._create_property_summary(property_data),
                "market_analysis": self._format_market_analysis(market_analysis),
                "investment_analysis": self._format_investment_analysis(investment_analysis),
                "negotiation_recommendations": self._format_negotiation_strategy(negotiation_strategy),
                "executive_summary": self._create_executive_summary(property_data, investment_analysis, negotiation_strategy),
                "risk_assessment": self._create_risk_assessment(property_data, investment_analysis),
                "recommendations": self._create_recommendations(property_data, investment_analysis, negotiation_strategy)
            }
            
            return json.dumps(report, indent=2)
        except Exception as e:
            return f"Error generating investment report: {str(e)}"
    
    def create_offer_email(self, property_data, offer_details, buyer_info):
        """
        Create a professional offer email.
        
        Args:
            property_data (str): JSON string of property data
            offer_details (str): Offer details and terms
            buyer_info (str): Buyer information
        
        Returns:
            str: Professional offer email
        """
        try:
            if isinstance(property_data, str):
                property_data = json.loads(property_data)
            if isinstance(offer_details, str):
                offer_details = json.loads(offer_details)
            if isinstance(buyer_info, str):
                buyer_info = json.loads(buyer_info)
            
            email = {
                "subject": f"Offer for {property_data['address']}",
                "sender": buyer_info.get("name", "Real Estate Investor"),
                "sender_email": buyer_info.get("email", "investor@example.com"),
                "recipient": "Seller/Listing Agent",
                "date": datetime.now().strftime("%B %d, %Y"),
                "body": self._generate_email_body(property_data, offer_details, buyer_info),
                "attachments": [
                    "Pre-approval Letter",
                    "Proof of Funds",
                    "Property Analysis Report"
                ]
            }
            
            return json.dumps(email, indent=2)
        except Exception as e:
            return f"Error creating offer email: {str(e)}"
    
    def generate_executive_summary(self, property_data, investment_analysis, market_conditions):
        """
        Generate an executive summary of the investment opportunity.
        
        Args:
            property_data (str): JSON string of property data
            investment_analysis (str): Investment analysis results
            market_conditions (str): Market conditions summary
        
        Returns:
            str: Executive summary
        """
        try:
            if isinstance(property_data, str):
                property_data = json.loads(property_data)
            if isinstance(investment_analysis, str):
                investment_analysis = json.loads(investment_analysis)
            if isinstance(market_conditions, str):
                market_conditions = json.loads(market_conditions)
            
            summary = {
                "investment_opportunity": {
                    "property_address": property_data["address"],
                    "property_type": property_data["property_type"],
                    "asking_price": f"${property_data['price']:,.0f}",
                    "investment_score": investment_analysis.get("total_score", 0),
                    "investment_grade": "A" if investment_analysis.get("total_score", 0) >= 80 else "B" if investment_analysis.get("total_score", 0) >= 60 else "C" if investment_analysis.get("total_score", 0) >= 40 else "D"
                },
                "key_metrics": {
                    "cap_rate": f"{investment_analysis.get('metrics', {}).get('cap_rate', 0):.2f}%",
                    "cash_on_cash": f"{investment_analysis.get('metrics', {}).get('cash_on_cash', 0):.2f}%",
                    "annual_cash_flow": f"${investment_analysis.get('metrics', {}).get('annual_cash_flow', 0):,.0f}",
                    "roi": f"{investment_analysis.get('metrics', {}).get('roi', 0):.2f}%"
                },
                "market_overview": {
                    "price_growth": f"{property_data['market_trends']['price_growth_1y']:.1f}%",
                    "rent_growth": f"{property_data['market_trends']['rent_growth_1y']:.1f}%",
                    "days_on_market": property_data['market_trends']['days_on_market']
                },
                "investment_recommendation": self._get_investment_recommendation(investment_analysis.get("total_score", 0)),
                "next_steps": self._get_next_steps(investment_analysis.get("total_score", 0))
            }
            
            return json.dumps(summary, indent=2)
        except Exception as e:
            return f"Error generating executive summary: {str(e)}"
    
    def create_comparative_analysis(self, target_property, comparable_properties):
        """
        Create a comparative analysis with similar properties.
        
        Args:
            target_property (str): JSON string of target property data
            comparable_properties (str): JSON string of comparable properties
        
        Returns:
            str: Comparative analysis report
        """
        try:
            if isinstance(target_property, str):
                target_property = json.loads(target_property)
            if isinstance(comparable_properties, str):
                comparable_properties = json.loads(comparable_properties)
            
            analysis = {
                "target_property": {
                    "address": target_property["address"],
                    "price": target_property["price"],
                    "price_per_sqft": target_property["price"] / target_property["sqft"],
                    "cap_rate": self._calculate_cap_rate(target_property),
                    "days_on_market": target_property["market_trends"]["days_on_market"]
                },
                "comparable_analysis": [],
                "market_positioning": {},
                "valuation_insights": []
            }
            
            # Analyze comparables
            for comp in comparable_properties:
                comp_analysis = {
                    "address": comp["address"],
                    "price": comp["price"],
                    "price_per_sqft": comp["price"] / comp["sqft"],
                    "cap_rate": self._calculate_cap_rate(comp),
                    "days_on_market": comp["market_trends"]["days_on_market"],
                    "comparison": self._compare_properties(target_property, comp)
                }
                analysis["comparable_analysis"].append(comp_analysis)
            
            # Market positioning
            avg_price = sum(comp["price"] for comp in comparable_properties) / len(comparable_properties)
            avg_cap_rate = sum(self._calculate_cap_rate(comp) for comp in comparable_properties) / len(comparable_properties)
            
            analysis["market_positioning"] = {
                "price_position": "Above Market" if target_property["price"] > avg_price * 1.05 else "Below Market" if target_property["price"] < avg_price * 0.95 else "At Market",
                "cap_rate_position": "Above Market" if self._calculate_cap_rate(target_property) > avg_cap_rate * 1.05 else "Below Market" if self._calculate_cap_rate(target_property) < avg_cap_rate * 0.95 else "At Market",
                "competitiveness": self._assess_competitiveness(target_property, comparable_properties)
            }
            
            return json.dumps(analysis, indent=2)
        except Exception as e:
            return f"Error creating comparative analysis: {str(e)}"
    
    def _create_property_summary(self, property_data):
        """Create a property summary section."""
        return {
            "address": property_data["address"],
            "property_type": property_data["property_type"],
            "key_features": {
                "bedrooms": property_data["bedrooms"],
                "bathrooms": property_data["bathrooms"],
                "square_feet": property_data["sqft"],
                "year_built": property_data["year_built"],
                "lot_size": f"{property_data['lot_size']} acres"
            },
            "financial_overview": {
                "asking_price": f"${property_data['price']:,.0f}",
                "monthly_rent": f"${property_data['rental_income']:,.0f}",
                "annual_rent": f"${property_data['rental_income'] * 12:,.0f}",
                "property_tax": f"${property_data['property_tax']:,.0f}/year",
                "hoa_fees": f"${property_data['hoa_fees']:,.0f}/month" if property_data['hoa_fees'] > 0 else "None"
            },
            "features": property_data["features"]
        }
    
    def _format_market_analysis(self, market_analysis):
        """Format market analysis for the report."""
        return {
            "market_trends": market_analysis.get("market_trends", {}),
            "price_analysis": market_analysis.get("price_range", {}),
            "market_insights": market_analysis.get("insights", [])
        }
    
    def _format_investment_analysis(self, investment_analysis):
        """Format investment analysis for the report."""
        return {
            "investment_score": investment_analysis.get("total_score", 0),
            "investment_grade": "A" if investment_analysis.get("total_score", 0) >= 80 else "B" if investment_analysis.get("total_score", 0) >= 60 else "C" if investment_analysis.get("total_score", 0) >= 40 else "D",
            "key_metrics": investment_analysis.get("metrics", {}),
            "scenario_analysis": investment_analysis.get("scenario_analysis", {}),
            "strengths": investment_analysis.get("recommendations", {}).get("strengths", []),
            "concerns": investment_analysis.get("recommendations", {}).get("concerns", [])
        }
    
    def _format_negotiation_strategy(self, negotiation_strategy):
        """Format negotiation strategy for the report."""
        return {
            "approach": negotiation_strategy.get("negotiation_approach", ""),
            "recommended_offer": negotiation_strategy.get("recommended_strategy", {}),
            "risk_assessment": negotiation_strategy.get("risk_assessment", {}),
            "leverage_points": negotiation_strategy.get("recommended_strategy", {}).get("leverage_points", [])
        }
    
    def _create_executive_summary(self, property_data, investment_analysis, negotiation_strategy):
        """Create an executive summary section."""
        score = investment_analysis.get("total_score", 0)
        
        return {
            "investment_opportunity": f"{property_data['property_type']} property in {property_data['city']}",
            "investment_score": score,
            "investment_grade": "A" if score >= 80 else "B" if score >= 60 else "C" if score >= 40 else "D",
            "key_recommendation": self._get_investment_recommendation(score),
            "negotiation_approach": negotiation_strategy.get("negotiation_approach", ""),
            "expected_returns": {
                "cap_rate": f"{investment_analysis.get('metrics', {}).get('cap_rate', 0):.2f}%",
                "cash_on_cash": f"{investment_analysis.get('metrics', {}).get('cash_on_cash', 0):.2f}%",
                "annual_cash_flow": f"${investment_analysis.get('metrics', {}).get('annual_cash_flow', 0):,.0f}"
            }
        }
    
    def _create_risk_assessment(self, property_data, investment_analysis):
        """Create a risk assessment section."""
        risks = []
        
        if investment_analysis.get("metrics", {}).get("cap_rate", 0) < 4:
            risks.append("Low cap rate indicates limited income potential")
        
        if property_data["market_trends"]["days_on_market"] > 45:
            risks.append("Extended time on market may indicate overpricing or issues")
        
        if property_data["year_built"] < 1990:
            risks.append("Older property may require significant maintenance")
        
        return {
            "risk_level": "Low" if len(risks) <= 1 else "Medium" if len(risks) <= 2 else "High",
            "risk_factors": risks,
            "mitigation_strategies": [
                "Conduct thorough property inspection",
                "Review comparable sales",
                "Assess market conditions",
                "Consider financing options"
            ]
        }
    
    def _create_recommendations(self, property_data, investment_analysis, negotiation_strategy):
        """Create recommendations section."""
        score = investment_analysis.get("total_score", 0)
        recommendations = []
        
        if score >= 80:
            recommendations.extend([
                "Proceed with offer - excellent investment opportunity",
                "Consider aggressive negotiation strategy",
                "Prepare for quick closing"
            ])
        elif score >= 60:
            recommendations.extend([
                "Consider making an offer - good investment potential",
                "Use moderate negotiation approach",
                "Conduct additional due diligence"
            ])
        else:
            recommendations.extend([
                "Consider alternative properties",
                "Re-evaluate investment criteria",
                "Focus on different market segments"
            ])
        
        return recommendations
    
    def _generate_email_body(self, property_data, offer_details, buyer_info):
        """Generate the body of the offer email."""
        return f"""
Dear Seller/Listing Agent,

I am writing to submit an offer for the property at {property_data['address']}.

PROPERTY DETAILS:
- Address: {property_data['address']}
- Property Type: {property_data['property_type']}
- Bedrooms: {property_data['bedrooms']}
- Bathrooms: {property_data['bathrooms']}
- Square Feet: {property_data['sqft']:,}

OFFER DETAILS:
- Offer Price: ${offer_details.get('offer_price', 0):,.0f}
- Earnest Money: ${offer_details.get('earnest_money', 5000):,.0f}
- Closing Date: {offer_details.get('closing_date', '30 days')}
- Financing: {offer_details.get('financing_type', 'Conventional')}

BUYER INFORMATION:
- Name: {buyer_info.get('name', 'Real Estate Investor')}
- Contact: {buyer_info.get('phone', 'N/A')}
- Email: {buyer_info.get('email', 'investor@example.com')}

I am a serious buyer with pre-approved financing and ready to move forward quickly. I have conducted thorough market research and believe this offer reflects the property's fair market value.

Please contact me to discuss this offer or if you need any additional information.

Best regards,
{buyer_info.get('name', 'Real Estate Investor')}
{buyer_info.get('phone', 'N/A')}
{buyer_info.get('email', 'investor@example.com')}
"""
    
    def _get_investment_recommendation(self, score):
        """Get investment recommendation based on score."""
        if score >= 80:
            return "Strong Buy - Excellent investment opportunity"
        elif score >= 60:
            return "Buy - Good investment potential"
        elif score >= 40:
            return "Hold - Consider with caution"
        else:
            return "Avoid - Poor investment potential"
    
    def _get_next_steps(self, score):
        """Get next steps based on investment score."""
        if score >= 60:
            return [
                "Schedule property inspection",
                "Review comparable sales",
                "Prepare offer strategy",
                "Secure financing"
            ]
        else:
            return [
                "Continue property search",
                "Re-evaluate investment criteria",
                "Consider different markets"
            ]
    
    def _calculate_cap_rate(self, property_data):
        """Calculate cap rate for a property."""
        annual_rent = property_data["rental_income"] * 12
        return (annual_rent / property_data["price"]) * 100
    
    def _compare_properties(self, target, comparable):
        """Compare target property with comparable."""
        target_price_per_sqft = target["price"] / target["sqft"]
        comp_price_per_sqft = comparable["price"] / comparable["sqft"]
        
        if target_price_per_sqft > comp_price_per_sqft * 1.1:
            return "Target is overpriced"
        elif target_price_per_sqft < comp_price_per_sqft * 0.9:
            return "Target is underpriced"
        else:
            return "Target is competitively priced"
    
    def _assess_competitiveness(self, target_property, comparables):
        """Assess competitiveness of target property."""
        target_price = target_property["price"]
        avg_comp_price = sum(comp["price"] for comp in comparables) / len(comparables)
        
        if target_price < avg_comp_price * 0.95:
            return "Highly competitive - below market average"
        elif target_price > avg_comp_price * 1.05:
            return "Less competitive - above market average"
        else:
            return "Competitive - within market range"
    
    def execute(self, task_description):
        """
        Execute the report generator task.
        
        Args:
            task_description (str): Description of the task to execute
        
        Returns:
            str: Task execution result
        """
        return self.agent.execute(task_description) 