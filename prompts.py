"""
Business Case Scenario Prompts for AI Validation Testing

This module contains pre-built business case scenarios that can be used
to test AI output consistency. Each scenario includes:
- A detailed prompt with specific inputs
- Expected metrics for validation
- Clear calculation requirements

Author: AI & Data Consultant
Purpose: Demo tool for testing AI agent consistency
"""

# =============================================================================
# CLOUD MIGRATION ROI SCENARIO
# =============================================================================

CLOUD_MIGRATION_SCENARIO = {
    "name": "Cloud Migration ROI Analysis",
    "description": "Evaluate the financial case for migrating on-premise infrastructure to cloud",
    
    "prompt": """You are a financial analyst helping a company evaluate a cloud migration project.

**COMPANY BACKGROUND:**
- Mid-size manufacturing company
- Currently running on-premise data center
- 200 employees across 3 locations
- Annual IT budget: $6M

**CURRENT STATE (On-Premise):**
- Server hardware costs: $800,000/year (maintenance, replacement cycle)
- Data center facility costs: $1,200,000/year (power, cooling, rent)
- IT staff costs (infrastructure): $2,400,000/year (5 FTE @ avg $480k fully loaded)
- Software licensing: $360,000/year
- **Total Current Annual Cost: $4,760,000**

**PROPOSED STATE (Cloud Migration):**
- Cloud infrastructure (AWS): $1,800,000/year
- Managed services & support: $300,000/year
- IT staff costs (reduced): $720,000/year (1.5 FTE @ avg $480k fully loaded)
- Software licensing (cloud-optimized): $280,000/year
- **Total Proposed Annual Cost: $3,100,000**

**MIGRATION COSTS (One-Time):**
- Migration services & consulting: $450,000
- Staff training: $80,000
- Parallel run period (3 months): $150,000
- **Total Migration Investment: $680,000**

**YOUR TASK:**
Analyze this cloud migration opportunity and provide:

1. **Annual Savings**: Calculate the annual cost reduction
2. **Payback Period**: How many months to recover the migration investment?
3. **3-Year Total Savings**: Net savings over 3 years (after migration costs)
4. **ROI Percentage**: Return on investment over 3 years
5. **Recommendation**: Should the company proceed with migration? (PROCEED, PROCEED WITH CAUTION, or DO NOT PROCEED)

**IMPORTANT:** Show all calculations clearly. Use exact numbers from the scenario above.
Provide your final recommendation with a brief justification (2-3 sentences).

Format your response with clear sections and bold the key metrics.""",

    # Expected metrics for validation (approximate ranges acceptable)
    "expected_metrics": {
        "current_cost": 4760000,
        "proposed_cost": 3100000,
        "annual_savings": 1660000,
        "migration_cost": 680000,
        "payback_months": 4.9,  # 680000 / (1660000/12) ≈ 4.9 months
        "three_year_savings": 4300000,  # (1660000 * 3) - 680000
        "roi_percentage": 632,  # ((4980000 - 680000) / 680000) * 100
        "recommendation": "PROCEED"
    },
    
    # Tolerance levels for validation (percentage variance allowed)
    "tolerance": {
        "dollar_amounts": 2.0,  # 2% variance acceptable
        "percentages": 5.0,      # 5% variance acceptable
        "time_periods": 10.0     # 10% variance acceptable for months
    }
}


# =============================================================================
# WAREHOUSE AUTOMATION SCENARIO
# =============================================================================

WAREHOUSE_AUTOMATION_SCENARIO = {
    "name": "Warehouse Automation Investment",
    "description": "Assess the business case for implementing robotic automation in a distribution center",
    
    "prompt": """You are a financial analyst evaluating a warehouse automation project.

**COMPANY BACKGROUND:**
- E-commerce distribution company
- Processing 50,000 orders/day
- Current warehouse: 300,000 sq ft
- 180 warehouse employees

**CURRENT STATE (Manual Operations):**
- Warehouse labor costs: $8,640,000/year (180 employees @ $48k/year avg)
- Error/returns costs: $720,000/year (1.2% error rate on $60M annual volume)
- Overtime costs: $960,000/year (seasonal peaks)
- Equipment maintenance: $180,000/year (forklifts, conveyors)
- **Total Current Annual Cost: $10,500,000**

**PROPOSED STATE (Automated System):**
- Warehouse labor costs: $2,400,000/year (50 employees @ $48k/year avg)
- Robotic system operating costs: $1,200,000/year (maintenance, energy)
- Error/returns costs: $180,000/year (0.3% error rate - 75% reduction)
- System software licenses: $360,000/year
- **Total Proposed Annual Cost: $4,140,000**

**AUTOMATION INVESTMENT (One-Time):**
- Robotic picking systems: $8,500,000
- Installation & integration: $2,100,000
- Staff training & transition: $400,000
- **Total Investment: $11,000,000**

**YOUR TASK:**
Analyze this automation investment and provide:

1. **Annual Savings**: Calculate the annual operating cost reduction
2. **Payback Period**: How many months to recover the investment?
3. **5-Year Total Savings**: Net savings over 5 years (after investment)
4. **ROI Percentage**: Return on investment over 5 years
5. **Recommendation**: Should the company proceed? (PROCEED, PROCEED WITH CAUTION, or DO NOT PROCEED)

**IMPORTANT:** Show all calculations clearly. Consider the substantial upfront investment.
Provide your final recommendation with a brief justification (2-3 sentences).

Format your response with clear sections and bold the key metrics.""",

    "expected_metrics": {
        "current_cost": 10500000,
        "proposed_cost": 4140000,
        "annual_savings": 6360000,
        "investment_cost": 11000000,
        "payback_months": 20.8,  # 11000000 / (6360000/12) ≈ 20.8 months
        "five_year_savings": 20800000,  # (6360000 * 5) - 11000000
        "roi_percentage": 189,  # ((31800000 - 11000000) / 11000000) * 100
        "recommendation": "PROCEED"
    },
    
    "tolerance": {
        "dollar_amounts": 2.0,
        "percentages": 5.0,
        "time_periods": 10.0
    }
}


