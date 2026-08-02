import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from sklearn.metrics import mean_squared_error, r2_score
from sklearn.inspection import permutation_importance


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "dynamic_pricing_dataset.csv"
)

MODELS_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODELS_DIR, exist_ok=True)


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(DATA_PATH)
print("\nALL DATASET COLUMNS:")
for col in df.columns:
    print("-", col)
print("\nCORRELATION WITH RECOMMENDED PRICE")
print("=" * 45)

check_columns = [
    "Demand Score",
    "Sales",
    "Quantity",
    "Profit",
    "Competitor Price",
    "Recommended Price"
]

print(
    df[check_columns]
    .corr(numeric_only=True)["Demand Score"]
    .sort_values(ascending=False)
)
print("\nWEATHER VALUES:")
print(df["Weather"].value_counts(dropna=False))

print("\nDEMAND LEVEL VALUES:")
print(df["Demand Level"].value_counts(dropna=False))
numeric_corr = df.select_dtypes(include="number").corr()["Recommended Price"]
numeric_corr = numeric_corr.sort_values(ascending=False)

print(numeric_corr)

print("Dataset loaded successfully.")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print("\nSAMPLE PRICING DATA")
print("=" * 80)

print(
    df[
        [
            "Recommended Price",
            "Competitor Price",
            "Discount",
            "Quantity",
            "Stock Level",
            "Holiday",
            "Weekend",
            "Demand Score"
        ]
    ].head(20).to_string(index=False)
)
# =========================================================
# FEATURE ENGINEERING
# =========================================================

# Interaction between competitor pricing and discount
df["Competitor_Discount"] = (
    df["Competitor Price"] * df["Discount"]
)

# Discount effect increases with quantity purchased
df["Quantity_Discount"] = (
    df["Quantity"] * df["Discount"]
)

# Inventory pressure based on stock and order quantity
df["Stock_Quantity"] = (
    df["Stock Level"] * df["Quantity"]
)

# Holiday + weekend demand interaction
df["Holiday_Weekend"] = (
    df["Holiday"] * df["Weekend"]
)

# Competitor pricing behaviour during holidays
df["Competitor_Holiday"] = (
    df["Competitor Price"] * df["Holiday"]
)

print("Feature engineering completed.")
# =========================================================
# FEATURES
# =========================================================

features = [
    "Category",
    "Sub-Category",
    "Region",
    "Weather",
    "Demand Level",
    "Quantity",
    "Discount",
    "Competitor Price",
    "Stock Level",
    "Holiday",
    "Weekend",
    "Competitor_Discount",
    "Quantity_Discount",
    "Stock_Quantity",
    "Holiday_Weekend",
    "Competitor_Holiday"
]
# =========================================================
# CREATE DYNAMIC PRICING TARGET
# =========================================================

# Start from competitor price as the market reference
# Historical selling price per unit
df["Historical Unit Price"] = (
    df["Sales"] / df["Quantity"].replace(0, 1)
)

# Use both market competition and historical selling behaviour
df["Base Market Price"] = (
    0.60 * df["Competitor Price"]
    + 0.40 * df["Historical Unit Price"]
)

# Starting point for dynamic pricing
df["Optimized Price"] = df["Base Market Price"].copy()

# -------------------------
# Demand adjustment
# -------------------------
demand_adjustment = {
    "Low": -0.05,       # reduce price by 5%
    "Medium": 0.00,     # no adjustment
    "High": 0.08        # increase price by 8%
}

df["Optimized Price"] *= (
    1 + df["Demand Level"].map(demand_adjustment).fillna(0)
)

# -------------------------
# Weather adjustment
# -------------------------
weather_adjustment = {
    "Rainy": 0.03,
    "Cloudy": 0.00,
    "Sunny": 0.02
}

df["Optimized Price"] *= (
    1 + df["Weather"].map(weather_adjustment).fillna(0)
)

# -------------------------
# Stock adjustment
# -------------------------
# Low stock -> price slightly higher
# High stock -> price slightly lower

stock_adjustment = np.where(
    df["Stock Level"] < 100,
    0.05,
    np.where(df["Stock Level"] > 250, -0.04, 0)
)

df["Optimized Price"] *= (1 + stock_adjustment)

# -------------------------
# Holiday adjustment
# -------------------------
df["Optimized Price"] *= (
    1 + (df["Holiday"] * 0.04)
)

# -------------------------
# Weekend adjustment
# -------------------------
df["Optimized Price"] *= (
    1 + (df["Weekend"] * 0.02)
)

# -------------------------
# Quantity adjustment
# -------------------------
# Larger orders receive a small bulk-price reduction

quantity_adjustment = np.where(
    df["Quantity"] >= 7,
    -0.04,
    np.where(df["Quantity"] >= 4, -0.02, 0)
)

df["Optimized Price"] *= (1 + quantity_adjustment)

# -------------------------
# Existing discount
# -------------------------
df["Optimized Price"] *= (
    1 - df["Discount"]
)

# Prevent invalid negative prices
df["Optimized Price"] = df["Optimized Price"].clip(lower=0.01)

print("\nOPTIMIZED PRICE SAMPLE")
print("=" * 60)

print(
    df[
        [
            "Competitor Price",
            "Demand Level",
            "Weather",
            "Stock Level",
            "Holiday",
            "Weekend",
            "Quantity",
            "Discount",
            "Optimized Price"
        ]
    ].head(10)
)
target = "Optimized Price"

X = df[features].copy()
y = df[target].copy()


# =========================================================
# FEATURE TYPES
# =========================================================
categorical_features = [
    "Category",
    "Sub-Category",
    "Region",
    "Weather",
    "Demand Level"
]

