"""
AI Business Case Validator - Streamlit Application

This tool helps companies test if their AI agents produce consistent, trustworthy
outputs before deploying them to executives. It runs business case prompts multiple
times and calculates a consistency score.

Author: AI & Data Consultant
Purpose: Demo tool for AI consistency testing
"""

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Import our custom modules
from prompts import SCENARIOS, SCENARIO_NAMES, get_scenario_prompt
from validator import (
    run_business_case,
    calculate_consistency_score,
    generate_comparison_table
)
from demo_data import DEMO_RESULTS

# Load environment variables
load_dotenv()

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="AI Business Case Validator",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .score-box {
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0;
    }
    .score-production-ready {
        background-color: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
    }
    .score-needs-tuning {
        background-color: #fff3cd;
        color: #856404;
        border: 2px solid #ffeeba;
    }
    .score-needs-engineering {
        background-color: #ffe5cc;
        color: #cc5500;
        border: 2px solid #ffd4a3;
    }
    .score-not-ready {
        background-color: #f8d7da;
        color: #721c24;
        border: 2px solid #f5c6cb;
    }
    .metric-box {
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        background-color: #f8f9fa;
    }
    .findings-section {
        background-color: #e7f3ff;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .recommendation-section {
        background-color: #f0f7ff;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #4a90e2;
        margin: 1rem 0;
    }
    /* New styles for variance display */
    .problem-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #dc3545;
        text-align: center;
        margin: 1rem 0;
    }
    .problem-question {
        font-size: 1.4rem;
        font-weight: 600;
        color: #333;
        text-align: center;
        margin: 1.5rem 0;
        font-style: italic;
    }
    .variance-card {
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .variance-card-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .variance-value {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }
    .variance-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .variance-run {
        font-size: 0.8rem;
        opacity: 0.8;
        margin-top: 0.3rem;
    }
    .trust-score-box {
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem auto;
        max-width: 500px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    .trust-score-value {
        font-size: 4rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }
    .trust-score-label {
        font-size: 1.1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .trust-question {
        font-size: 1.2rem;
        margin-top: 1rem;
        opacity: 0.9;
    }
    .demo-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 1rem;
    }
    .warning-banner {
        background: linear-gradient(135deg, #ff9a56 0%, #ff6b6b 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR CONFIGURATION
# =============================================================================

st.sidebar.title("⚙️ Configuration")

# Demo Mode Toggle
st.sidebar.subheader("🎬 Mode")
demo_mode = st.sidebar.toggle(
    "Demo Mode",
    value=True,
    help="Use pre-loaded results for instant demo (no API key needed)"
)

if demo_mode:
    st.sidebar.success("Demo mode: Using pre-loaded results")
    api_key_input = "demo"  # Placeholder
else:
    # API Key Input
    st.sidebar.subheader("🔑 API Authentication")
    api_key_input = st.sidebar.text_input(
        "Anthropic API Key",
        type="password",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        help="Enter your Anthropic API key. You can also set ANTHROPIC_API_KEY environment variable."
    )

# Scenario Selection
st.sidebar.subheader("📋 Business Case Scenario")
selected_scenario = st.sidebar.selectbox(
    "Select a scenario to test:",
    options=SCENARIO_NAMES,
    help="Choose from pre-built business case scenarios"
)

# Temperature Slider
st.sidebar.subheader("🌡️ AI Settings")
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=1.0,
    step=0.1,
    help="Higher temperature = more variation. Use 1.0 to test consistency, 0.0 for deterministic outputs."
)

st.sidebar.markdown("---")

# Number of Runs
num_runs = st.sidebar.number_input(
    "Number of Test Runs",
    min_value=2,
    max_value=5,
    value=3,
    help="How many times to run the same prompt"
)

st.sidebar.markdown("---")

# Info Section
st.sidebar.subheader("ℹ️ About")
st.sidebar.info(
    """
    **AI Business Case Validator**

    See what happens when you ask AI for business cases multiple times.

    **The Problem:**
    Same prompt, different answers. Which one do you send to the client?

    **Trust Score:**
    - 95-100: High Trust ✅
    - 85-94: Medium Trust ⚠️
    - 70-84: Low Trust 🔧
    - <70: Don't Trust ❌
    """
)

# =============================================================================
# MAIN APPLICATION
# =============================================================================

# Header
if demo_mode:
    st.markdown('<div class="main-header">🔍 AI Business Case Validator <span class="demo-badge">DEMO</span></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="main-header">🔍 AI Business Case Validator</div>', unsafe_allow_html=True)

st.markdown("""
**What happens when you ask AI to build a business case 3 times?**

You get 3 different answers. Different ROI. Different payback periods. Different numbers.

*Which one do you put in the client proposal?*
""")

st.markdown("---")

# Display Selected Scenario
st.header("📝 Selected Business Case")
scenario_data = SCENARIOS[selected_scenario]

# Show scenario description
st.markdown(f"**Scenario:** {scenario_data['name']}")
st.markdown(f"*{scenario_data['description']}*")

# Show the prompt in an expander
with st.expander("👁️ View Full Prompt", expanded=False):
    st.code(scenario_data['prompt'], language=None)

st.markdown("---")

# =============================================================================
# VALIDATION TEST SECTION
# =============================================================================

st.header("🧪 Run Validation Test")

# Handle demo mode vs live mode
if demo_mode:
    # Demo mode - use pre-loaded results
    if st.button("🚀 See The Problem (Demo)", type="primary", use_container_width=True):
        # Load demo results
        demo_data = DEMO_RESULTS.get(selected_scenario)
        if demo_data:
            results = demo_data["results"]
            key_variance = demo_data["key_variance"]
            score_data = calculate_consistency_score(results)

            # Store in session state
            st.session_state['results'] = results
            st.session_state['score_data'] = score_data
            st.session_state['key_variance'] = key_variance
            st.session_state['show_results'] = True
            st.session_state['selected_scenario'] = selected_scenario

elif not api_key_input or api_key_input.strip() == "":
    st.warning("⚠️ Please enter your Anthropic API key in the sidebar to run the validation test.")
    st.info("💡 You can get an API key from https://console.anthropic.com/")
else:
    # Live mode - call API
    if st.button("🚀 Run Validation Test", type="primary", use_container_width=True):
        prompt = get_scenario_prompt(selected_scenario)
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            status_text.text("🔄 Running validation test...")
            results = run_business_case(
                prompt=prompt,
                api_key=api_key_input,
                num_runs=num_runs,
                temperature=temperature
            )
            progress_bar.progress(50)
            status_text.text("📊 Analyzing results...")
            score_data = calculate_consistency_score(results)
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")

            # Store in session state
            st.session_state['results'] = results
            st.session_state['score_data'] = score_data
            st.session_state['key_variance'] = None
            st.session_state['show_results'] = True
            st.session_state['selected_scenario'] = selected_scenario

        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Error during validation: {str(e)}")
            st.exception(e)

# =============================================================================
# DISPLAY RESULTS (persistent after button click)
# =============================================================================

if st.session_state.get('show_results') and st.session_state.get('selected_scenario') == selected_scenario:
    results = st.session_state['results']
    score_data = st.session_state['score_data']
    key_variance = st.session_state.get('key_variance')

    st.markdown("---")

    # =================================================================
    # THE PROBLEM - Visual variance display (hero section)
    # =================================================================

    st.markdown('<div class="problem-header">⚠️ THE PROBLEM: Same Prompt, Different Answers</div>', unsafe_allow_html=True)

    # Display the key metric that varies
    if key_variance:
        metric_name = key_variance['metric_name']
        values = key_variance['values']
        problem_statement = key_variance['problem_statement']

        st.markdown(f'<div class="warning-banner">{problem_statement}</div>', unsafe_allow_html=True)

        # Show the 3 different values side by side
        cols = st.columns(3)
        for i, (col, val) in enumerate(zip(cols, values)):
            with col:
                # Alternate colors for visual impact
                card_class = "variance-card" if i != 1 else "variance-card variance-card-warning"
                st.markdown(f'''
                <div class="{card_class}">
                    <div class="variance-label">{metric_name}</div>
                    <div class="variance-value">{val}</div>
                    <div class="variance-run">Run #{i+1}</div>
                </div>
                ''', unsafe_allow_html=True)
    else:
        # For live mode, extract key variance from results
        # Show ROI or first percentage that varies
        all_percentages = [r['metrics']['percentages'] for r in results if r['metrics']['percentages']]
        if all_percentages and len(all_percentages) >= 2:
            first_pcts = [p[0] for p in all_percentages if p]
            if len(set(first_pcts)) > 1:  # Values differ
                cols = st.columns(len(results))
                for i, (col, result) in enumerate(zip(cols, results)):
                    with col:
                        pct = result['metrics']['percentages'][0] if result['metrics']['percentages'] else 'N/A'
                        card_class = "variance-card" if i != 1 else "variance-card variance-card-warning"
                        st.markdown(f'''
                        <div class="{card_class}">
                            <div class="variance-label">ROI</div>
                            <div class="variance-value">{pct}%</div>
                            <div class="variance-run">Run #{i+1}</div>
                        </div>
                        ''', unsafe_allow_html=True)

    st.markdown('<div class="problem-question">"Which number do you put in the client proposal?"</div>', unsafe_allow_html=True)

    st.markdown("---")

    # =================================================================
    # TRUST SCORE (reframed from consistency score)
    # =================================================================

    score = score_data['total_score']
    status = score_data['status']

    # Determine styling based on score
    if score >= 95:
        bg_color = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"
        trust_label = "HIGH TRUST"
        trust_question = "Safe to send to clients"
    elif score >= 85:
        bg_color = "linear-gradient(135deg, #F2994A 0%, #F2C94C 100%)"
        trust_label = "MEDIUM TRUST"
        trust_question = "Review before sending"
    elif score >= 70:
        bg_color = "linear-gradient(135deg, #eb3349 0%, #f45c43 100%)"
        trust_label = "LOW TRUST"
        trust_question = "Needs validation"
    else:
        bg_color = "linear-gradient(135deg, #8E2DE2 0%, #4A00E0 100%)"
        trust_label = "DON'T TRUST"
        trust_question = "Do not use without review"

    st.markdown(f'''
    <div class="trust-score-box" style="background: {bg_color}; color: white;">
        <div class="trust-score-label">{trust_label}</div>
        <div class="trust-score-value">{score}%</div>
        <div class="trust-question">{trust_question}</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("---")

    # =================================================================
    # METRICS COMPARISON TABLE
    # =================================================================

    st.header("📊 Side-by-Side Comparison")
    st.markdown("*Look at how the numbers differ across runs:*")

    comparison_df = generate_comparison_table(results)

    # Display the comparison table with highlighting
    st.dataframe(
        comparison_df,
        use_container_width=True,
        height=350
    )

    st.markdown("---")

    # =================================================================
    # KEY FINDINGS (simplified)
    # =================================================================

    st.header("🔍 What This Means")

    if score_data['findings']:
        for finding in score_data['findings']:
            st.markdown(f"- {finding}")

    # =================================================================
    # AI OUTPUTS (collapsed by default)
    # =================================================================

    st.markdown("---")
    st.header("🤖 Full AI Responses")
    st.markdown("*Expand to see what the AI actually generated:*")

    for result in results:
        with st.expander(f"📄 Run #{result['run_number']}", expanded=False):
            st.markdown(result['response_text'])

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1.5rem 0;">
    <p style="font-size: 1rem; margin-bottom: 0.5rem;">
        <strong>AI outputs need validation before they reach your clients.</strong>
    </p>
    <p style="font-size: 0.85rem; color: #888;">
        Built by Rahul Bagga | Powered by Claude & Streamlit
    </p>
</div>
""", unsafe_allow_html=True)