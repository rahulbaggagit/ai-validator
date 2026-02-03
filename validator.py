"""
AI Output Validator - Core Logic

This module contains the core validation logic for testing AI consistency:
- Calling the Anthropic API multiple times with the same prompt
- Parsing AI responses to extract metrics
- Calculating consistency scores
- Generating comparison tables

Author: AI & Data Consultant
Purpose: Test AI agent output consistency before production deployment
"""

import re
import anthropic
import pandas as pd
from typing import List, Dict, Any, Tuple
from statistics import mean, stdev


# =============================================================================
# API INTERACTION
# =============================================================================

def run_business_case(
    prompt: str,
    api_key: str,
    num_runs: int = 3,
    model: str = "claude-sonnet-4-20250514",
    temperature: float = 1.0,
    max_tokens: int = 4000
) -> List[Dict[str, Any]]:
    """
    Run the same business case prompt multiple times to test consistency.
    
    This is the main function that calls the Anthropic API. It runs the same
    prompt multiple times and returns all responses for comparison.
    
    Args:
        prompt (str): The business case prompt to send to the AI
        api_key (str): Anthropic API key
        num_runs (int): Number of times to run the prompt (default: 3)
        model (str): Claude model to use (default: claude-sonnet-4-20250514)
        temperature (float): Temperature setting (default: 1.0)
        max_tokens (int): Maximum tokens in response (default: 4000)
    
    Returns:
        List[Dict]: List of results, each containing:
            - run_number: Which run this was (1, 2, 3...)
            - response_text: The full AI response
            - metrics: Extracted metrics (populated by extract_metrics)
            - raw_response: The full API response object
    
    Raises:
        anthropic.APIError: If API calls fail
        ValueError: If api_key is invalid
    
    Example:
        >>> results = run_business_case(prompt, api_key, num_runs=3)
        >>> print(f"Got {len(results)} responses")
        Got 3 responses
    """
    if not api_key or api_key.strip() == "":
        raise ValueError("API key is required")
    
    # Initialize the Anthropic client
    client = anthropic.Anthropic(api_key=api_key)
    
    results = []
    
    # Run the prompt multiple times
    for run_num in range(1, num_runs + 1):
        try:
            # Call the Anthropic API
            # Note: We use the Messages API (the modern approach)
            message = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract the text response
            response_text = message.content[0].text
            
            # Store the result
            result = {
                "run_number": run_num,
                "response_text": response_text,
                "metrics": extract_metrics(response_text),  # Parse metrics immediately
                "raw_response": message
            }
            
            results.append(result)
            
        except anthropic.APIError as e:
            # Handle API errors gracefully
            raise anthropic.APIError(f"API call failed on run {run_num}: {str(e)}")
    
    return results


# =============================================================================
# METRIC EXTRACTION (PARSING)
# =============================================================================

