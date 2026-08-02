import streamlit as st
import pandas as pd
import joblib
import os
import textwrap

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="PriceOpt AI",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- Main application ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(76, 110, 245, 0.10), transparent 28%),
            radial-gradient(circle at 95% 15%, rgba(124, 58, 237, 0.08), transparent 25%),
            #0b0f19;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }
    
    /* ---------- Native metric cards ---------- */

    div[data-testid="stMetric"] {
        
        background: #111724;
        border: 1px solid #273149;
        padding: 1.4rem 1.5rem;
        border-radius: 15px;
        min-height: 145px;
    }

    div[data-testid="stMetric"] label {
        color: #8d99ad !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
    }

    div[data-testid="stMetricDelta"] {
        font-weight: 700;
    } 

    /* ---------- Typography ---------- */

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 2.7rem !important;
        font-weight: 800 !important;
    }

    h2 {
        font-weight: 750 !important;
    }

    p {
        color: #aab3c5;
    }


    /* ---------- Header ---------- */

    .brand {
        font-size: 0.88rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        color: #8ea2ff;
        margin-bottom: 0.7rem;
    }

    .hero-title {
        font-size: 3rem;
        line-height: 1.08;
        font-weight: 850;
        color: #f8fafc;
        margin-bottom: 0.7rem;
        letter-spacing: -0.045em;
    }

    .hero-subtitle {
        color: #98a2b3;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
    }

    .status-pill {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        background: rgba(34, 197, 94, 0.10);
        border: 1px solid rgba(34, 197, 94, 0.25);
        color: #4ade80;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-top: 0.7rem;
    }


    /* ---------- Section labels ---------- */

    .section-label {
        color: #7f91ff;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }

    .section-title {
        color: #f8fafc;
        font-size: 1.55rem;
        font-weight: 750;
        margin-bottom: 1.1rem;
    }


    /* ---------- Input styling ---------- */

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #131927 !important;
        border-color: #252d40 !important;
        border-radius: 10px !important;
    }

    .stNumberInput input,
    .stTextInput input {
        background-color: #131927 !important;
    }

    label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }


    /* ---------- Button ---------- */

    .stButton > button {
        width: 100%;
        min-height: 3.2rem;
        border: none;
        border-radius: 11px;
        background: linear-gradient(
            90deg,
            #536dfe 0%,
            #7557f6 50%,
            #8b5cf6 100%
        );
        color: white;
        font-weight: 750;
        font-size: 1rem;
        letter-spacing: 0.01em;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.22);
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border: none;
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 10px 35px rgba(99, 102, 241, 0.34);
    }


    /* ---------- Divider ---------- */

    .custom-divider {
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            #293146,
            transparent
        );
        margin: 2.8rem 0;
    }


    /* ---------- Recommendation ---------- */

    .recommendation-card {
        background:
            linear-gradient(
                135deg,
                rgba(83, 109, 254, 0.15),
                rgba(124, 58, 237, 0.09)
            );
        border: 1px solid rgba(129, 140, 248, 0.26);
        border-radius: 18px;
        padding: 1.8rem;
        text-align: center;
        min-height: 180px;
    }

    .recommendation-label {
        color: #9ba8bd;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.11em;
        text-transform: uppercase;
    }

    .recommendation-price {
        color: #ffffff;
        font-size: 3.25rem;
        font-weight: 850;
        margin: 0.35rem 0;
        letter-spacing: -0.04em;
    }

    .recommendation-change-positive {
        color: #4ade80;
        font-size: 0.95rem;
        font-weight: 700;
    }

    .recommendation-change-negative {
        color: #fb7185;
        font-size: 0.95rem;
        font-weight: 700;
    }


    /* ---------- KPI cards ---------- */

    .kpi-card {
        background: #111724;
        border: 1px solid #242d40;
        border-radius: 15px;
        padding: 1.35rem 1.45rem;
        min-height: 130px;
    }

    .kpi-label {
        color: #8995a9;
        font-size: 0.75rem;
        font-weight: 750;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        margin-bottom: 0.65rem;
    }

    .kpi-value {
        color: #f8fafc;
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.03em;
    }

    .kpi-caption {
        color: #667085;
        font-size: 0.78rem;
        margin-top: 0.35rem;
    }


    /* ---------- Demand ---------- */

    .demand-box {
        background: #111724;
        border: 1px solid #242d40;
        border-radius: 15px;
        padding: 1.5rem;
        height: 100%;
    }

    .demand-badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        background: rgba(59, 130, 246, 0.12);
        border: 1px solid rgba(96, 165, 250, 0.22);
        color: #60a5fa;
        font-weight: 750;
        font-size: 0.82rem;
        margin-top: 0.4rem;
    }

    .strategy-badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        background: rgba(168, 85, 247, 0.12);
        border: 1px solid rgba(192, 132, 252, 0.22);
        color: #c084fc;
        font-weight: 750;
        font-size: 0.82rem;
        margin-top: 0.4rem;
    }


    /* ---------- Explanation ---------- */

    .explanation {
        background: rgba(59, 130, 246, 0.08);
        border: 1px solid rgba(96, 165, 250, 0.17);
        border-left: 3px solid #6366f1;
        border-radius: 10px;
        padding: 1.1rem 1.2rem;
        color: #b7c3d6;
        margin-top: 1.2rem;
        line-height: 1.65;
    }

    .explanation strong {
        color: #e5e7eb;
    }


    /* ---------- Performance ---------- */

    .performance-card {
        background: #111724;
        border: 1px solid #242d40;
        border-radius: 15px;
        padding: 1.4rem;
        min-height: 140px;
    }

    .performance-icon {
        font-size: 1.3rem;
        margin-bottom: 0.6rem;
    }

    .performance-label {
        color: #8792a7;
        font-size: 0.76rem;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .performance-value {
        color: #f8fafc;
        font-size: 1.85rem;
        font-weight: 800;
        margin-top: 0.25rem;
    }

    .performance-caption {
        color: #667085;
        font-size: 0.77rem;
        margin-top: 0.3rem;
    }
    
    /* ---------- Streamlit progress bars ---------- */

    div[data-testid="stProgress"] > div > div > div {
        background: linear-gradient(
           90deg,
           #536dfe,
           #8b5cf6
        );
    }

    div[data-testid="stProgress"] > div > div {
        background-color: #1b2232;
        border-radius: 999px;
    }

    div[data-testid="stProgress"] {
        margin-bottom: 1rem;
    } 

    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #4f596b;
        font-size: 0.78rem;
        margin-top: 3rem;
    }


    /* Remove Streamlit header spacing */

    header[data-testid="stHeader"] {
        background: transparent;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD MODEL, METRICS AND FEATURE IMPORTANCE
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

model = joblib.load(
    os.path.join(
        MODEL_DIR,
        "dynamic_pricing_pipeline.pkl"
    )
)

metrics = joblib.load(
    os.path.join(
        MODEL_DIR,
        "model_metrics.pkl"
    )
)

feature_importance = joblib.load(
    os.path.join(
        MODEL_DIR,
        "feature_importance.pkl"
    )
)
    
print("MODEL METRICS:", metrics)
print("FEATURE IMPORTANCE TYPE:", type(feature_importance))
print(feature_importance)

# =========================================================
# SESSION STATE
# =========================================================

if "pricing_result" not in st.session_state:
    st.session_state.pricing_result = None


# =========================================================
# HERO
# =========================================================

hero_left, hero_right = st.columns([4, 1])

with hero_left:

    st.markdown(
        """
        <div class="brand">◆ PRICEOPT AI</div>

        <div class="hero-title">
            Dynamic Pricing Intelligence
        </div>

        <div class="hero-subtitle">
            AI-powered pricing recommendations based on
            product, market and demand conditions.
        </div>

        <div class="status-pill">
            ● MODEL ACTIVE
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    '<div class="custom-divider"></div>',
    unsafe_allow_html=True
)


# =========================================================
# INPUT SECTION
# =========================================================

st.markdown(
    '<div class="section-label">Pricing Simulator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Configure Pricing Parameters</div>',
    unsafe_allow_html=True
)


left, right = st.columns(2, gap="large")


# ---------------------------------------------------------
# PRODUCT PARAMETERS
# ---------------------------------------------------------

with left:

    st.markdown("### 📦 Product Parameters")

    category = st.selectbox(
        "Category",
        [
            "Furniture",
            "Office Supplies",
            "Technology"
        ]
    )

    subcategory = st.text_input(
        "Sub Category",
        placeholder="Enter product sub-category"
    )

    region = st.selectbox(
        "Region",
        [
            "Central",
            "East",
            "South",
            "West"
        ]
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1,
        step=1
    )

    discount = st.slider(
        "Discount",
        min_value=0.0,
        max_value=0.8,
        value=0.2,
        step=0.01,
        format="%.2f"
    )

    st.caption(
        f"Selected discount: {discount * 100:.0f}%"
    )


# ---------------------------------------------------------
# MARKET CONDITIONS
# ---------------------------------------------------------

with right:

    st.markdown("### 📈 Market Conditions")

    competitor_price = st.number_input(
        "Competitor Price (₹)",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

    stock_level = st.number_input(
        "Stock Level",
        min_value=0,
        value=50,
        step=1
    )

    holiday_option = st.selectbox(
        "Holiday",
        ["No", "Yes"]
    )
    weekend_option = st.selectbox(
        "Weekend",
        ["No", "Yes"]
    )

    weather = st.selectbox(
        "Weather",
        ["Sunny", "Cloudy", "Rainy"]
    )

    demand_level = st.selectbox(
        "Demand Level",
        ["Low", "Medium", "High"]
    )

    # Convert user-friendly options to the
    # values expected by the ML model.

    holiday = 1 if holiday_option == "Yes" else 0
    weekend = 1 if weekend_option == "Yes" else 0

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption(
        "Market conditions help the model adjust pricing "
        "for demand and competitive pressure."
    )


# =========================================================
# GENERATE BUTTON
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

button_col1, button_col2, button_col3 = st.columns([1, 2, 1])

with button_col2:

    generate_price = st.button(
        "⚡ Generate Optimal Price",
        use_container_width=True
    )


# =========================================================
# PREDICTION
# =========================================================

if generate_price:
    
    
    demand_score_map = {
        "Low": 1,
        "Medium": 2,
        "High": 3
    }
    demand_score = demand_score_map[demand_level]
    input_data = pd.DataFrame(
        {
            "Category": [category],
            "Sub-Category": [subcategory],
            "Region": [region],
            "Quantity": [quantity],
            "Discount": [discount],
            "Competitor Price": [competitor_price],
            "Stock Level": [stock_level],
            "Holiday": [holiday],
            "Weekend": [weekend],
            "Weather": [weather],
            "Demand Level": [demand_level],
            "Demand Score": [demand_score]
        }
    )
    # Generate prediction using the trained preprocessing + model pipeline
    
    # ============================================================
    # CREATE ENGINEERED FEATURES FOR MODEL
    # ============================================================

    input_data["Competitor_Discount"] = (
        input_data["Competitor Price"] * input_data["Discount"]
    )

    input_data["Quantity_Discount"] = (
        input_data["Quantity"] * input_data["Discount"]
    )

    input_data["Stock_Quantity"] = (
        input_data["Stock Level"] * input_data["Quantity"]
    )

    input_data["Holiday_Weekend"] = (
        input_data["Holiday"] * input_data["Weekend"]
    )

    input_data["Competitor_Holiday"] = (
        input_data["Competitor Price"] * input_data["Holiday"]
    )
    prediction = model.predict(
        input_data
    )
    
    recommended_price = float(
        prediction[0]
)
    # -----------------------------------------------------
    # DEMAND
    # -----------------------------------------------------

    if quantity >= 5:
        demand = "High"

    elif quantity >= 2:
        demand = "Medium"

    else:
        demand = "Low"


    # -----------------------------------------------------
    # DIFFERENCE
    # -----------------------------------------------------

    difference = (
        recommended_price -
        competitor_price
    )

    if competitor_price > 0:

        percentage_difference = (
            difference /
            competitor_price
        ) * 100

    else:

        percentage_difference = 0


    # -----------------------------------------------------
    # STRATEGY
    # -----------------------------------------------------

    if recommended_price > competitor_price:

        strategy = "Premium Pricing"

    elif recommended_price < competitor_price:

        strategy = "Competitive Pricing"

    else:

        strategy = "Market Matching"


    # -----------------------------------------------------
    # EXPLANATION
    # -----------------------------------------------------

    if (
        recommended_price > competitor_price
        and demand != "Low"
    ):

        explanation = (
            "The model recommends pricing above the "
            "competitor because the current demand "
            "conditions support a premium pricing strategy."
        )

    elif (
        recommended_price > competitor_price
        and demand == "Low"
    ):

        explanation = (
            "The model recommends a moderate price increase "
            "based on competitor pricing and the supplied "
            "market conditions."
        )

    else:

        explanation = (
            "The model recommends a lower price to improve "
            "competitiveness under the current market "
            "conditions."
        )


    # Save result

    st.session_state.pricing_result = {
        "competitor_price": competitor_price,
        "recommended_price": recommended_price,
        "difference": difference,
        "percentage_difference": percentage_difference,
        "demand": demand,
        "strategy": strategy,
        "explanation": explanation
    }
# =========================================================
# PRICING RESULTS
# =========================================================

result = st.session_state.pricing_result

if result is not None:

    st.markdown(
        '<div class="custom-divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-label">AI Recommendation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Optimal Pricing Strategy</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # PRICE METRICS
    # -----------------------------------------------------

    price_col, competitor_col, difference_col = st.columns(
        [1.4, 1, 1],
        gap="large"
    )

    percentage = result["percentage_difference"]
    difference = result["difference"]

    with price_col:
        st.metric(
            label="💎 Recommended Price",
            value=f"₹{result['recommended_price']:.2f}",
            delta=f"{percentage:+.1f}% vs competitor"
        )

    with competitor_col:
        st.metric(
            label="Competitor Price",
            value=f"₹{result['competitor_price']:.2f}"
        )

    with difference_col:
        st.metric(
            label="Price Difference",
            value=f"₹{difference:+.2f}"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # DEMAND + STRATEGY
    # -----------------------------------------------------

    demand_col, strategy_col = st.columns(2, gap="large")

    with demand_col:

        st.markdown("##### Current Demand")

        if result["demand"] == "High":
            st.success("● HIGH DEMAND")

        elif result["demand"] == "Medium":
            st.info("● MEDIUM DEMAND")

        else:
            st.warning("● LOW DEMAND")

        st.caption(
            "Estimated from current order quantity"
        )

    with strategy_col:

        st.markdown("##### Pricing Strategy")

        st.info(
            f"◆ {result['strategy'].upper()}"
        )

        st.caption(
            "Strategy generated from model output"
        )

    # -----------------------------------------------------
    # EXPLANATION
    # -----------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="explanation">
            <strong>💡 Why this price?</strong>
            <br><br>
            {result['explanation']}
        </div>
        """,
        unsafe_allow_html=True
    )
     
# =========================================================
# MODEL PERFORMANCE
# =========================================================

st.markdown(
    '<div class="custom-divider"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-label">Model Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Model Performance</div>',
    unsafe_allow_html=True
)

perf1, perf2, perf3 = st.columns(3)

with perf1:
    st.markdown(
        textwrap.dedent(f"""
        <div class="performance-card">
            <div class="performance-icon">◎</div>
            <div class="performance-label">R² Score</div>
            <div class="performance-value">{metrics['r2']:.4f}</div>
            <div class="performance-caption">
                Variance explained by model
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

with perf2:
    st.markdown(
        textwrap.dedent(f"""
        <div class="performance-card">
            <div class="performance-icon">△</div>
            <div class="performance-label">RMSE</div>
            <div class="performance-value">{metrics['rmse']:.2f}</div>
            <div class="performance-caption">
                Root mean squared error
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

with perf3:
    st.markdown(
        textwrap.dedent("""
        <div class="performance-card">
            <div class="performance-icon">⚙</div>
            <div class="performance-label">Algorithm</div>
            <div class="performance-value" style="font-size:1.45rem;">
                Linear Regression
            </div>
            <div class="performance-caption">
                Active pricing prediction model
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

# =========================================================
# KEY PRICING FACTORS
# =========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-label">Model Insights</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Key Pricing Factors</div>',
    unsafe_allow_html=True
)

# ==========================================
# KEY PRICING FACTORS - REAL MODEL VALUES
# ==========================================

# Convert feature importance into a clean dictionary

if isinstance(feature_importance, pd.DataFrame):

    # Case: DataFrame with feature names + importance column

    if "Feature" in feature_importance.columns and "Importance" in feature_importance.columns:

        importance_dict = dict(
            zip(
                feature_importance["Feature"],
                feature_importance["Importance"]
            )
        )
        # Convert raw coefficient magnitudes into relative importance percentages
        total_importance = sum(
            abs(float(value))
            for value in importance_dict.values()
        )

        if total_importance > 0:
            importance_dict = {
                feature: abs(float(value)) / total_importance
                for feature, value in importance_dict.items()
            }

    else:
        # fallback: use first column as feature names
        # and second column as importance
        importance_dict = dict(
            zip(
                feature_importance.iloc[:, 0],
                feature_importance.iloc[:, 1]
            )
        )


elif isinstance(feature_importance, pd.Series):

    importance_dict = feature_importance.to_dict()


elif isinstance(feature_importance, dict):

    importance_dict = feature_importance


else:

    st.error(
        f"Unsupported feature importance format: {type(feature_importance)}"
    )

    importance_dict = {}
# Sort highest importance first
importance_dict = dict(
    sorted(
        importance_dict.items(),
        key=lambda x: float(x[1]),
        reverse=True
    )
)
# Keep only the Top 5 most important pricing factors
top_features = list(importance_dict.items())[:5]

# Cleaner names for engineered features
display_names = {
    "Competitor Price": "Competitor Price",
    "Competitor_Discount": "Competitor Price × Discount",
    "Competitor_Holiday": "Competitor Price × Holiday",
    "Quantity_Discount": "Quantity × Discount",
    "Stock_Quantity": "Stock Level × Quantity",
    "Holiday_Weekend": "Holiday × Weekend",
    "Sub-Category": "Sub-Category",
    "Category": "Category",
    "Quantity": "Quantity",
    "Discount": "Discount",
    "Stock Level": "Stock Level",
    "Holiday": "Holiday",
    "Region": "Region",
    "Weekend": "Weekend",
}

# Display only Top 5
for feature, impact in top_features:

    impact = float(impact)

    feature_label = display_names.get(feature, feature)

    label_col, value_col = st.columns([8, 1])

    with label_col:
        st.markdown(f"**{feature_label}**")

    with value_col:
        st.markdown(
            f"""
            <div style="
                text-align:right;
                color:#8ea2ff;
                font-weight:700;
            ">
                {impact * 100:.2f}%
            </div>
            """,
            unsafe_allow_html=True
        )

    st.progress(min(max(impact, 0.0), 1.0))
# =========================================================
# FOOTER
# =========================================================

st.markdown(
    textwrap.dedent("""
    <div class="footer">
        PriceOpt AI • Dynamic Pricing Optimization Engine
        <br>
        Machine Learning Powered Pricing Intelligence
    </div>
    """),
    unsafe_allow_html=True
)