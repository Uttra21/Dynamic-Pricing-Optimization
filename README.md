# Dynamic Pricing Optimization Model

An end-to-end **Machine Learning Dynamic Pricing System** that recommends optimal product prices based on market conditions, competitor pricing, inventory, demand, weather, and seasonal factors.

The project compares multiple regression algorithms, performs feature engineering, automatically selects the best-performing model, and provides an interactive **Streamlit dashboard** for real-time pricing recommendations.

---

# Live Demo
https://dynamicpricing-optimization.streamlit.app/

---

# Project Overview

Dynamic pricing is widely used by companies like Amazon, Uber, airlines, and e-commerce platforms to maximize revenue by adjusting prices according to changing market conditions.

This project builds an intelligent pricing engine that predicts the optimal selling price using machine learning and presents recommendations through a modern interactive dashboard.

---

# Problem Statement

Businesses often rely on fixed pricing strategies that fail to account for:

- Competitor pricing
- Demand fluctuations
- Inventory levels
- Seasonal effects
- Weather conditions
- Customer purchasing behavior

As a result, businesses either lose customers due to overpriced products or lose profit by underpricing them.

This project solves this problem using machine learning.

---

# Solution

The application predicts an optimal product price by analyzing:

- Competitor Price
- Stock Level
- Quantity Purchased
- Discount
- Weather
- Holiday
- Weekend
- Demand Level
- Product Category
- Region

The best-performing regression model is automatically selected and used for prediction.

---

# Features

- Dynamic Price Prediction
- Multiple Machine Learning Models
- Automatic Best Model Selection
- GridSearchCV Hyperparameter Tuning
- Feature Engineering
- Feature Importance Analysis
- Weather-aware Pricing
- Inventory-aware Pricing
- Demand-aware Pricing
- Modern Interactive Streamlit Dashboard
- Saved ML Pipeline for Production Use

---

# Project Structure

```
Dynamic-Pricing-Optimization/
│
├── app/
│   └── app.py
│
├── data/
│   └── processed/
│       └── dynamic_pricing_dataset.csv
│
├── models/
│   ├── dynamic_pricing_pipeline.pkl
│   ├── model_metrics.pkl
│   └── feature_importance.pkl
│
├── notebooks/
│   ├── 01_Data_Understanding.ipynb
│   ├── 02_Feature_Engineering.ipynb
│   └── 03_Model_Building.ipynb
│
├── reports/
│
├── src/
│
├── train_model.py
├── requirements.txt
└── README.md
```

---

# Dataset Features

## Product Features

- Category
- Sub-Category
- Region
- Quantity

## Market Features

- Competitor Price
- Discount
- Stock Level
- Weather
- Holiday
- Weekend
- Demand Level
- Demand Score

## Target Variable

- Recommended Price

---

# Feature Engineering

The following interaction features were created to improve prediction quality:

- Competitor Price × Discount
- Quantity × Discount
- Stock Level × Quantity
- Competitor Price × Holiday
- Holiday × Weekend

These engineered features help the model capture more realistic pricing behaviour.

---

# Machine Learning Models

The project compares multiple regression algorithms.

| Model | Purpose |
|--------|----------|
| Linear Regression | Baseline model |
| Random Forest Regressor | Ensemble learning |
| Gradient Boosting Regressor | Boosted decision trees |

The best model is selected automatically based on RMSE.

---

# Final Model Performance

| Metric | Score |
|---------|-------|
| Best Model | Linear Regression |
| R² Score | **0.9964** |
| RMSE | **24.20** |

The model explains over **99% of the variance** in the pricing data.

---

# Top Pricing Factors

The trained model identified the following key pricing drivers:

| Feature | Importance |
|----------|------------|
| Competitor Price | **88.29%** |
| Competitor Price × Discount | **10.95%** |
| Demand Score | **0.69%** |
| Demand Level | **0.02%** |
| Competitor Price × Holiday | **0.01%** |

These insights help explain how the model makes pricing decisions.

---

# Dashboard Features

The Streamlit application provides:

### Pricing Simulator

Users can configure:

- Product Category
- Product Sub-category
- Region
- Quantity
- Discount
- Competitor Price
- Stock Level
- Holiday
- Weekend
- Weather
- Demand Level

### AI Recommendation

The application predicts:

- Recommended Price
- Price Difference
- Pricing Strategy
- Demand Status

### Model Analytics

The dashboard also displays:

- R² Score
- RMSE
- Best Model
- Feature Importance

---

# Tech Stack

### Programming

- Python

### Data Analysis

- Pandas
- NumPy

### Machine Learning

- Scikit-Learn
- GridSearchCV
- Linear Regression
- Random Forest
- Gradient Boosting

### Deployment

- Streamlit

### Model Storage

- Joblib

---

# Installation

Clone the repository

```bash
git clone https://github.com/Uttra21/Dynamic-Pricing-Optimization.git
```

Move into the project folder

```bash
cd Dynamic-Pricing-Optimization
```

Install dependencies

```bash
pip install -r requirements.txt
```

Train the model

```bash
python train_model.py
```

Launch the Streamlit application

```bash
streamlit run app/app.py
```

---

# Application Preview
<img width="815" height="436" alt="image" src="https://github.com/user-attachments/assets/6b41821a-7ee8-4def-9f2c-7e901becbd33" />
<img width="685" height="394" alt="image" src="https://github.com/user-attachments/assets/7229b084-9297-4054-8eca-76278f6eb316" />

---

# Machine Learning Workflow

```
Dataset
     │
     ▼
Data Cleaning
     │
     ▼
Feature Engineering
     │
     ▼
Train/Test Split
     │
     ▼
Preprocessing
     │
     ▼
Model Training
     │
     ▼
GridSearchCV
     │
     ▼
Model Evaluation
     │
     ▼
Feature Importance
     │
     ▼
Streamlit Dashboard
```

---

# Future Improvements

- Live Weather API Integration
- Real-time Competitor Price Scraping
- Time-Series Demand Forecasting
- Deep Learning Pricing Models
- Docker Deployment
- AWS Cloud Deployment

---

# Author

**Uttra Manhas**

B.Tech Computer Science & Engineering

Machine Learning • Data Analytics • Artificial Intelligence

GitHub: https://github.com/Uttra21

---

# If you found this project useful, consider giving it a star!
