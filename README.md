# 🔍 AI Business Case Validator

A professional tool for testing AI agent consistency before deploying to production. Built for AI & Data Consultants to demonstrate the importance of AI output validation to clients.

## 📋 Overview

This tool helps companies answer a critical question: **"Can we trust our AI agent to give consistent answers to executives?"**

It works by:
1. Running the same business case prompt multiple times
2. Extracting and comparing key metrics (costs, ROI, recommendations)
3. Calculating a consistency score (0-100)
4. Providing actionable recommendations for improvement

## 🎯 Use Cases

- **Pre-deployment Testing**: Validate AI agents before production rollout
- **Client Demos**: Show the importance of AI consistency testing
- **Prompt Engineering**: Compare different prompt strategies
- **Temperature Testing**: Find the right balance between creativity and consistency

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key** (choose one method):

   **Option A: Environment variable**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

   **Option B: .env file**
   Create a `.env` file in the project root:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ```

   **Option C: Enter in UI**
   You can also enter your API key directly in the Streamlit sidebar.

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 📁 Project Structure

```
ai-validator/
├── app.py                 # Main Streamlit application
├── validator.py           # Core validation logic (API calls, parsing, scoring)
├── prompts.py            # Business case scenarios
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .env                 # API keys (not in git)
```

## 🎮 How to Use

### Step 1: Configure Settings
- **API Key**: Enter your Anthropic API key in the sidebar
- **Scenario**: Choose from pre-built business cases:
  - Cloud Migration ROI
  - Warehouse Automation
  - AI Customer Service Chatbot
- **Temperature**: Adjust AI creativity (1.0 = test consistency, 0.0 = deterministic)
- **Runs**: Choose how many times to test (default: 3)

### Step 2: Run Validation
- Click **"Run Validation Test"**
- Wait for AI to process (usually 30-60 seconds)

### Step 3: Review Results
- **Consistency Score**: See your 0-100 score with color coding
- **AI Outputs**: Review all responses in expandable boxes
- **Comparison Table**: Side-by-side metric comparison
- **Findings**: Specific variances detected
- **Recommendations**: Actionable improvement suggestions

### Step 4: Export Results
- Download comparison table as CSV
- Download full report as TXT

## 📊 Understanding Scores

| Score Range | Status | Meaning | Action |
|------------|--------|---------|--------|
| 95-100 | ✅ Production Ready | Excellent consistency | Safe to deploy |
| 85-94 | ⚠️ Needs Tuning | Good but could improve | Minor adjustments needed |
| 70-84 | 🔧 Needs Engineering | Significant variance | Prompt rewrite required |
| Below 70 | ❌ Not Ready | Inconsistent outputs | Major issues, do not deploy |

## 🔧 Customization Guide

### Adding New Scenarios

Edit `prompts.py` and add your scenario:

```python
MY_CUSTOM_SCENARIO = {
    "name": "Your Scenario Name",
    "description": "Brief description",
    "prompt": """Your detailed prompt here...""",
    "expected_metrics": {
        "current_cost": 1000000,
        "roi_percentage": 150,
        # etc...
    },
    "tolerance": {
        "dollar_amounts": 2.0,
        "percentages": 5.0,
        "time_periods": 10.0
    }
}

# Add to SCENARIOS dictionary
SCENARIOS["Your Scenario Name"] = MY_CUSTOM_SCENARIO
```

### Adjusting Scoring Logic

Edit the `calculate_consistency_score()` function in `validator.py`:

```python
# Current scoring thresholds:
if max_variance < 2.0:
    score = 20  # Modify these values
elif max_variance < 5.0:
    score = 15
# etc...
```

### Custom Metric Extraction

Add your own regex patterns in `extract_metrics()` in `validator.py`:

```python
# Example: Extract custom patterns
custom_pattern = r'your_regex_here'
custom_matches = re.findall(custom_pattern, ai_response)
```

## 💡 Best Practices

### For Testing Consistency
- **Use Temperature 1.0**: Tests real-world variance
- **Run 3-5 times**: Good balance between thoroughness and speed
- **Test edge cases**: Try scenarios with ambiguous inputs

### For Production Deployment
- **Use Temperature 0.0**: Maximizes determinism
- **Add structured output**: Request JSON format in prompts
- **Validate calculations**: Include explicit calculation steps in prompts
- **Monitor continuously**: Test periodically even after deployment

### For Client Demos
1. Start with Temperature 1.0 to show variance
2. Show the consistency score (usually 70-90)
3. Adjust to Temperature 0.0 to demonstrate improvement
4. Explain the business impact of inconsistent AI outputs

## 🐛 Troubleshooting

### "API key is required" error
- Make sure you've entered a valid Anthropic API key
- Check that your key has sufficient credits

### "Rate limit exceeded" error
- Wait a few seconds and try again
- Reduce number of runs
- Check your API usage limits

### Metrics not parsing correctly
- Check the AI output format
- Adjust regex patterns in `validator.py`
- Consider requesting structured JSON output in prompts

### Low consistency scores
- Reduce temperature (try 0.5 or 0.0)
- Add more explicit instructions in the prompt
- Break complex tasks into smaller prompts
- Add examples to the prompt

## 🔒 Security Notes

- **Never commit API keys**: Use environment variables or `.env` files
- **Add `.env` to `.gitignore`**: Prevent accidental commits
- **Rotate keys regularly**: Follow security best practices
- **Limit key permissions**: Use least-privilege access

## 📚 Dependencies

- **Streamlit**: Web interface framework
- **Anthropic SDK**: Claude API integration
- **Pandas**: Data comparison and export
- **python-dotenv**: Environment variable management

## 🛠️ Advanced Features (TODO)

Future enhancements you can implement:

- [ ] Historical tracking (save test results to database)
- [ ] Multi-model comparison (OpenAI, Google, etc.)
- [ ] Custom metric definitions (user-defined extractors)
- [ ] Automated testing (CI/CD integration)
- [ ] Visualization charts (variance trends, distributions)
- [ ] Email reporting (scheduled reports to stakeholders)
- [ ] API endpoint (REST API for programmatic access)

## 📄 License

This is a demo project for educational purposes. Feel free to modify and use for your consulting work.

## 🤝 Contributing

This is a demo tool, but suggestions are welcome! Feel free to:
- Report bugs
- Suggest new scenarios
- Improve documentation
- Share your use cases

## 📧 Contact

Built by an AI & Data Consultant for demonstrating AI validation best practices.

---

**Remember**: Consistency testing is not optional—it's essential for production AI deployments. Use this tool to build trust with your clients and stakeholders.