numerical_features = [
    "Quantity",
    "Discount",
    "Competitor Price",
    "Stock Level",
    "Holiday",
    "Weekend",
    "Competitor_Discount",
    "Quantity_Discount",
    "Stock_Quantity",
    "Holiday_Weekend",
    "Competitor_Holiday"
]


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")


# =========================================================
# PREPROCESSING
# =========================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),
        (
            "numerical",
            StandardScaler(),
            numerical_features
        )
    ]
)

# =========================================================
# MODEL TRAINING AND COMPARISON
# =========================================================

models = {
    "Linear Regression": {
        "model": LinearRegression(),
        "params": {}
    },

    "Random Forest": {
        "model": RandomForestRegressor(
            random_state=42
        ),
        "params": {
            "model__n_estimators": [100, 200],
            "model__max_depth": [None, 10, 20],
            "model__min_samples_split": [2, 5]
        }
    },

    "Gradient Boosting": {
        "model": GradientBoostingRegressor(
            random_state=42
        ),
        "params": {
            "model__n_estimators": [100, 200],
            "model__learning_rate": [0.05, 0.1],
            "model__max_depth": [2, 3, 5]
        }
    }
}


results = []

best_pipeline = None
best_model_name = None
best_rmse = float("inf")
best_r2 = None


# =========================================================
# TRAIN EACH MODEL
# =========================================================

for model_name, config in models.items():

    print("\n===================================")
    print(f"Training: {model_name}")
    print("===================================")

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", config["model"])
        ]
    )

    # ---------------------------------------------
    # GRID SEARCH FOR MODELS WITH PARAMETERS
    # ---------------------------------------------

    if config["params"]:

        grid_search = GridSearchCV(
            estimator=pipeline,
            param_grid=config["params"],
            cv=3,
            scoring="neg_root_mean_squared_error",
            n_jobs=-1
        )

        grid_search.fit(
            X_train,
            y_train
        )

        current_pipeline = grid_search.best_estimator_

        print(
            "Best Parameters:",
            grid_search.best_params_
        )

    else:

        pipeline.fit(
            X_train,
            y_train
        )

        current_pipeline = pipeline

    # ---------------------------------------------
    # MODEL EVALUATION
    # ---------------------------------------------

    predictions = current_pipeline.predict(
        X_test
    )

    current_r2 = r2_score(
        y_test,
        predictions
    )

    current_rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    print(f"R² Score : {current_r2:.4f}")
    print(f"RMSE     : {current_rmse:.2f}")

    results.append(
        {
            "Model": model_name,
            "R2": current_r2,
            "RMSE": current_rmse
        }
    )

    # ---------------------------------------------
    # SELECT BEST MODEL
    # ---------------------------------------------

    if current_rmse < best_rmse:

        best_rmse = current_rmse
        best_r2 = current_r2
        best_pipeline = current_pipeline
        best_model_name = model_name


# =========================================================
# MODEL COMPARISON
# =========================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="RMSE",
    ascending=True
).reset_index(drop=True)

print("\n\nMODEL COMPARISON")
print("===================================")

print(
    results_df.to_string(
        index=False
    )
)


# =========================================================
# WINNING MODEL
# =========================================================

pipeline = best_pipeline
r2 = best_r2
rmse = best_rmse

print("\n===================================")
print("BEST MODEL")
print("===================================")

print(f"Algorithm : {best_model_name}")
print(f"R² Score  : {r2:.4f}")
print(f"RMSE      : {rmse:.2f}")

# =========================================================
# PERMUTATION FEATURE IMPORTANCE
# =========================================================

print("\nCalculating feature importance...")

importance_result = permutation_importance(
    pipeline,
    X_test,
    y_test,
    n_repeats=10,
    random_state=42,
    scoring="r2"
)

importance_df = pd.DataFrame(
    {
        "Feature": features,
        "Importance": importance_result.importances_mean
    }
)

importance_df["Importance"] = (
    importance_df["Importance"]
    .clip(lower=0)
)

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
).reset_index(drop=True)

# Convert positive importance values to relative percentages
total_importance = importance_df["Importance"].sum()

if total_importance > 0:
    importance_df["Importance Percentage"] = (
        importance_df["Importance"]
        / total_importance
        * 100
    )
else:
    importance_df["Importance Percentage"] = 0


print("\nFEATURE IMPORTANCE")
print("---------------------------")

for _, row in importance_df.iterrows():

    print(
        f"{row['Feature']:<20} "
        f"{row['Importance Percentage']:.2f}%"
    )


# =========================================================
# SAVE MODEL
# =========================================================

model_path = os.path.join(
    MODELS_DIR,
    "dynamic_pricing_pipeline.pkl"
)

joblib.dump(
    pipeline,
    model_path
)


# =========================================================
# SAVE METRICS
# =========================================================

metrics = {
    "r2": float(r2),
    "rmse": float(rmse),
    "algorithm": best_model_name,
    "training_samples": len(X_train),
    "testing_samples": len(X_test)
}

metrics_path = os.path.join(
    MODELS_DIR,
    "model_metrics.pkl"
)

joblib.dump(
    metrics,
    metrics_path
)


# =========================================================
# SAVE FEATURE IMPORTANCE
# =========================================================

importance_path = os.path.join(
    MODELS_DIR,
    "feature_importance.pkl"
)

joblib.dump(
    importance_df,
    importance_path
)


# =========================================================
# COMPLETE
# =========================================================

print("\nFiles saved successfully:")

print(
    "1.",
    model_path
)

print(
    "2.",
    metrics_path
)

print(
    "3.",
    importance_path
)

print("\nFinal model training complete.")