def extract_metrics(ai_response: str) -> Dict[str, Any]:
    """
    Extract key metrics from an AI response using regex patterns.
    
    This function parses the AI's text response to find:
    - Dollar amounts (e.g., "$1,234,567" or "$1,234,567.89")
    - Percentages (e.g., "45.2%" or "100%")
    - Time periods in months (e.g., "12.5 months" or "6 months")
    - Recommendations (keywords like "proceed", "recommend", etc.)
    
    Args:
        ai_response (str): The full text response from the AI
    
    Returns:
        Dict[str, Any]: Dictionary containing extracted metrics:
            - dollar_amounts: List of all dollar values found
            - percentages: List of all percentage values found
            - months: List of all month values found
            - recommendation: Classification of recommendation (PROCEED, CAUTION, or DO_NOT_PROCEED)
            - raw_recommendation_text: The actual text containing the recommendation
    
    Example:
        >>> text = "Annual savings: $1,500,000. ROI: 250%. Payback: 8.5 months. Recommendation: PROCEED"
        >>> metrics = extract_metrics(text)
        >>> metrics['dollar_amounts']
        [1500000.0]
    """
    metrics = {
        "dollar_amounts": [],
        "percentages": [],
        "months": [],
        "recommendation": None,
        "raw_recommendation_text": None
    }
    
    # -------------------------------------------------------------------------
    # EXTRACT DOLLAR AMOUNTS
    # -------------------------------------------------------------------------
    # Pattern: $1,234,567 or $1,234,567.89
    # We'll find all matches and convert to float
    dollar_pattern = r'\$[\d,]+(?:\.\d{2})?'
    dollar_matches = re.findall(dollar_pattern, ai_response)
    
    for match in dollar_matches:
        # Remove $ and commas, then convert to float
        clean_value = match.replace('$', '').replace(',', '')
        try:
            metrics["dollar_amounts"].append(float(clean_value))
        except ValueError:
            # Skip if conversion fails
            continue
    
    # -------------------------------------------------------------------------
    # EXTRACT PERCENTAGES
    # -------------------------------------------------------------------------
    # Pattern: 45.2% or 100%
    # Look for numbers followed by % sign
    percentage_pattern = r'(\d+(?:\.\d+)?)\s*%'
    percentage_matches = re.findall(percentage_pattern, ai_response)
    
    for match in percentage_matches:
        try:
            metrics["percentages"].append(float(match))
        except ValueError:
            continue
    
    # -------------------------------------------------------------------------
    # EXTRACT TIME PERIODS (MONTHS)
    # -------------------------------------------------------------------------
    # Pattern: "12.5 months" or "6 months"
    # Look for numbers followed by "month" or "months"
    months_pattern = r'(\d+(?:\.\d+)?)\s*months?'
    months_matches = re.findall(months_pattern, ai_response, re.IGNORECASE)
    
    for match in months_matches:
        try:
            metrics["months"].append(float(match))
        except ValueError:
            continue
    
    # -------------------------------------------------------------------------
    # EXTRACT RECOMMENDATION
    # -------------------------------------------------------------------------
    # Look for recommendation keywords in the text
    # We'll classify as: PROCEED, PROCEED_WITH_CAUTION, or DO_NOT_PROCEED
    
    response_lower = ai_response.lower()
    
    # Try to find the recommendation section (usually at the end)
    recommendation_section = ""
    if "recommendation:" in response_lower:
        recommendation_section = ai_response[response_lower.index("recommendation:"):]
    elif "should" in response_lower and "proceed" in response_lower:
        # Look for sentences with "should" and "proceed"
        sentences = ai_response.split('.')
        for sentence in sentences:
            if "should" in sentence.lower() and "proceed" in sentence.lower():
                recommendation_section = sentence
                break
    
    metrics["raw_recommendation_text"] = recommendation_section.strip()
    
    # Classify the recommendation
    rec_lower = recommendation_section.lower()
    
    if any(keyword in rec_lower for keyword in ["do not proceed", "not recommended", "reconsider", "advise against"]):
        metrics["recommendation"] = "DO_NOT_PROCEED"
    elif any(keyword in rec_lower for keyword in ["proceed with caution", "conditional", "carefully consider"]):
        metrics["recommendation"] = "PROCEED_WITH_CAUTION"
    elif any(keyword in rec_lower for keyword in ["proceed", "recommend", "go ahead", "move forward", "approve"]):
        metrics["recommendation"] = "PROCEED"
    else:
        metrics["recommendation"] = "UNCLEAR"
    
    return metrics


def extract_specific_metric(
    ai_response: str,
    metric_name: str,
    context_words: List[str] = None
) -> Any:
    """
    Extract a specific named metric from the AI response.
    
    This is a more targeted extraction function that looks for specific metrics
    by name (e.g., "Annual Savings", "Payback Period", etc.)
    
    Args:
        ai_response (str): The AI response text
        metric_name (str): The name of the metric to find (e.g., "Annual Savings")
        context_words (List[str]): Optional list of context words that might appear near the metric
    
    Returns:
        Any: The extracted value (float for numbers, str for text)
    
    TODO: Implement more sophisticated metric extraction using context
    TODO: Add support for extracting metrics from tables in the response
    """
    # This is a placeholder for more advanced extraction
    # You can enhance this based on your specific needs
    
    # For now, use the general extraction and let the user specify which value
    metrics = extract_metrics(ai_response)
    
    # Return the first matching type based on metric name
    if "cost" in metric_name.lower() or "savings" in metric_name.lower():
        return metrics["dollar_amounts"][0] if metrics["dollar_amounts"] else None
    elif "percentage" in metric_name.lower() or "roi" in metric_name.lower():
        return metrics["percentages"][0] if metrics["percentages"] else None
    elif "payback" in metric_name.lower() or "period" in metric_name.lower():
        return metrics["months"][0] if metrics["months"] else None
    elif "recommendation" in metric_name.lower():
        return metrics["recommendation"]
    
    return None


