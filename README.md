# Uber Eats Operational & Customer Intelligence System

## Project Overview

This project uses synthetic food-delivery data to explore customer behaviour, restaurant performance, customer review sentiment, delivery-time prediction, and hourly order demand forecasting.

## Objectives

1. Segment customers and restaurants using clustering.
2. Analyse customer review sentiment using NLP.
3. Predict delivery time using regression models.
4. Forecast hourly order demand using time-series methods.
5. Develop data-driven operational recommendations.

## Project Structure

- `data/raw/` — Generated synthetic CSV datasets
- `data/processed/` — Cleaned and transformed datasets
- `notebooks/` — Analysis and modelling notebooks
- `src/` — Python scripts for data generation and validation
- `models/` — Saved machine-learning models
- `reports/figures/` — Visualisations and report figures
- `docs/` — Data dictionary and project documentation
- `tests/` — Data and pipeline tests

## Data

Seven synthetic datasets are generated: customers, restaurants, drivers, orders, deliveries, reviews, and payments.

## Environment Setup

Create and activate a Python virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Generate and Validate Data

```bash
python src/data_generation.py
python src/validate_data.py
```

## Disclaimer

This is an educational project using synthetic data. It is not affiliated with or based on private Uber Eats customer or operational records.
