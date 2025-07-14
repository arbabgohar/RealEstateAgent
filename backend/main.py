"""
FastAPI backend for Real Estate Deal Screener & Negotiation Copilot.
Orchestrates CrewAI agents to provide comprehensive real estate analysis.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import os
from dotenv import load_dotenv

# Import agents
from agents.market_analyst import MarketAnalystAgent
from agents.investment_agent import InvestmentAgent
from agents.deal_negotiator import DealNegotiatorAgent
from agents.report_generator import ReportGeneratorAgent

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Real Estate Deal Screener & Negotiation Copilot",
    description="AI-powered real estate investment analysis and negotiation assistance",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
openai_api_key = os.getenv("OPENAI_API_KEY")
market_analyst = MarketAnalystAgent(openai_api_key)
investment_agent = InvestmentAgent(openai_api_key)
deal_negotiator = DealNegotiatorAgent(openai_api_key)
report_generator = ReportGeneratorAgent(openai_api_key)

# Pydantic models for request/response
class PropertySearchRequest(BaseModel):
    city: str
    max_price: int
    property_type: Optional[str] = None

class DealAnalysisRequest(BaseModel):
    property_id: str
    investment_goals: Optional[str] = "balanced"
    buyer_info: Optional[dict] = None

class PropertyAnalysisResponse(BaseModel):
    property_data: dict
    market_analysis: dict
    investment_analysis: dict
    negotiation_strategy: dict
    final_report: dict
    offer_email: Optional[dict] = None

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Real Estate Deal Screener & Negotiation Copilot API",
        "version": "1.0.0",
        "endpoints": {
            "/search": "Search for properties",
            "/analyze": "Analyze a specific property",
            "/health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agents": "initialized"}

@app.post("/search", response_model=List[dict])
async def search_properties(request: PropertySearchRequest):
    """
    Search for properties based on criteria.
    
    Args:
        request: Property search criteria
    
    Returns:
        List of matching properties with basic analysis
    """
    try:
        # Use market analyst to search properties
        search_result = market_analyst.search_properties(
            city=request.city,
            max_price=request.max_price,
            property_type=request.property_type
        )
        
        # Parse the result
        properties = json.loads(search_result)
        
        # Add basic market insights
        market_insights = market_analyst.get_market_insights(request.city)
        market_data = json.loads(market_insights)
        
        return {
            "properties": properties,
            "market_insights": market_data,
            "search_criteria": {
                "city": request.city,
                "max_price": request.max_price,
                "property_type": request.property_type
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching properties: {str(e)}")

@app.post("/analyze", response_model=PropertyAnalysisResponse)
async def analyze_property_deal(request: DealAnalysisRequest):
    """
    Perform comprehensive analysis of a property deal.
    
    Args:
        request: Property analysis request with property ID and goals
    
    Returns:
        Comprehensive property analysis including all agent outputs
    """
    try:
        # Step 1: Get property data
        from backend.data.mock_listings import get_property_by_id
        property_data = get_property_by_id(request.property_id)
        
        if not property_data:
            raise HTTPException(status_code=404, detail="Property not found")
        
        # Step 2: Market Analysis
        market_analysis_result = market_analyst.analyze_property(request.property_id)
        market_analysis = json.loads(market_analysis_result)
        
        # Step 3: Investment Analysis
        investment_analysis_result = investment_agent.calculate_investment_metrics(
            json.dumps(property_data)
        )
        investment_analysis = json.loads(investment_analysis_result)
        
        # Step 4: Negotiation Strategy
        negotiation_strategy_result = deal_negotiator.develop_negotiation_strategy(
            json.dumps(property_data),
            json.dumps(property_data["market_trends"])
        )
        negotiation_strategy = json.loads(negotiation_strategy_result)
        
        # Step 5: Generate Final Report
        final_report_result = report_generator.generate_investment_report(
            json.dumps(property_data),
            json.dumps(market_analysis),
            json.dumps(investment_analysis),
            json.dumps(negotiation_strategy)
        )
        final_report = json.loads(final_report_result)
        
        # Step 6: Generate Offer Email (if buyer info provided)
        offer_email = None
        if request.buyer_info:
            offer_details = {
                "offer_price": negotiation_strategy.get("recommended_strategy", {}).get("target_price", property_data["price"] * 0.95),
                "earnest_money": 5000,
                "closing_date": "30 days",
                "financing_type": "Conventional"
            }
            
            offer_email_result = report_generator.create_offer_email(
                json.dumps(property_data),
                json.dumps(offer_details),
                json.dumps(request.buyer_info)
            )
            offer_email = json.loads(offer_email_result)
        
        return PropertyAnalysisResponse(
            property_data=property_data,
            market_analysis=market_analysis,
            investment_analysis=investment_analysis,
            negotiation_strategy=negotiation_strategy,
            final_report=final_report,
            offer_email=offer_email
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing property: {str(e)}")

@app.get("/properties")
async def get_all_properties():
    """Get all available properties (for demo purposes)."""
    try:
        from backend.data.mock_listings import MOCK_PROPERTIES
        return {"properties": MOCK_PROPERTIES}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving properties: {str(e)}")

@app.get("/properties/{property_id}")
async def get_property(property_id: str):
    """Get a specific property by ID."""
    try:
        from backend.data.mock_listings import get_property_by_id
        property_data = get_property_by_id(property_id)
        
        if not property_data:
            raise HTTPException(status_code=404, detail="Property not found")
        
        return {"property": property_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving property: {str(e)}")

@app.post("/calculate-offer")
async def calculate_offer_price(property_id: str, target_returns: str = "moderate return"):
    """
    Calculate optimal offer price for a property.
    
    Args:
        property_id: Property ID
        target_returns: Target return requirements
    
    Returns:
        Offer price analysis
    """
    try:
        from backend.data.mock_listings import get_property_by_id
        property_data = get_property_by_id(property_id)
        
        if not property_data:
            raise HTTPException(status_code=404, detail="Property not found")
        
        offer_analysis_result = deal_negotiator.calculate_optimal_offer(
            json.dumps(property_data),
            target_returns
        )
        
        return json.loads(offer_analysis_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating offer price: {str(e)}")

@app.post("/generate-email")
async def generate_offer_email(property_id: str, buyer_info: dict, offer_details: dict):
    """
    Generate a professional offer email.
    
    Args:
        property_id: Property ID
        buyer_info: Buyer information
        offer_details: Offer details
    
    Returns:
        Professional offer email
    """
    try:
        from backend.data.mock_listings import get_property_by_id
        property_data = get_property_by_id(property_id)
        
        if not property_data:
            raise HTTPException(status_code=404, detail="Property not found")
        
        email_result = report_generator.create_offer_email(
            json.dumps(property_data),
            json.dumps(offer_details),
            json.dumps(buyer_info)
        )
        
        return json.loads(email_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating email: {str(e)}")

@app.get("/market-insights/{city}")
async def get_market_insights(city: str):
    """
    Get market insights for a specific city.
    
    Args:
        city: City name
    
    Returns:
        Market insights and trends
    """
    try:
        market_insights_result = market_analyst.get_market_insights(city)
        return json.loads(market_insights_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting market insights: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 