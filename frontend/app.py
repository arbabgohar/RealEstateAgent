"""
Streamlit frontend for Real Estate Deal Screener & Negotiation Copilot.
Provides a user-friendly interface for property search and analysis.
"""

import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configuration
API_BASE_URL = "http://localhost:8000"

def main():
    st.set_page_config(
        page_title="Real Estate Deal Screener & Negotiation Copilot",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .property-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🏠 Real Estate Deal Screener & Negotiation Copilot</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["Property Search", "Property Analysis", "Market Insights", "About"]
        )
        
        st.header("API Status")
        try:
            response = requests.get(f"{API_BASE_URL}/health")
            if response.status_code == 200:
                st.success("✅ Backend Connected")
            else:
                st.error("❌ Backend Error")
        except:
            st.error("❌ Backend Unavailable")
    
    # Page routing
    if page == "Property Search":
        property_search_page()
    elif page == "Property Analysis":
        property_analysis_page()
    elif page == "Market Insights":
        market_insights_page()
    elif page == "About":
        about_page()

def property_search_page():
    """Property search and listing page."""
    st.header("🔍 Property Search")
    
    # Search form
    with st.form("search_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            city = st.text_input("City", value="Austin", placeholder="Enter city name")
        
        with col2:
            max_price = st.number_input("Max Price ($)", min_value=100000, max_value=2000000, value=500000, step=50000)
        
        with col3:
            property_type = st.selectbox(
                "Property Type",
                ["Any", "Single Family", "Townhouse", "Condo", "Multi-Family"]
            )
        
        search_button = st.form_submit_button("🔍 Search Properties")
    
    if search_button:
        with st.spinner("Searching properties..."):
            try:
                response = requests.post(f"{API_BASE_URL}/search", json={
                    "city": city,
                    "max_price": max_price,
                    "property_type": None if property_type == "Any" else property_type
                })
                
                if response.status_code == 200:
                    data = response.json()
                    properties = data["properties"]
                    market_insights = data["market_insights"]
                    
                    # Display market insights
                    st.subheader("📊 Market Insights")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Properties", market_insights.get("total_properties", 0))
                    
                    with col2:
                        st.metric("Avg Price", f"${market_insights.get('average_price', 0):,.0f}")
                    
                    with col3:
                        st.metric("Avg Cap Rate", f"{market_insights.get('average_cap_rate', 0):.2f}%")
                    
                    with col4:
                        st.metric("Avg Days on Market", f"{market_insights.get('average_days_on_market', 0):.0f}")
                    
                    # Display properties
                    st.subheader(f"🏠 Found {len(properties)} Properties")
                    
                    for i, prop in enumerate(properties):
                        with st.expander(f"{prop['address']} - ${prop['price']:,.0f}"):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.write(f"**Property Type:** {prop['property_type']}")
                                st.write(f"**Bedrooms:** {prop['bedrooms']} | **Bathrooms:** {prop['bathrooms']}")
                                st.write(f"**Square Feet:** {prop['sqft']:,} | **Year Built:** {prop['year_built']}")
                                st.write(f"**Monthly Rent:** ${prop['rental_income']:,.0f}")
                                st.write(f"**Description:** {prop['description']}")
                                
                                # Investment metrics
                                if "investment_analysis" in prop:
                                    analysis = prop["investment_analysis"]
                                    st.write(f"**Investment Score:** {analysis.get('total_score', 0)}/100")
                                    st.write(f"**Cap Rate:** {analysis.get('metrics', {}).get('cap_rate', 0):.2f}%")
                                    st.write(f"**Cash-on-Cash:** {analysis.get('metrics', {}).get('cash_on_cash', 0):.2f}%")
                            
                            with col2:
                                if st.button(f"Analyze Property {i+1}", key=f"analyze_{i}"):
                                    st.session_state.selected_property = prop
                                    st.success("Property selected for analysis!")
                
                else:
                    st.error("Error searching properties")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")

def property_analysis_page():
    """Property analysis and deal evaluation page."""
    st.header("📊 Property Analysis")
    
    # Check if property is selected
    if "selected_property" not in st.session_state:
        st.info("Please search for properties and select one for analysis.")
        return
    
    property_data = st.session_state.selected_property
    
    # Property overview
    st.subheader("🏠 Property Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Asking Price", f"${property_data['price']:,.0f}")
    
    with col2:
        st.metric("Monthly Rent", f"${property_data['rental_income']:,.0f}")
    
    with col3:
        st.metric("Cap Rate", f"{(property_data['rental_income'] * 12 / property_data['price'] * 100):.2f}%")
    
    with col4:
        st.metric("Days on Market", property_data['market_trends']['days_on_market'])
    
    # Analysis form
    with st.form("analysis_form"):
        st.subheader("📋 Analysis Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            investment_goals = st.selectbox(
                "Investment Goals",
                ["balanced", "cash flow", "appreciation", "high return", "conservative"]
            )
        
        with col2:
            include_email = st.checkbox("Generate Offer Email")
        
        buyer_info = {}
        if include_email:
            st.subheader("👤 Buyer Information")
            col1, col2 = st.columns(2)
            
            with col1:
                buyer_info["name"] = st.text_input("Name", placeholder="Your Name")
                buyer_info["email"] = st.text_input("Email", placeholder="your.email@example.com")
            
            with col2:
                buyer_info["phone"] = st.text_input("Phone", placeholder="(555) 123-4567")
                buyer_info["financing"] = st.selectbox("Financing Type", ["Conventional", "FHA", "Cash"])
        
        analyze_button = st.form_submit_button("🚀 Analyze Property")
    
    if analyze_button:
        with st.spinner("Analyzing property with AI agents..."):
            try:
                response = requests.post(f"{API_BASE_URL}/analyze", json={
                    "property_id": property_data["id"],
                    "investment_goals": investment_goals,
                    "buyer_info": buyer_info if include_email else None
                })
                
                if response.status_code == 200:
                    analysis = response.json()
                    
                    # Display results in tabs
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "📊 Investment Analysis", 
                        "💼 Negotiation Strategy", 
                        "📋 Final Report", 
                        "📧 Offer Email",
                        "📈 Charts"
                    ])
                    
                    with tab1:
                        display_investment_analysis(analysis["investment_analysis"])
                    
                    with tab2:
                        display_negotiation_strategy(analysis["negotiation_strategy"])
                    
                    with tab3:
                        display_final_report(analysis["final_report"])
                    
                    with tab4:
                        if analysis.get("offer_email"):
                            display_offer_email(analysis["offer_email"])
                        else:
                            st.info("No offer email generated. Check 'Generate Offer Email' option.")
                    
                    with tab5:
                        display_charts(property_data, analysis["investment_analysis"])
                
                else:
                    st.error("Error analyzing property")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")

