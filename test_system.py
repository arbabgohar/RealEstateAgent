#!/usr/bin/env python3
"""
Test script for Real Estate Deal Screener & Negotiation Copilot.
Verifies that all components are working correctly.
"""

import sys
import os
import json
import requests
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from backend.data.mock_listings import MOCK_PROPERTIES, get_properties_by_criteria
        print("✅ Mock listings imported successfully")
    except Exception as e:
        print(f"❌ Error importing mock listings: {e}")
        return False
    
    try:
        from utils.calculations import calculate_investment_score, calculate_cap_rate
        print("✅ Calculation utilities imported successfully")
    except Exception as e:
        print(f"❌ Error importing calculation utilities: {e}")
        return False
    
    try:
        from agents.market_analyst import MarketAnalystAgent
        from agents.investment_agent import InvestmentAgent
        from agents.deal_negotiator import DealNegotiatorAgent
        from agents.report_generator import ReportGeneratorAgent
        print("✅ All agents imported successfully")
    except Exception as e:
        print(f"❌ Error importing agents: {e}")
        return False
    
    return True

def test_mock_data():
    """Test that mock data is working correctly."""
    print("\n📊 Testing mock data...")
    
    try:
        from backend.data.mock_listings import MOCK_PROPERTIES, get_properties_by_criteria
        
        # Test property retrieval
        properties = get_properties_by_criteria(city="Austin", max_price=500000)
        print(f"✅ Found {len(properties)} properties in Austin under $500k")
        
        if len(properties) > 0:
            property_data = properties[0]
            print(f"✅ Sample property: {property_data['address']} - ${property_data['price']:,.0f}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing mock data: {e}")
        return False

def test_calculations():
    """Test that calculation utilities work correctly."""
    print("\n🧮 Testing calculations...")
    
    try:
        from backend.data.mock_listings import MOCK_PROPERTIES
        from utils.calculations import calculate_investment_score, calculate_cap_rate
        
        # Test with first property
        property_data = MOCK_PROPERTIES[0]
        
        # Test cap rate calculation
        annual_rent = property_data["rental_income"] * 12
        cap_rate = calculate_cap_rate(annual_rent, property_data["price"])
        print(f"✅ Cap rate calculation: {cap_rate:.2f}%")
        
        # Test investment score calculation
        investment_analysis = calculate_investment_score(property_data)
        print(f"✅ Investment score: {investment_analysis['total_score']}/100")
        print(f"✅ Investment grade: {investment_analysis.get('grade', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing calculations: {e}")
        return False

def test_agents():
    """Test that agents can be initialized and basic functions work."""
    print("\nTesting agents...")
    
    try:
        from agents.market_analyst import MarketAnalystAgent
        from agents.investment_agent import InvestmentAgent
        from agents.deal_negotiator import DealNegotiatorAgent
        from agents.report_generator import ReportGeneratorAgent
        
        # Initialize agents (without OpenAI key for testing)
        market_analyst = MarketAnalystAgent()
        investment_agent = InvestmentAgent()
        deal_negotiator = DealNegotiatorAgent()
        report_generator = ReportGeneratorAgent()
        
        print("✅ All agents initialized successfully")
        
        # Test basic agent functions
        from backend.data.mock_listings import MOCK_PROPERTIES
        property_data = MOCK_PROPERTIES[0]
        
        # Test market analyst search
        search_result = market_analyst.search_properties("Austin", 500000, "Single Family")
        if search_result and "Error" not in search_result:
            print("✅ Market analyst search working")
        else:
            print("⚠️  Market analyst search returned error (expected without OpenAI)")
        
        return True
    except Exception as e:
        print(f"❌ Error testing agents: {e}")
        return False

def test_backend_api():
    """Test that the backend API is working (if running)."""
    print("\n🌐 Testing backend API...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is running and healthy")
            return True
        else:
            print("⚠️  Backend API responded but not healthy")
            return False
    except requests.exceptions.ConnectionError:
        print("⚠️  Backend API not running (start with: python start.py)")
        return False
    except Exception as e:
        print(f"❌ Error testing backend API: {e}")
        return False

def test_frontend():
    """Test that the frontend can be accessed (if running)."""
    print("\n🎨 Testing frontend...")
    
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running and accessible")
            return True
        else:
            print("⚠️  Frontend responded but not healthy")
            return False
    except requests.exceptions.ConnectionError:
        print("⚠️  Frontend not running (start with: python start.py)")
        return False
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")
        return False

def main():
    """Run all tests."""
    print("🏠 Real Estate Deal Screener & Negotiation Copilot - System Test")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Mock Data", test_mock_data),
        ("Calculations", test_calculations),
        ("Agents", test_agents),
        ("Backend API", test_backend_api),
        ("Frontend", test_frontend)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\n🚀 To start the application:")
        print("   python start.py")
    elif passed >= 4:  # Core functionality tests
        print("✅ Core functionality is working!")
        print("⚠️  Some optional components (API/Frontend) are not running.")
        print("\n🚀 To start the full application:")
        print("   python start.py")
    else:
        print("❌ Some core tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Check that all files are in the correct locations")
        print("   3. Ensure Python 3.8+ is being used")

if __name__ == "__main__":
    main() 