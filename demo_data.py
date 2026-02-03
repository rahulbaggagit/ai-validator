"""
Demo Mode Data - Pre-loaded results showing AI inconsistency

These are realistic sample outputs that demonstrate the variance problem
without needing to call the API during a live demo.
"""

DEMO_RESULTS = {
    "Cloud Migration ROI": {
        "results": [
            {
                "run_number": 1,
                "response_text": """## Cloud Migration ROI Analysis

**1. Annual Savings**
- Current Annual Cost: $4,760,000
- Proposed Annual Cost: $3,100,000
- **Annual Savings: $1,660,000**

**2. Payback Period**
- Migration Investment: $680,000
- Monthly Savings: $138,333
- **Payback Period: 4.9 months**

**3. 3-Year Total Savings**
- Gross Savings (3 years): $4,980,000
- Less Migration Costs: $680,000
- **Net 3-Year Savings: $4,300,000**

**4. ROI Percentage**
- Total Return: $4,980,000
- Investment: $680,000
- **ROI: 632%**

**5. Recommendation: PROCEED**

The cloud migration presents a compelling financial case with a payback period under 5 months and substantial long-term savings. The 632% ROI over 3 years significantly exceeds typical IT investment thresholds.""",
                "metrics": {
                    "dollar_amounts": [4760000, 3100000, 1660000, 680000, 138333, 4980000, 4300000],
                    "percentages": [632],
                    "months": [4.9],
                    "recommendation": "PROCEED",
                    "raw_recommendation_text": "Recommendation: PROCEED"
                }
            },
            {
                "run_number": 2,
                "response_text": """## Cloud Migration Financial Analysis

**1. Annual Cost Reduction**
- Current State: $4,760,000/year
- Future State: $3,100,000/year
- **Annual Savings: $1,660,000**

**2. Investment Recovery Timeline**
- One-time Migration Cost: $680,000
- Monthly Cost Reduction: $138,333
- **Payback Period: 5.2 months**

**3. Three-Year Net Benefit**
- Total Savings (36 months): $4,980,000
- Migration Investment: $680,000
- **3-Year Net Savings: $4,300,000**

**4. Return on Investment**
- Net Benefit: $4,300,000
- Initial Investment: $680,000
- **3-Year ROI: 588%**

**5. Recommendation: PROCEED**

This migration offers excellent financial returns. With a payback period of approximately 5 months and strong ROI, the company should proceed with the cloud migration initiative.""",
                "metrics": {
                    "dollar_amounts": [4760000, 3100000, 1660000, 680000, 138333, 4980000, 4300000],
                    "percentages": [588],
                    "months": [5.2],
                    "recommendation": "PROCEED",
                    "raw_recommendation_text": "Recommendation: PROCEED"
                }
            },
            {
                "run_number": 3,
                "response_text": """## Cloud Migration Business Case

**1. Annual Savings Calculation**
- Current Annual Costs: $4,760,000
- Proposed Annual Costs: $3,100,000
- **Annual Savings: $1,660,000**

**2. Payback Analysis**
- Total Migration Investment: $680,000
- Savings per Month: ~$138,000
- **Payback Period: 4.5 months**

**3. 3-Year Financial Impact**
- Cumulative Savings: $4,980,000
- Less: Initial Investment: $680,000
- **Net 3-Year Savings: $4,300,000**

**4. ROI Calculation**
- Gain from Investment: $4,980,000
- Cost of Investment: $680,000
- **ROI: 732%**

**5. Recommendation: PROCEED**

The analysis strongly supports proceeding with the cloud migration. The quick payback period of under 5 months and exceptional 3-year ROI make this a low-risk, high-reward investment.""",
                "metrics": {
                    "dollar_amounts": [4760000, 3100000, 1660000, 680000, 138000, 4980000, 4300000],
                    "percentages": [732],
                    "months": [4.5],
                    "recommendation": "PROCEED",
                    "raw_recommendation_text": "Recommendation: PROCEED"
                }
            }
        ],
        "key_variance": {
            "metric_name": "ROI",
            "values": ["632%", "588%", "732%"],
            "variance_pct": 24.5,
            "problem_statement": "ROI varies by 144 percentage points across runs"
        }
    },

    "Warehouse Automation": {
        "results": [
            {
                "run_number": 1,
                "response_text": """## Warehouse Automation Investment Analysis

**1. Annual Operating Savings**
- Current Annual Cost: $10,500,000
- Proposed Annual Cost: $4,140,000
- **Annual Savings: $6,360,000**

**2. Payback Period**
- Total Investment: $11,000,000
- Monthly Savings: $530,000
- **Payback Period: 20.8 months**

**3. 5-Year Total Savings**
- Gross Savings (5 years): $31,800,000
- Less Investment: $11,000,000
- **Net 5-Year Savings: $20,800,000**

**4. ROI Percentage**
- Net Return: $20,800,000
- Investment: $11,000,000
- **5-Year ROI: 189%**

**5. Recommendation: PROCEED**

Despite the significant upfront investment, the automation project delivers strong returns with a payback period under 2 years and nearly 190% ROI over 5 years.""",
                "metrics": {
                    "dollar_amounts": [10500000, 4140000, 6360000, 11000000, 530000, 31800000, 20800000],
                    "percentages": [189],
                    "months": [20.8],
                    "recommendation": "PROCEED",
                    "raw_recommendation_text": "Recommendation: PROCEED"
                }
            },
            {
                "run_number": 2,
                "response_text": """## Warehouse Automation Business Case

**1. Annual Cost Reduction**
- Current Operating Costs: $10,500,000
- Future Operating Costs: $4,140,000
- **Annual Savings: $6,360,000**

**2. Investment Recovery**
- Capital Investment: $11,000,000
- Monthly Cost Reduction: $530,000
- **Payback Period: 24 months**

**3. Five-Year Net Benefit**
- Total Savings: $31,800,000
- Initial Investment: $11,000,000
- **5-Year Net Savings: $20,800,000**

**4. Return on Investment**
- Total Return: $31,800,000
- Investment Cost: $11,000,000
- **5-Year ROI: 289%**

**5. Recommendation: PROCEED WITH CAUTION**

While the long-term financials are attractive, the substantial $11M investment and 2-year payback period require careful consideration of cash flow implications and implementation risks.""",
                "metrics": {
                    "dollar_amounts": [10500000, 4140000, 6360000, 11000000, 530000, 31800000, 20800000],
                    "percentages": [289],
                    "months": [24],
                    "recommendation": "PROCEED_WITH_CAUTION",
                    "raw_recommendation_text": "Recommendation: PROCEED WITH CAUTION"
                }
            },
            {
                "run_number": 3,
                "response_text": """## Warehouse Automation ROI Analysis

**1. Annual Savings**
- Current State Costs: $10,500,000/year
- Future State Costs: $4,140,000/year
- **Annual Savings: $6,360,000**

**2. Payback Timeline**
- Automation Investment: $11,000,000
- Monthly Benefit: $530,000
- **Payback Period: 18 months**

**3. 5-Year Financial Impact**
- Cumulative Savings: $31,800,000
- Less: Upfront Investment: $11,000,000
- **Net 5-Year Savings: $20,800,000**

**4. ROI Analysis**
- Net Benefit: $20,800,000
- Initial Outlay: $11,000,000
- **5-Year ROI: 189%**

**5. Recommendation: PROCEED**

The automation investment is financially justified with strong savings potential. The 18-month payback and 189% ROI over 5 years provide a solid foundation for approval.""",
                "metrics": {
                    "dollar_amounts": [10500000, 4140000, 6360000, 11000000, 530000, 31800000, 20800000],
                    "percentages": [189],
                    "months": [18],
                    "recommendation": "PROCEED",
                    "raw_recommendation_text": "Recommendation: PROCEED"
                }
            }
        ],
        "key_variance": {
            "metric_name": "Payback Period",
            "values": ["20.8 months", "24 months", "18 months"],
            "variance_pct": 33.3,
            "problem_statement": "Payback period varies by 6 months - that's a 33% swing"
        }
    },

    "AI Customer Service Chatbot": {
        "results": [
            {
                "run_number": 1,
                "response_text": """## AI Chatbot Investment Analysis

**1. Annual Savings**
- Current Annual Cost: $3,600,000
- Proposed Annual Cost: $2,280,000
- **Annual Savings: $1,320,000**

**2. Payback Period**
- Implementation Cost: $360,000
- Monthly Savings: $110,000
- **Payback Period: 3.3 months**

**3. 3-Year Total Savings**
- Gross Savings: $3,960,000
- Less Implementation: $360,000
- **Net 3-Year Savings: $3,600,000**

**4. ROI Percentage**
- Total Return: $3,960,000
- Investment: $360,000
- **3-Year ROI: 1000%**

**5. Additional Benefits**
- Response time: 6 hours → 30 minutes (AI) / 4 hours (human)
- CSAT improvement: 78% → 82%

**6. Recommendation: PROCEED**

Exceptional ROI with quick payback. The AI chatbot not only reduces costs but improves customer experience metrics.""",
                "metrics": {
                    "dollar_amounts": [3600000, 2280000, 1320000, 360000, 110000, 3960000, 3600000],
                    "percentages": [1000, 78, 82],
                    "months": [3.3],
                    "recommendation": "PROCEED",
                    "raw_recommendation_text": "Recommendation: PROCEED"
                }
            },
            {
                "run_number": 2,
                "response_text": """## AI Customer Service Chatbot Business Case

**1. Annual Cost Reduction**
- Current Support Costs: $3,600,000
- Future Support Costs: $2,280,000
- **Annual Savings: $1,320,000**

**2. Investment Recovery**
- Setup & Implementation: $360,000
- Monthly Cost Reduction: $110,000
- **Payback Period: 4 months**

**3. Three-Year Net Benefit**
- Total Savings: $3,960,000
- Implementation Costs: $360,000
- **3-Year Net Savings: $3,600,000**

**4. Return on Investment**
- Net Gain: $3,600,000
- Initial Cost: $360,000
- **3-Year ROI: 900%**

**5. Service Improvements**
- Faster response times (30 min vs 6 hours)
- Higher customer satisfaction (82% vs 78%)

**6. Recommendation: PROCEED**

Strong financial case combined with service improvements makes this a compelling investment.""",
                "metrics": {
                    "dollar_amounts": [3600000, 2280000, 1320000, 360000, 110000, 3960000, 3600000],
                    "percentages": [900, 82, 78],
                    "months": [4],
                    "recommendation": "PROCEED",
                    "raw_recommendation_text": "Recommendation: PROCEED"
                }
            },
            {
                "run_number": 3,
                "response_text": """## AI Chatbot ROI Analysis

**1. Annual Savings Calculation**
- Current State: $3,600,000/year
- Future State: $2,280,000/year
- **Annual Savings: $1,320,000**

**2. Payback Analysis**
- One-time Investment: $360,000
- Savings per Month: $110,000
- **Payback Period: 3 months**

**3. 3-Year Financial Impact**
- Cumulative Savings: $3,960,000
- Less: Implementation: $360,000
- **Net 3-Year Savings: $3,600,000**

**4. ROI Calculation**
- Benefit: $3,960,000
- Cost: $360,000
- **3-Year ROI: 1100%**

**5. Qualitative Benefits**
- Response time reduction: 92% faster
- Customer satisfaction: +4 points

**6. Recommendation: PROCEED**

Outstanding ROI of over 1000% with minimal payback period. Strongly recommend implementation.""",
                "metrics": {
                    "dollar_amounts": [3600000, 2280000, 1320000, 360000, 110000, 3960000, 3600000],
                    "percentages": [1100, 92],
                    "months": [3],
                    "recommendation": "PROCEED",
                    "raw_recommendation_text": "Recommendation: PROCEED"
                }
            }
        ],
        "key_variance": {
            "metric_name": "ROI",
            "values": ["1000%", "900%", "1100%"],
            "variance_pct": 22.2,
            "problem_statement": "ROI ranges from 900% to 1100% - a 200 point spread"
        }
    }
}
