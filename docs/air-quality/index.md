<!-- # Air Quality Dashboard

![Hopsworks Logo](../titanic/assets/img/logo.png)

{% include air-quality.html %}

![Forecast](./assets/img/pm25_forecast.png)


There is also a Python program to interact with the air quality ML system using language (text, voice),
powered by a [function-calling LLM](https://www.hopsworks.ai/dictionary/function-calling-with-llms).

# Model Performance Monitoring

1-Day Hindcast: Predictions vs Outcomes

![Hindcast](./assets/img/pm25_hindcast_1day.png) -->

---
layout: default
title: Air Quality Forecast – Lund
---

# Air Quality Forecast Dashboard – Lund

This dashboard shows **PM2.5 predictions for the next 7** and a **1-day-ahead hindcast** (prediction vs actual)  
for three sensors in Lund. The data is stored in Hopsworks Feature Store, the model is trained in notebook `3_air_quality_training_pipeline.ipynb`, and the plots are generated daily by `4_air_quality_batch_inference.ipynb` and a GitHub Actions workflow.

---

## Sensors in Lund

We predict air quality for these sensors:

- **Bankgatan**
- **Linåkersvägen**
- **Trollebergsvägen**

Each section below shows the forecast and 1-day-ahead hindcast for that sensor.

---

## Bankgatan

### 7 Day Forecast

![PM2.5 Forecast – Lund Bankgatan](./assets/img/lund_bankgatan_pm25_forecast.png)

### 1-Day-Ahead Hindcast (Prediction vs Actual)

![PM2.5 Hindcast 1 Day – Lund Bankgatan](./assets/img/img/lund_bankgatan_pm25_hindcast_1day.png)

---

## Linåkersvägen

### 7 Day Forecast

![PM2.5 Forecast – Lund Linåkersvägen](./assets/img/lund_linåkersvägen_pm25_forecast.png)

### 1-Day-Ahead Hindcast (Prediction vs Actual)

![PM2.5 Hindcast 1 Day – Lund Linåkersvägen](./assets/img/lund_linåkersvägen_pm25_hindcast_1day.png)

---

## Trollebergsvägen

### 7 Day Forecast

![PM2.5 Forecast – Lund Trollebergsvägen](./assets/img/lund_trollebergsvägen_pm25_forecast.png)

### 1-Day-Ahead Hindcast (Prediction vs Actual)

![PM2.5 Hindcast 1 Day – Lund Trollebergsvägen](./assets/img/lund_trollebergsvägen_pm25_hindcast_1day.png)


---

## Implementation Notes

- **Feature Store:** Weather and air-quality time series are stored in Hopsworks Feature Store.
- **Model:** The PM2.5 prediction model is trained using a feature view that includes:
  - Weather features (temperature, humidity, wind, etc.).
  - Air-quality history features.
  - **Lag features:** PM2.5 from the previous 1, 2, and 3 days.
- **Pipelines:**
  - `1_air_quality_feature_backfill.ipynb` and `2_air_quality_feature_pipeline.ipynb` populate and update the feature groups.
  - `3_air_quality_training_pipeline.ipynb` trains and registers the model.
  - `4_air_quality_batch_inference.ipynb` runs daily, reads future weather, predicts PM2.5 for the next 7–10 days for **all three Lund sensors**, writes these PNGs to `docs/air-quality/assets/img`, and commits them via GitHub Actions.
- **Monitoring (hindcast):** A monitoring feature group stores daily predictions; these are joined with measured PM2.5 to produce the 1-day-ahead hindcast plots above.

