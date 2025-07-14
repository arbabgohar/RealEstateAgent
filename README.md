# Real Estate Deal Screener

A comprehensive real estate investment analysis and negotiation assistance system built with FastAPI, Streamlit, and CrewAI.


```
real_estate_copilot/
├── backend/                 # FastAPI application
│   ├── main.py             # API routes and agent orchestration
│   └── data/               # Mock property data
│       └── mock_listings.py
├── agents/                 # CrewAI agent definitions
│   ├── market_analyst.py   # Property search and market analysis
│   ├── investment_agent.py # ROI and investment calculations
│   ├── deal_negotiator.py  # Negotiation strategy
│   └── report_generator.py # Report and email generation
├── frontend/               # Streamlit interface
│   └── app.py             # Main Streamlit application
├── utils/                  # Shared utilities
│   └── calculations.py    # Financial calculation helpers
├── start.py               # Easy startup script
├── test_system.py         # System testing script
├── requirements.txt       # Python dependencies
└── env_template.txt       # Environment variables template
```
