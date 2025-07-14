"""
Real estate investment calculation utilities.
Provides functions for calculating key investment metrics.
"""

def calculate_cap_rate(annual_rental_income, property_price):
    """
    Calculate the capitalization rate (cap rate).
    
    Args:
        annual_rental_income (float): Annual rental income
        property_price (float): Property purchase price
    
    Returns:
        float: Cap rate as a percentage
    """
    if property_price == 0:
        return 0
    return (annual_rental_income / property_price) * 100

def calculate_cash_on_cash_return(annual_cash_flow, total_cash_invested):
    """
    Calculate cash-on-cash return.
    
    Args:
        annual_cash_flow (float): Annual cash flow after expenses
        total_cash_invested (float): Total cash invested (down payment + closing costs)
    
    Returns:
        float: Cash-on-cash return as a percentage
    """
    if total_cash_invested == 0:
        return 0
    return (annual_cash_flow / total_cash_invested) * 100

def calculate_annual_cash_flow(monthly_rent, monthly_expenses):
    """
    Calculate annual cash flow.
    
    Args:
        monthly_rent (float): Monthly rental income
        monthly_expenses (float): Monthly expenses (mortgage, taxes, insurance, etc.)
    
    Returns:
        float: Annual cash flow
    """
    return (monthly_rent - monthly_expenses) * 12

def calculate_monthly_expenses(property_data, down_payment_percent=20, interest_rate=5.5, loan_term=30):
    """
    Calculate monthly expenses for a property.
    
    Args:
        property_data (dict): Property information
        down_payment_percent (float): Down payment percentage
        interest_rate (float): Mortgage interest rate
        loan_term (int): Loan term in years
    
    Returns:
        float: Monthly expenses
    """
    property_price = property_data["price"]
    down_payment = property_price * (down_payment_percent / 100)
    loan_amount = property_price - down_payment
    
    # Calculate monthly mortgage payment
    monthly_rate = interest_rate / 100 / 12
    num_payments = loan_term * 12
    
    if monthly_rate == 0:
        monthly_mortgage = loan_amount / num_payments
    else:
        monthly_mortgage = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
    
    # Calculate other monthly expenses
    monthly_tax = property_data["property_tax"] / 12
    monthly_insurance = property_data["insurance"] / 12
    monthly_hoa = property_data["hoa_fees"]
    monthly_maintenance = property_data["maintenance_reserve"]
    
    total_monthly_expenses = monthly_mortgage + monthly_tax + monthly_insurance + monthly_hoa + monthly_maintenance
    
    return total_monthly_expenses

def calculate_roi(annual_cash_flow, total_investment, annual_appreciation=3):
    """
    Calculate Return on Investment (ROI).
    
    Args:
        annual_cash_flow (float): Annual cash flow
        total_investment (float): Total cash invested
        annual_appreciation (float): Expected annual appreciation percentage
    
    Returns:
        float: ROI as a percentage
    """
    if total_investment == 0:
        return 0
    
    appreciation_return = total_investment * (annual_appreciation / 100)
    total_return = annual_cash_flow + appreciation_return
    
    return (total_return / total_investment) * 100