# =============================================================================
# AI CHATBOT SCENARIO
# =============================================================================

AI_CHATBOT_SCENARIO = {
    "name": "AI Customer Service Chatbot",
    "description": "Evaluate implementing an AI chatbot to handle customer service inquiries",
    
    "prompt": """You are a financial analyst evaluating an AI chatbot implementation for customer service.

**COMPANY BACKGROUND:**
- SaaS company with 50,000 active customers
- Customer service team handles 25,000 tickets/month
- Current CSAT (Customer Satisfaction): 78%
- Average response time: 6 hours

**CURRENT STATE (Human-Only Support):**
- Support staff costs: $2,880,000/year (30 agents @ $96k/year fully loaded)
- Support tools & software: $240,000/year
- Training & quality assurance: $180,000/year
- Escalation & overtime: $300,000/year
- **Total Current Annual Cost: $3,600,000**
- **Metrics:** 25,000 tickets/month, 6-hour avg response time, 78% CSAT

**PROPOSED STATE (AI Chatbot + Human Support):**
- Support staff costs: $1,440,000/year (15 agents @ $96k/year - handles complex cases)
- AI chatbot platform: $480,000/year (enterprise plan)
- Support tools & software: $240,000/year
- Training & quality assurance: $120,000/year
- **Total Proposed Annual Cost: $2,280,000**
- **Expected Metrics:** 
  - 60% of tickets resolved by AI (15,000/month)
  - Remaining 40% handled by humans (10,000/month)
  - Average response time: 30 minutes (AI) / 4 hours (human)
  - Expected CSAT: 82% (based on pilot data)

**IMPLEMENTATION COSTS (One-Time):**
- AI platform setup & customization: $180,000
- Knowledge base migration: $60,000
- Staff training on new system: $45,000
- 3-month pilot/transition: $75,000
- **Total Implementation Cost: $360,000**

**YOUR TASK:**
Analyze this AI chatbot investment and provide:

1. **Annual Savings**: Calculate the annual cost reduction
2. **Payback Period**: How many months to recover the implementation cost?
3. **3-Year Total Savings**: Net savings over 3 years (after implementation costs)
4. **ROI Percentage**: Return on investment over 3 years
5. **Additional Benefits**: Note the improvements in response time and CSAT
6. **Recommendation**: Should the company proceed? (PROCEED, PROCEED WITH CAUTION, or DO NOT PROCEED)

**IMPORTANT:** Show all calculations clearly. Consider both cost savings and service improvements.
Provide your final recommendation with a brief justification (2-3 sentences).

Format your response with clear sections and bold the key metrics.""",

    "expected_metrics": {
        "current_cost": 3600000,
        "proposed_cost": 2280000,
        "annual_savings": 1320000,
        "implementation_cost": 360000,
        "payback_months": 3.3,  # 360000 / (1320000/12) ≈ 3.3 months
        "three_year_savings": 3600000,  # (1320000 * 3) - 360000
        "roi_percentage": 1000,  # ((3960000 - 360000) / 360000) * 100
        "recommendation": "PROCEED"
    },
    
    "tolerance": {
        "dollar_amounts": 2.0,
        "percentages": 5.0,
        "time_periods": 10.0
    }
}


# =============================================================================
# SCENARIO REGISTRY
# =============================================================================

# Dictionary to easily access scenarios by name
SCENARIOS = {
    "Cloud Migration ROI": CLOUD_MIGRATION_SCENARIO,
    "Warehouse Automation": WAREHOUSE_AUTOMATION_SCENARIO,
    "AI Customer Service Chatbot": AI_CHATBOT_SCENARIO
}

# List of scenario names for UI dropdown
SCENARIO_NAMES = list(SCENARIOS.keys())


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_scenario(scenario_name):
    """
    Retrieve a scenario by name.
    
    Args:
        scenario_name (str): Name of the scenario to retrieve
        
    Returns:
        dict: Scenario dictionary with prompt, expected_metrics, etc.
        
    Raises:
        KeyError: If scenario name not found
    """
    if scenario_name not in SCENARIOS:
        raise KeyError(f"Scenario '{scenario_name}' not found. Available: {SCENARIO_NAMES}")
    
    return SCENARIOS[scenario_name]


def get_scenario_prompt(scenario_name):
    """
    Get just the prompt text for a scenario.
    
    Args:
        scenario_name (str): Name of the scenario
        
    Returns:
        str: The prompt text
    """
    scenario = get_scenario(scenario_name)
    return scenario["prompt"]


def get_expected_metrics(scenario_name):
    """
    Get the expected metrics for a scenario.
    
    Args:
        scenario_name (str): Name of the scenario
        
    Returns:
        dict: Expected metrics and their values
    """
    scenario = get_scenario(scenario_name)
    return scenario["expected_metrics"]


# TODO: Add more scenarios as needed
# TODO: Consider adding industry-specific scenarios (healthcare, finance, retail, etc.)
# TODO: Add difficulty levels (simple, intermediate, complex)