# =============================================================================
# CONSISTENCY ANALYSIS
# =============================================================================

def calculate_consistency_score(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate a consistency score by comparing metrics across multiple runs.
    
    This is the core validation function. It compares the extracted metrics
    from multiple AI runs and calculates a score based on how consistent they are.
    
    Scoring Logic:
    - For numeric metrics (costs, percentages, time periods):
        - All 3 values identical: +25 points
        - Variance < 2%: +20 points
        - Variance 2-5%: +15 points
        - Variance 5-10%: +10 points
        - Variance > 10%: +0 points
    
    - For recommendations:
        - All 3 match: +25 points
        - 2 of 3 match: +15 points
        - All different: +0 points
    
    Args:
        results (List[Dict]): List of results from run_business_case()
    
    Returns:
        Dict containing:
            - total_score: Overall consistency score (0-100)
            - max_possible_score: Maximum achievable score
            - metric_scores: Breakdown of scores by metric
            - variances: Calculated variances for each metric
            - status: Text status (PRODUCTION_READY, NEEDS_TUNING, etc.)
            - findings: List of specific findings/issues
            - recommendations: List of recommendations for improvement
    
    Example:
        >>> results = run_business_case(prompt, api_key, num_runs=3)
        >>> score_data = calculate_consistency_score(results)
        >>> print(f"Score: {score_data['total_score']}/100")
        Score: 87/100
    """
    # Initialize scoring structure
    scoring = {
        "total_score": 0,
        "max_possible_score": 0,
        "metric_scores": {},
        "variances": {},
        "findings": [],
        "recommendations": []
    }
    
    # Extract all metrics from results
    all_metrics = [result["metrics"] for result in results]
    
    # -------------------------------------------------------------------------
    # ANALYZE DOLLAR AMOUNTS
    # -------------------------------------------------------------------------
    # Compare the first few dollar amounts across runs (usually the key costs)
    # We'll check up to 5 dollar amounts
    for i in range(5):
        values = []
        for metrics in all_metrics:
            if i < len(metrics["dollar_amounts"]):
                values.append(metrics["dollar_amounts"][i])
        
        if len(values) >= 2:  # Need at least 2 values to compare
            score, variance = _score_numeric_metric(values)
            metric_name = f"dollar_amount_{i+1}"
            scoring["metric_scores"][metric_name] = score
            scoring["variances"][metric_name] = variance
            scoring["total_score"] += score
            scoring["max_possible_score"] += 25
            
            # Add findings if there's significant variance
            if variance > 2.0:
                scoring["findings"].append(
                    f"⚠️ Dollar amount #{i+1} varies by {variance:.1f}% across runs"
                )
    
    # -------------------------------------------------------------------------
    # ANALYZE PERCENTAGES
    # -------------------------------------------------------------------------
    for i in range(3):  # Check up to 3 percentages
        values = []
        for metrics in all_metrics:
            if i < len(metrics["percentages"]):
                values.append(metrics["percentages"][i])
        
        if len(values) >= 2:
            score, variance = _score_numeric_metric(values)
            metric_name = f"percentage_{i+1}"
            scoring["metric_scores"][metric_name] = score
            scoring["variances"][metric_name] = variance
            scoring["total_score"] += score
            scoring["max_possible_score"] += 25
            
            if variance > 5.0:
                scoring["findings"].append(
                    f"⚠️ Percentage #{i+1} varies by {variance:.1f}% across runs"
                )
    
    # -------------------------------------------------------------------------
    # ANALYZE TIME PERIODS (MONTHS)
    # -------------------------------------------------------------------------
    for i in range(2):  # Check up to 2 time periods
        values = []
        for metrics in all_metrics:
            if i < len(metrics["months"]):
                values.append(metrics["months"][i])
        
        if len(values) >= 2:
            score, variance = _score_numeric_metric(values)
            metric_name = f"months_{i+1}"
            scoring["metric_scores"][metric_name] = score
            scoring["variances"][metric_name] = variance
            scoring["total_score"] += score
            scoring["max_possible_score"] += 25
            
            if variance > 10.0:
                scoring["findings"].append(
                    f"⚠️ Time period #{i+1} varies by {variance:.1f}% across runs"
                )
    
    # -------------------------------------------------------------------------
    # ANALYZE RECOMMENDATIONS
    # -------------------------------------------------------------------------
    recommendations = [metrics["recommendation"] for metrics in all_metrics]
    rec_score = _score_recommendation(recommendations)
    scoring["metric_scores"]["recommendation"] = rec_score
    scoring["total_score"] += rec_score
    scoring["max_possible_score"] += 25
    
    if rec_score == 25:
        scoring["findings"].append("✅ Final recommendation is consistent across all runs")
    elif rec_score == 15:
        scoring["findings"].append("⚠️ Recommendation varies - 2 out of 3 runs agree")
    else:
        scoring["findings"].append("❌ Recommendations are inconsistent across runs")
    
    # -------------------------------------------------------------------------
    # CALCULATE FINAL SCORE (NORMALIZED TO 100)
    # -------------------------------------------------------------------------
    if scoring["max_possible_score"] > 0:
        scoring["total_score"] = int(
            (scoring["total_score"] / scoring["max_possible_score"]) * 100
        )
    else:
        scoring["total_score"] = 0
    
    # -------------------------------------------------------------------------
    # DETERMINE STATUS
    # -------------------------------------------------------------------------
    score = scoring["total_score"]
    if score >= 95:
        scoring["status"] = "PRODUCTION_READY"
        scoring["status_emoji"] = "✅"
        scoring["status_color"] = "green"
    elif score >= 85:
        scoring["status"] = "NEEDS_TUNING"
        scoring["status_emoji"] = "⚠️"
        scoring["status_color"] = "yellow"
    elif score >= 70:
        scoring["status"] = "NEEDS_PROMPT_ENGINEERING"
        scoring["status_emoji"] = "🔧"
        scoring["status_color"] = "orange"
    else:
        scoring["status"] = "NOT_READY"
        scoring["status_emoji"] = "❌"
        scoring["status_color"] = "red"
    
    # -------------------------------------------------------------------------
    # GENERATE RECOMMENDATIONS
    # -------------------------------------------------------------------------
    if score < 95:
        scoring["recommendations"].append(
            "1. Add structured JSON output format to your prompt for more consistent parsing"
        )
    
    if score < 85:
        scoring["recommendations"].append(
            "2. Reduce temperature to 0.0 for more deterministic outputs"
        )
    
    if score < 70:
        scoring["recommendations"].append(
            "3. Add explicit calculation validation steps in the prompt"
        )
        scoring["recommendations"].append(
            "4. Consider breaking complex analysis into smaller, focused prompts"
        )
    
    if rec_score < 25:
        scoring["recommendations"].append(
            "5. Provide clearer decision criteria for recommendations in the prompt"
        )
    
    return scoring


def _score_numeric_metric(values: List[float]) -> Tuple[int, float]:
    """
    Score a numeric metric based on variance across runs.
    
    Args:
        values (List[float]): List of values from different runs
    
    Returns:
        Tuple[int, float]: (score, variance_percentage)
    """
    if not values or len(values) < 2:
        return 0, 0.0
    
    # Check if all values are identical
    if len(set(values)) == 1:
        return 25, 0.0
    
    # Calculate variance as percentage
    avg = mean(values)
    if avg == 0:
        return 0, 100.0
    
    # Calculate percentage difference from mean
    variances = [abs(v - avg) / avg * 100 for v in values]
    max_variance = max(variances)
    
    # Score based on variance
    if max_variance < 2.0:
        score = 20
    elif max_variance < 5.0:
        score = 15
    elif max_variance < 10.0:
        score = 10
    else:
        score = 0
    
    return score, max_variance


def _score_recommendation(recommendations: List[str]) -> int:
    """
    Score recommendation consistency.
    
    Args:
        recommendations (List[str]): List of recommendations from different runs
    
    Returns:
        int: Score (0, 15, or 25)
    """
    if not recommendations:
        return 0
    
    # Count occurrences
    unique_recs = set(recommendations)
    
    if len(unique_recs) == 1:
        # All match
        return 25
    elif len(unique_recs) == 2 and len(recommendations) == 3:
        # 2 of 3 match
        return 15
    else:
        # All different
        return 0


# =============================================================================
# COMPARISON TABLE GENERATION
# =============================================================================

def generate_comparison_table(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Generate a pandas DataFrame comparing metrics across runs.
    
    This creates a side-by-side comparison table that's easy to display
    in Streamlit or export to CSV.
    
    Args:
        results (List[Dict]): List of results from run_business_case()
    
    Returns:
        pd.DataFrame: Comparison table with metrics as rows and runs as columns
    
    Example:
        >>> df = generate_comparison_table(results)
        >>> print(df)
                          Run #1        Run #2        Run #3
        Dollar Amount 1   $4,760,000   $4,760,000   $4,760,000
        Dollar Amount 2   $3,100,000   $3,100,000   $3,050,000
        ...
    """
    # Prepare data structure
    comparison_data = {}
    
    # Extract metrics from each run
    for result in results:
        run_num = result["run_number"]
        metrics = result["metrics"]
        
        col_name = f"Run #{run_num}"
        comparison_data[col_name] = []
    
    # Build rows for dollar amounts
    max_dollars = max(len(r["metrics"]["dollar_amounts"]) for r in results)
    row_labels = []
    
    for i in range(max_dollars):
        row_labels.append(f"Dollar Amount {i+1}")
        for result in results:
            col_name = f"Run #{result['run_number']}"
            metrics = result["metrics"]
            if i < len(metrics["dollar_amounts"]):
                value = metrics["dollar_amounts"][i]
                comparison_data[col_name].append(f"${value:,.2f}")
            else:
                comparison_data[col_name].append("N/A")
    
    # Build rows for percentages
    max_percentages = max(len(r["metrics"]["percentages"]) for r in results)
    for i in range(max_percentages):
        row_labels.append(f"Percentage {i+1}")
        for result in results:
            col_name = f"Run #{result['run_number']}"
            metrics = result["metrics"]
            if i < len(metrics["percentages"]):
                value = metrics["percentages"][i]
                comparison_data[col_name].append(f"{value:.1f}%")
            else:
                comparison_data[col_name].append("N/A")
    
    # Build rows for months
    max_months = max(len(r["metrics"]["months"]) for r in results)
    for i in range(max_months):
        row_labels.append(f"Time Period {i+1}")
        for result in results:
            col_name = f"Run #{result['run_number']}"
            metrics = result["metrics"]
            if i < len(metrics["months"]):
                value = metrics["months"][i]
                comparison_data[col_name].append(f"{value:.1f} months")
            else:
                comparison_data[col_name].append("N/A")
    
    # Build row for recommendation
    row_labels.append("Recommendation")
    for result in results:
        col_name = f"Run #{result['run_number']}"
        metrics = result["metrics"]
        comparison_data[col_name].append(metrics["recommendation"])
    
    # Create DataFrame
    df = pd.DataFrame(comparison_data, index=row_labels)
    
    return df


# TODO: Add support for custom metric extractors (user-defined regex patterns)
# TODO: Add visualization functions (charts showing variance across runs)
# TODO: Add export functionality (JSON, CSV, PDF report generation)
# TODO: Add statistical significance testing for variances
# TODO: Support for comparing against expected values from prompts.py