def calculate_investment_score(property_data, down_payment_percent=20):
    """
    Calculate a comprehensive investment score (0-100).
    
    Args:
        property_data (dict): Property information
        down_payment_percent (float): Down payment percentage
    
    Returns:
        dict: Investment score and breakdown
    """
    score = 0
    breakdown = {}
    
    # Calculate key metrics
    annual_rental_income = property_data["rental_income"] * 12
    cap_rate = calculate_cap_rate(annual_rental_income, property_data["price"])
    
    monthly_expenses = calculate_monthly_expenses(property_data, down_payment_percent)
    annual_cash_flow = calculate_annual_cash_flow(property_data["rental_income"], monthly_expenses)
    
    total_investment = property_data["price"] * (down_payment_percent / 100) + 5000  # Assuming $5k closing costs
    cash_on_cash = calculate_cash_on_cash_return(annual_cash_flow, total_investment)
    roi = calculate_roi(annual_cash_flow, total_investment)
    
    # Score based on cap rate (0-25 points)
    if cap_rate >= 8:
        cap_rate_score = 25
    elif cap_rate >= 6:
        cap_rate_score = 20
    elif cap_rate >= 4:
        cap_rate_score = 15
    else:
        cap_rate_score = 10
    score += cap_rate_score
    breakdown["cap_rate_score"] = cap_rate_score
    
    # Score based on cash-on-cash return (0-25 points)
    if cash_on_cash >= 8:
        coc_score = 25
    elif cash_on_cash >= 6:
        coc_score = 20
    elif cash_on_cash >= 4:
        coc_score = 15
    else:
        coc_score = 10
    score += coc_score
    breakdown["cash_on_cash_score"] = coc_score
    
    # Score based on property age (0-15 points)
    current_year = 2024
    property_age = current_year - property_data["year_built"]
    if property_age <= 5:
        age_score = 15
    elif property_age <= 10:
        age_score = 12
    elif property_age <= 20:
        age_score = 8
    else:
        age_score = 5
    score += age_score
    breakdown["age_score"] = age_score
    
    # Score based on market trends (0-20 points)
    market_trends = property_data["market_trends"]
    price_growth = market_trends["price_growth_1y"]
    rent_growth = market_trends["rent_growth_1y"]
    
    if price_growth >= 7 and rent_growth >= 5:
        market_score = 20
    elif price_growth >= 5 and rent_growth >= 3:
        market_score = 15
    elif price_growth >= 3 and rent_growth >= 2:
        market_score = 10
    else:
        market_score = 5
    score += market_score
    breakdown["market_score"] = market_score
    
    # Score based on days on market (0-15 points)
    days_on_market = market_trends["days_on_market"]
    if days_on_market <= 15:
        dom_score = 15
    elif days_on_market <= 30:
        dom_score = 10
    elif days_on_market <= 60:
        dom_score = 5
    else:
        dom_score = 0
    score += dom_score
    breakdown["days_on_market_score"] = dom_score
    
    return {
        "total_score": score,
        "breakdown": breakdown,
        "metrics": {
            "cap_rate": cap_rate,
            "cash_on_cash": cash_on_cash,
            "roi": roi,
            "annual_cash_flow": annual_cash_flow,
            "monthly_expenses": monthly_expenses
        }
    }

def calculate_max_offer_price(property_data, target_cap_rate=6.5, target_cash_on_cash=6):
    """
    Calculate maximum offer price based on target returns.
    
    Args:
        property_data (dict): Property information
        target_cap_rate (float): Target cap rate percentage
        target_cash_on_cash (float): Target cash-on-cash return percentage
    
    Returns:
        dict: Maximum offer prices based on different criteria
    """
    annual_rental_income = property_data["rental_income"] * 12
    
    # Max price based on cap rate
    max_price_cap_rate = (annual_rental_income / (target_cap_rate / 100)) if target_cap_rate > 0 else float('inf')
    
    # Max price based on cash-on-cash return
    # This is more complex as it involves mortgage calculations
    # For simplicity, we'll use a conservative estimate
    monthly_expenses_no_mortgage = (property_data["property_tax"] / 12 + 
                                   property_data["insurance"] / 12 + 
                                   property_data["hoa_fees"] + 
                                   property_data["maintenance_reserve"])
    
    annual_cash_flow_no_mortgage = (property_data["rental_income"] - monthly_expenses_no_mortgage) * 12
    
    # Assuming 20% down payment and $5k closing costs
    down_payment_percent = 20
    closing_costs = 5000
    
    # Solve for property price that gives target cash-on-cash return
    # This is a simplified calculation
    target_annual_cash_flow = (property_data["price"] * (down_payment_percent / 100) + closing_costs) * (target_cash_on_cash / 100)
    
    # This is a rough estimate - in practice, you'd need to iterate through different prices
    max_price_coc = property_data["price"] * 0.95  # Conservative 5% below asking
    
    return {
        "max_price_cap_rate": max_price_cap_rate,
        "max_price_cash_on_cash": max_price_coc,
        "recommended_max_offer": min(max_price_cap_rate, max_price_coc),
        "target_cap_rate": target_cap_rate,
        "target_cash_on_cash": target_cash_on_cash
    } 