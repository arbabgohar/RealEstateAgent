# Real Estate Deal Screener & Negotiation Copilot

A comprehensive real estate investment analysis and negotiation assistance system built with FastAPI, Streamlit, and CrewAI.

## 🏗️ Architecture

- **Backend**: FastAPI with CrewAI multi-agent system
- **Frontend**: Streamlit web interface
- **AI Agents**: OpenAI-powered analysis and negotiation agents
- **Data**: Mock property listings for demonstration

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run the Backend**:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

4. **Run the Frontend**:
   ```bash
   cd frontend
   streamlit run app.py
   ```

5. **Access the Application**:
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000

## 📁 Project Structure

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
└── requirements.txt        # Python dependencies
```

## 🤖 AI Agents

### Market Analyst Agent
- Searches property listings based on location and budget
- Analyzes market trends and property characteristics
- Returns filtered property recommendations

### Investment Agent
- Calculates key investment metrics (ROI, Cap Rate, Cash-on-Cash)
- Assigns investment scores based on multiple factors
- Provides investment risk assessment

### Deal Negotiator Agent
- Suggests optimal negotiation strategies
- Recommends maximum offer prices
- Provides negotiation talking points

### Report Generator Agent
- Creates professional deal summaries
- Generates offer email drafts
- Compiles comprehensive investment reports

## 💡 Features

- **Property Search**: Filter by location, budget, and property type
- **Investment Analysis**: Automated ROI and cap rate calculations
- **Negotiation Support**: AI-powered negotiation strategies
- **Professional Reports**: Generated summaries and email drafts
- **Multi-Agent Collaboration**: Coordinated analysis across specialized agents

## 🔧 Configuration

The system uses mock data by default. To integrate with real APIs:
1. Update the `market_analyst.py` agent to use real property APIs
2. Modify data structures in `mock_listings.py`
3. Add authentication for external services

## 📊 Sample Output

The system generates comprehensive reports including:
- Property analysis with investment metrics
- Negotiation strategy recommendations
- Professional offer email drafts
- Risk assessment and investment scores

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details 