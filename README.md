#  Dynamic Pricing Optimization Engine

A machine learning-based pricing recommendation system that analyzes product, demand, inventory, competitor, and market-related factors to recommend an appropriate product price.

The project demonstrates an end-to-end machine learning workflow, including data exploration, feature engineering, model comparison, model evaluation, and deployment through an interactive Streamlit application.

##  Project Objective

Traditional fixed-pricing strategies do not adapt effectively to changing market conditions. Product demand, competitor pricing, inventory levels, discounts, and temporal factors can all influence the price at which a product should be offered.

The objective of this project is to build a **Dynamic Pricing Optimization Engine** that uses historical sales data and engineered market features to generate data-driven price recommendations.

The system considers factors such as:

- Product category and sub-category
- Product quantity
- Regional market information
- Discount
- Competitor price
- Stock level
- Holiday conditions
- Weekend conditions
- Demand-related features

The final trained model is integrated into a **Streamlit web application**, allowing users to enter market conditions and receive an instant recommended price.
## 💡 Problem Statement

Businesses often use fixed or manually determined pricing strategies that may not respond effectively to changes in demand and market conditions.

Several factors can influence an appropriate product price, including competitor pricing, available stock, discounts, product demand, regional differences, and time-related conditions such as weekends and holidays.

The challenge is to develop a data-driven system that can analyze these factors and recommend a suitable price dynamically instead of relying entirely on static pricing rules.

## 🚀 Proposed Solution

This project implements a machine learning-based pricing recommendation system.

Historical Superstore sales data is processed and enhanced with additional pricing-related features. Multiple regression algorithms are then trained and evaluated to determine which model performs best for the pricing prediction task.

The resulting model is integrated into an interactive Streamlit application where users can provide product and market information and receive a recommended price.

### Application Inputs

The pricing engine accepts:

- Category
- Sub-Category
- Region
- Quantity
- Discount
- Competitor Price
- Stock Level
- Holiday indicator
- Weekend indicator

### Application Output

The system provides:

- Recommended Price
- Competitor Price comparison
- Price Difference
- Estimated Demand Level
- Pricing recommendation explanation
## 🔄 Project Workflow

The project follows an end-to-end machine learning pipeline:

```text
Raw Superstore Dataset
        ↓
Data Understanding & Exploration
        ↓
Data Cleaning
        ↓
Feature Engineering
        ↓
Pricing & Demand Feature Creation
        ↓
Categorical Encoding
        ↓
Train-Test Split
        ↓
Multiple Regression Models
        ↓
Model Evaluation
        ↓
Best Model Selection
        ↓
Model Serialization using Joblib
        ↓
Streamlit Pricing Application


One small Markdown issue: because the workflow itself contains a code block, make sure the final README has the opening ` ```text ` and closing ` ``` ` around the workflow.

### What we'll add next

Once you've pasted and saved this, the next section is particularly important:

**📊 Dataset & Feature Engineering**

We'll document your original `Superstore.csv` and explain the additional variables such as **Competitor Price, Stock Level, Holiday, Weekend, Demand Score, Demand Level, and Recommended Price**.

After that we'll document your four models and the actual results you obtained:

| Model | RMSE | R² |
|---|---:|---:|
| Linear Regression | **41.10** | **0.9971** |
| Decision Tree | 195.91 | 0.9333 |
| Random Forest | 181.53 | 0.9427 |
| Gradient Boosting | 142.72 | 0.9646 |

We'll also be careful to distinguish **engineered/simulated variables** from variables actually present in the original Superstore dataset. That's important if an interviewer asks where competitor price or stock data came from.
