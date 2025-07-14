"""
Mock property listings data for demonstration purposes.
In a real implementation, this would be replaced with API calls to property listing services.
"""

MOCK_PROPERTIES = [
    {
        "id": "prop_001",
        "address": "123 Main Street, Austin, TX 78701",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78701",
        "property_type": "Single Family",
        "price": 450000,
        "sqft": 2200,
        "bedrooms": 3,
        "bathrooms": 2,
        "year_built": 2015,
        "lot_size": 0.25,
        "rental_income": 2800,
        "property_tax": 8500,
        "insurance": 1200,
        "hoa_fees": 0,
        "maintenance_reserve": 300,
        "description": "Beautiful 3-bedroom home in prime Austin location with modern amenities and great rental potential.",
        "features": ["Hardwood floors", "Updated kitchen", "Large backyard", "Garage"],
        "market_trends": {
            "price_growth_1y": 8.5,
            "rent_growth_1y": 6.2,
            "days_on_market": 15
        }
    },
    {
        "id": "prop_002",
        "address": "456 Oak Avenue, Austin, TX 78702",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78702",
        "property_type": "Townhouse",
        "price": 380000,
        "sqft": 1800,
        "bedrooms": 2,
        "bathrooms": 2.5,
        "year_built": 2018,
        "lot_size": 0.15,
        "rental_income": 2400,
        "property_tax": 7200,
        "insurance": 1000,
        "hoa_fees": 150,
        "maintenance_reserve": 250,
        "description": "Modern townhouse with excellent location near downtown Austin, perfect for young professionals.",
        "features": ["Granite countertops", "Balcony", "Community pool", "Gym access"],
        "market_trends": {
            "price_growth_1y": 7.8,
            "rent_growth_1y": 5.9,
            "days_on_market": 22
        }
    },
    {
        "id": "prop_003",
        "address": "789 Pine Street, Austin, TX 78703",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78703",
        "property_type": "Multi-Family",
        "price": 650000,
        "sqft": 3200,
        "bedrooms": 4,
        "bathrooms": 4,
        "year_built": 2012,
        "lot_size": 0.35,
        "rental_income": 4200,
        "property_tax": 11000,
        "insurance": 1800,
        "hoa_fees": 0,
        "maintenance_reserve": 400,
        "description": "Duplex with excellent rental income potential in growing Austin neighborhood.",
        "features": ["Separate entrances", "Updated appliances", "Large yard", "Off-street parking"],
        "market_trends": {
            "price_growth_1y": 9.2,
            "rent_growth_1y": 7.1,
            "days_on_market": 18
        }
    },
    {
        "id": "prop_004",
        "address": "321 Elm Drive, Austin, TX 78704",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78704",
        "property_type": "Single Family",
        "price": 520000,
        "sqft": 2400,
        "bedrooms": 4,
        "bathrooms": 3,
        "year_built": 2016,
        "lot_size": 0.3,
        "rental_income": 3200,
        "property_tax": 9500,
        "insurance": 1400,
        "hoa_fees": 0,
        "maintenance_reserve": 350,
        "description": "Spacious family home with excellent schools and growing neighborhood value.",
        "features": ["Open floor plan", "Master suite", "Fireplace", "Patio"],
        "market_trends": {
            "price_growth_1y": 8.9,
            "rent_growth_1y": 6.5,
            "days_on_market": 12
        }
    },
    {
        "id": "prop_005",
        "address": "654 Maple Lane, Austin, TX 78705",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78705",
        "property_type": "Condo",
        "price": 320000,
        "sqft": 1400,
        "bedrooms": 2,
        "bathrooms": 2,
        "year_built": 2019,
        "lot_size": 0.05,
        "rental_income": 2100,
        "property_tax": 6000,
        "insurance": 800,
        "hoa_fees": 300,
        "maintenance_reserve": 200,
        "description": "Modern condo in prime location with excellent amenities and low maintenance.",
        "features": ["Concierge service", "Rooftop deck", "Fitness center", "Secure parking"],
        "market_trends": {
            "price_growth_1y": 6.5,
            "rent_growth_1y": 5.2,
            "days_on_market": 25
        }
    }
]

def get_properties_by_criteria(city=None, max_price=None, property_type=None):
    """
    Filter mock properties based on search criteria.
    
    Args:
        city (str): City name to filter by
        max_price (int): Maximum price filter
        property_type (str): Property type filter
    
    Returns:
        list: Filtered property listings
    """
    filtered_properties = MOCK_PROPERTIES.copy()
    
    if city:
        filtered_properties = [p for p in filtered_properties if p["city"].lower() == city.lower()]
    
    if max_price:
        filtered_properties = [p for p in filtered_properties if p["price"] <= max_price]
    
    if property_type:
        filtered_properties = [p for p in filtered_properties if p["property_type"].lower() == property_type.lower()]
    
    return filtered_properties

def get_property_by_id(property_id):
    """
    Get a specific property by its ID.
    
    Args:
        property_id (str): Property ID to search for
    
    Returns:
        dict: Property data or None if not found
    """
    for property in MOCK_PROPERTIES:
        if property["id"] == property_id:
            return property
    return None 