def display_investment_analysis(analysis):
    """Display investment analysis results."""
    st.subheader("💰 Investment Analysis")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Investment Score", f"{analysis.get('basic_metrics', {}).get('total_score', 0)}/100")
    
    with col2:
        st.metric("Cap Rate", f"{analysis.get('basic_metrics', {}).get('metrics', {}).get('cap_rate', 0):.2f}%")
    
    with col3:
        st.metric("Cash-on-Cash", f"{analysis.get('basic_metrics', {}).get('metrics', {}).get('cash_on_cash', 0):.2f}%")
    
    with col4:
        st.metric("Annual Cash Flow", f"${analysis.get('basic_metrics', {}).get('metrics', {}).get('annual_cash_flow', 0):,.0f}")
    
    # Scenario analysis
    if "scenario_analysis" in analysis:
        st.subheader("📊 Scenario Analysis")
        
        scenarios = analysis["scenario_analysis"]
        scenario_data = []
        
        for scenario_name, scenario in scenarios.items():
            scenario_data.append({
                "Scenario": scenario_name.title(),
                "Investment Score": scenario.get("total_score", 0),
                "Cap Rate": scenario.get("metrics", {}).get("cap_rate", 0),
                "Cash-on-Cash": scenario.get("metrics", {}).get("cash_on_cash", 0),
                "ROI": scenario.get("roi", 0)
            })
        
        df = pd.DataFrame(scenario_data)
        st.dataframe(df, use_container_width=True)
        
        # Create comparison chart
        fig = go.Figure()
        
        scenarios = df["Scenario"].tolist()
        cap_rates = df["Cap Rate"].tolist()
        cash_on_cash = df["Cash-on-Cash"].tolist()
        
        fig.add_trace(go.Bar(name="Cap Rate (%)", x=scenarios, y=cap_rates, marker_color='blue'))
        fig.add_trace(go.Bar(name="Cash-on-Cash (%)", x=scenarios, y=cash_on_cash, marker_color='green'))
        
        fig.update_layout(
            title="Investment Metrics by Scenario",
            xaxis_title="Scenario",
            yaxis_title="Percentage (%)",
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def display_negotiation_strategy(strategy):
    """Display negotiation strategy results."""
    st.subheader("💼 Negotiation Strategy")
    
    # Strategy overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Approach", strategy.get("negotiation_approach", "N/A"))
    
    with col2:
        st.metric("Initial Offer", f"${strategy.get('recommended_strategy', {}).get('initial_offer', 0):,.0f}")
    
    with col3:
        st.metric("Target Price", f"${strategy.get('recommended_strategy', {}).get('target_price', 0):,.0f}")
    
    # Key factors
    st.subheader("🔍 Key Factors")
    factors = strategy.get("key_factors", [])
    for factor in factors:
        st.write(f"• {factor}")
    
    # Recommended strategy
    st.subheader("📋 Recommended Strategy")
    rec_strategy = strategy.get("recommended_strategy", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Timeline:**", rec_strategy.get("timeline", "N/A"))
        st.write("**Concessions:**")
        concessions = rec_strategy.get("concessions", [])
        for concession in concessions:
            st.write(f"• {concession}")
    
    with col2:
        st.write("**Leverage Points:**")
        leverage_points = rec_strategy.get("leverage_points", [])
        for point in leverage_points:
            st.write(f"• {point}")
    
    # Risk assessment
    st.subheader("⚠️ Risk Assessment")
    risks = strategy.get("risk_assessment", {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        risk_color = {"Low": "green", "Medium": "orange", "High": "red"}
        st.metric("Losing Deal Risk", risks.get("losing_deal_risk", "N/A"))
    
    with col2:
        st.metric("Market Risk", risks.get("market_risk", "N/A"))
    
    with col3:
        st.metric("Timing Risk", risks.get("timing_risk", "N/A"))

def display_final_report(report):
    """Display final investment report."""
    st.subheader("📋 Investment Report")
    
    # Report header
    st.write(f"**Report ID:** {report.get('report_id', 'N/A')}")
    st.write(f"**Generated:** {report.get('generated_date', 'N/A')}")
    
    # Executive summary
    st.subheader("📊 Executive Summary")
    exec_summary = report.get("executive_summary", {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Investment Score", f"{exec_summary.get('investment_score', 0)}/100")
    
    with col2:
        st.metric("Investment Grade", exec_summary.get("investment_grade", "N/A"))
    
    with col3:
        st.metric("Cap Rate", exec_summary.get("key_metrics", {}).get("cap_rate", "N/A"))
    
    with col4:
        st.metric("Cash-on-Cash", exec_summary.get("key_metrics", {}).get("cash_on_cash", "N/A"))
    
    # Recommendations
    st.subheader("💡 Recommendations")
    recommendations = report.get("recommendations", [])
    for rec in recommendations:
        st.write(f"• {rec}")
    
    # Risk assessment
    st.subheader("⚠️ Risk Assessment")
    risk_assessment = report.get("risk_assessment", {})
    
    st.write(f"**Risk Level:** {risk_assessment.get('risk_level', 'N/A')}")
    
    st.write("**Risk Factors:**")
    risk_factors = risk_assessment.get("risk_factors", [])
    for factor in risk_factors:
        st.write(f"• {factor}")
    
    st.write("**Mitigation Strategies:**")
    mitigation = risk_assessment.get("mitigation_strategies", [])
    for strategy in mitigation:
        st.write(f"• {strategy}")

def display_offer_email(email):
    """Display offer email."""
    st.subheader("📧 Offer Email")
    
    # Email details
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**From:** {email.get('sender', 'N/A')}")
        st.write(f"**Email:** {email.get('sender_email', 'N/A')}")
    
    with col2:
        st.write(f"**To:** {email.get('recipient', 'N/A')}")
        st.write(f"**Date:** {email.get('date', 'N/A')}")
    
    st.write(f"**Subject:** {email.get('subject', 'N/A')}")
    
    # Email body
    st.subheader("Email Body")
    st.text_area("Email Content", email.get("body", ""), height=400, disabled=True)
    
    # Attachments
    st.subheader("📎 Attachments")
    attachments = email.get("attachments", [])
    for attachment in attachments:
        st.write(f"• {attachment}")

def display_charts(property_data, investment_analysis):
    """Display investment charts."""
    st.subheader("📈 Investment Charts")
    
    # Cash flow chart
    metrics = investment_analysis.get("basic_metrics", {}).get("metrics", {})
    
    # Monthly cash flow breakdown
    monthly_rent = property_data["rental_income"]
    monthly_expenses = metrics.get("monthly_expenses", 0)
    monthly_cash_flow = monthly_rent - monthly_expenses
    
    cash_flow_data = {
        "Category": ["Rental Income", "Expenses", "Cash Flow"],
        "Amount": [monthly_rent, -monthly_expenses, monthly_cash_flow]
    }
    
    df_cash_flow = pd.DataFrame(cash_flow_data)
    
    fig = px.bar(df_cash_flow, x="Category", y="Amount", 
                 title="Monthly Cash Flow Breakdown",
                 color="Amount",
                 color_continuous_scale=["red", "yellow", "green"])
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Investment metrics comparison
    metrics_data = {
        "Metric": ["Cap Rate", "Cash-on-Cash", "ROI"],
        "Value": [
            metrics.get("cap_rate", 0),
            metrics.get("cash_on_cash", 0),
            metrics.get("roi", 0)
        ]
    }
    
    df_metrics = pd.DataFrame(metrics_data)
    
    fig2 = px.bar(df_metrics, x="Metric", y="Value",
                  title="Investment Metrics",
                  color="Value",
                  color_continuous_scale="viridis")
    
    st.plotly_chart(fig2, use_container_width=True)

def market_insights_page():
    """Market insights page."""
    st.header("📊 Market Insights")
    
    # City selection
    city = st.text_input("Enter city name", value="Austin")
    
    if st.button("Get Market Insights"):
        with st.spinner("Fetching market insights..."):
            try:
                response = requests.get(f"{API_BASE_URL}/market-insights/{city}")
                
                if response.status_code == 200:
                    insights = response.json()
                    
                    # Market overview
                    st.subheader(f"📈 {city} Market Overview")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Properties", insights.get("total_properties", 0))
                    
                    with col2:
                        st.metric("Average Price", f"${insights.get('average_price', 0):,.0f}")
                    
                    with col3:
                        st.metric("Average Cap Rate", f"{insights.get('average_cap_rate', 0):.2f}%")
                    
                    with col4:
                        st.metric("Avg Days on Market", f"{insights.get('average_days_on_market', 0):.0f}")
                    
                    # Price range
                    st.subheader("💰 Price Range")
                    price_range = insights.get("price_range", {})
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Minimum Price", f"${price_range.get('min', 0):,.0f}")
                    
                    with col2:
                        st.metric("Maximum Price", f"${price_range.get('max', 0):,.0f}")
                    
                    # Market trends
                    st.subheader("📊 Market Trends")
                    trends = insights.get("market_trends", {})
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Avg Price Growth (1Y)", f"{trends.get('avg_price_growth', 0):.1f}%")
                    
                    with col2:
                        st.metric("Avg Rent Growth (1Y)", f"{trends.get('avg_rent_growth', 0):.1f}%")
                
                else:
                    st.error("Error fetching market insights")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")

def about_page():
    """About page."""
    st.header("ℹ️ About")
    
    st.markdown("""
    ## Real Estate Deal Screener & Negotiation Copilot
    
    This application uses AI-powered agents to help real estate investors:
    
    - **Search** for investment properties
    - **Analyze** investment potential and returns
    - **Develop** negotiation strategies
    - **Generate** professional reports and offer emails
    
    ### Technology Stack
    
    - **Backend**: FastAPI with CrewAI multi-agent system
    - **Frontend**: Streamlit web interface
    - **AI**: OpenAI GPT models for analysis and reasoning
    - **Data**: Mock property listings (easily replaceable with real APIs)
    
    ### AI Agents
    
    1. **Market Analyst Agent**: Searches properties and analyzes market conditions
    2. **Investment Agent**: Calculates ROI, cap rates, and investment scores
    3. **Deal Negotiator Agent**: Develops negotiation strategies and offer prices
    4. **Report Generator Agent**: Creates professional reports and email drafts
    
    ### Getting Started
    
    1. Search for properties by location, price, and type
    2. Select a property for detailed analysis
    3. Review investment metrics and recommendations
    4. Generate negotiation strategies and offer emails
    
    ### Features
    
    - Comprehensive investment analysis
    - Multi-scenario financial modeling
    - Professional report generation
    - Negotiation strategy development
    - Market insights and trends
    - Offer email generation
    
    ### Note
    
    This is a demonstration system using mock data. In production, integrate with real property listing APIs and MLS data sources.
    """)

if __name__ == "__main__":
    main() 