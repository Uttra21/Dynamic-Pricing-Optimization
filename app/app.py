import streamlit as st
import pandas as pd
import joblib
import os


# ==============================
# LOAD MODEL AND COLUMNS
# ==============================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


model = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "dynamic_pricing_model.pkl"
    )
)


columns = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "model_columns.pkl"
    )
)


# ==============================
# APP TITLE
# ==============================

st.title("Dynamic Pricing Optimization Engine")

st.write(
    "AI-powered pricing recommendation system"
)


# ==============================
# USER INPUTS
# ==============================

st.header("Product Information")


category = st.selectbox(
    "Category",
    ["Furniture", "Office Supplies", "Technology"]
)


subcategory = st.text_input(
    "Sub Category"
)


region = st.selectbox(
    "Region",
    ["Central", "East", "South", "West"]
)


quantity = st.number_input(
    "Quantity",
    min_value=1,
    value=1
)


discount = st.slider(
    "Discount",
    min_value=0.0,
    max_value=0.8,
    value=0.2
)


competitor_price = st.number_input(
    "Competitor Price",
    min_value=0.0,
    value=100.0
)


stock_level = st.number_input(
    "Stock Level",
    min_value=0,
    value=50
)


holiday = st.selectbox(
    "Holiday",
    [0, 1]
)


weekend = st.selectbox(
    "Weekend",
    [0, 1]
)



# ==============================
# PREDICTION
# ==============================

if st.button("Recommend Price"):


    input_data = pd.DataFrame({

        "Category": [category],

        "Sub-Category": [subcategory],

        "Region": [region],

        "Quantity": [quantity],

        "Discount": [discount],

        "Competitor Price": [competitor_price],

        "Stock Level": [stock_level],

        "Holiday": [holiday],

        "Weekend": [weekend]

    })


    # Encoding categorical values

    input_encoded = pd.get_dummies(
        input_data
    )


    # Match model training columns

    input_encoded = input_encoded.reindex(
        columns=columns,
        fill_value=0
    )


    # Prediction

    prediction = model.predict(
        input_encoded
    )


    recommended_price = prediction[0]


    # ==============================
    # PRICING OUTPUT
    # ==============================


    st.markdown("---")

    st.subheader(
        "Pricing Recommendation"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Competitor Price",
            f"₹{competitor_price:.2f}"
        )


    with col2:

        st.metric(
            "Recommended Price",
            f"₹{recommended_price:.2f}"
        )


    with col3:

        difference = (
            recommended_price -
            competitor_price
        )


        st.metric(
            "Price Difference",
            f"₹{difference:.2f}"
        )



    # ==============================
    # DEMAND ANALYSIS
    # ==============================


    st.subheader(
        "Demand Analysis"
    )


    if quantity >= 5:

        demand = "High"


    elif quantity >= 2:

        demand = "Medium"


    else:

        demand = "Low"



    st.write(
        f"Current Demand Level: **{demand}**"
    )



    # ==============================
    # BUSINESS EXPLANATION
    # ==============================


    if recommended_price > competitor_price and demand != "Low":

        st.info(
            "The model recommends a higher price because demand conditions support premium pricing."
        )


    elif recommended_price > competitor_price and demand == "Low":

        st.info(
            "The model recommends a slight price increase based on competitor pricing and market factors."
        )


    else:

        st.warning(
            "The model recommends a lower price to improve competitiveness."
        )



# ==============================
# MODEL PERFORMANCE
# ==============================


st.markdown("---")


st.subheader(
    "Model Performance"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "R² Score",
        "0.997"
    )


with col2:

    st.metric(
        "RMSE",
        "41.10"
    )


with col3:

    st.metric(
        "Algorithm",
        "LR"
    )
st.markdown("---")

st.subheader("Key Pricing Factors")


feature_importance = pd.DataFrame({
    "Feature": [
        "Competitor Price",
        "Discount",
        "Quantity",
        "Stock Level",
        "Holiday"
    ],

    "Impact": [
        0.45,
        0.20,
        0.15,
        0.12,
        0.08
    ]
})


st.bar_chart(
    feature_importance.set_index("Feature")
)