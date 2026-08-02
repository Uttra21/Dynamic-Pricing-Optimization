# Dynamic Pricing Optimization Engine

A machine learning-based pricing recommendation system that analyzes product, demand, inventory, competitor, and market-related factors to recommend an optimized product price.

This project demonstrates an end-to-end machine learning workflow including data exploration, feature engineering, model development, evaluation, model deployment, and an interactive Streamlit application.

---

#  Project Objective

Traditional fixed pricing strategies often fail to adapt to changing market conditions.

Product prices can be influenced by multiple factors such as:

- Customer demand
- Competitor pricing
- Inventory availability
- Product category
- Discounts
- Seasonal factors
- Regional differences

The objective of this project is to build a **Dynamic Pricing Optimization Engine** that uses machine learning to recommend suitable product prices based on market conditions and historical sales patterns.

---
## Technology Stack

### Programming Language
- Python

### Data Processing
- Pandas
- NumPy

### Data Visualization
- Matplotlib
- Seaborn

### Machine Learning
- Scikit-learn
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor

### Model Deployment
- Streamlit

### Model Serialization
- Joblib

---


#  Problem Statement

Businesses need pricing strategies that can adapt dynamically instead of relying on manually defined prices.

The challenge is to develop a machine learning system that can analyze product and market-related factors and provide data-driven pricing recommendations.

This project addresses this problem by creating a regression-based ML model that predicts recommended prices using engineered pricing features.

---

#  Proposed Solution

The solution consists of:

1. Data analysis and understanding
2. Feature engineering
3. Machine learning model training
4. Model comparison and evaluation
5. Model deployment using Streamlit

The final application allows users to enter product and market conditions and receive a recommended selling price.

---

#  Project Workflow

The project follows an end-to-end machine learning pipeline:


with:

```markdown
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
```


#  Dataset

The project uses the **Superstore Sales Dataset** containing historical sales transactions.

The dataset includes information such as:

- Order details
- Customer information
- Product categories
- Regional information
- Sales
- Quantity
- Discount
- Profit

Additional pricing-related features were engineered to simulate real-world dynamic pricing scenarios.

---

# Feature Engineering

The following features were created/enhanced:

### Product Features

- Category
- Sub-category

### Market Features

- Competitor Price
- Stock Level
- Discount

### Time-Based Features

- Holiday indicator
- Weekend indicator

### Demand Features

Demand-related features were created to represent customer demand conditions:

- Demand Score
- Demand Level

Demand levels were categorized into:

- Low
- Medium
- High

---

# Machine Learning Models

Multiple regression models were trained and compared:

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor

---

# Model Evaluation

Models were evaluated using:

### RMSE (Root Mean Square Error)

Measures prediction error. Lower values indicate better performance.

### R² Score

Measures how well the model explains variation in the target variable.

---

## Model Comparison

| Model | RMSE | R² Score |
|------|------|----------|
| Linear Regression | 41.10 | 0.9971 |
| Decision Tree Regressor | 195.91 | 0.9333 |
| Random Forest Regressor | 181.53 | 0.9427 |
| Gradient Boosting Regressor | 142.72 | 0.9646 |

Based on the evaluation results, **Linear Regression** was selected as the final pricing prediction model.

---

# Streamlit Application

The trained model is deployed using Streamlit.

The application allows users to provide:

- Product Category
- Sub Category
- Region
- Quantity
- Discount
- Competitor Price
- Stock Level
- Holiday Condition
- Weekend Condition

The application provides:

- Recommended Price
- Difference from Competitor Price
- Demand Level Analysis
- Pricing Recommendation Explanation
- Model Performance Metrics

---

#  Application Preview

<img width="446" height="405" alt="image" src="https://github.com/user-attachments/assets/20972d26-546a-42dc-9a86-c40245feae62" />
<img width="416" height="319" alt="image" src="https://github.com/user-attachments/assets/6c489cc2-4d00-4492-a96a-9a1fed83de38" />
<img width="341" height="331" alt="image" src="https://github.com/user-attachments/assets/124e3b4d-69ba-46c2-8e06-1a0df8c8f274" />

Example:

| Gradient Boosting | 142.72 | 0.9646 |

We'll also be careful to distinguish **engineered/simulated variables** from variables actually present in the original Superstore dataset. That's important if an interviewer asks where competitor price or stock data came from.
