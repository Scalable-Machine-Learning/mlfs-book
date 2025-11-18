# mlfs-book
O'Reilly book - Building Machine Learning Systems with a feature store: batch, real-time, and LLMs


<!-- ## ML System Examples -->


<!-- [Dashboards for Example ML Systems](https://featurestorebook.github.io/mlfs-book/) -->




<!-- # Run Air Quality Tutorial

See [tutorial instructions here](https://docs.google.com/document/d/1YXfM1_rpo1-jM-lYyb1HpbV9EJPN6i1u6h2rhdPduNE/edit?usp=sharing)
    # Create a conda or virtual environment for your project
    conda create -n book 
    conda activate book

    # Install 'uv' and 'invoke'
    pip install invoke dotenv

    # 'invoke install' installs python dependencies using uv and requirements.txt
    invoke install


## PyInvoke

    invoke aq-backfill
    invoke aq-features
    invoke aq-train
    invoke aq-inference
    invoke aq-clean



## Feldera


pip install feldera ipython-secrets
sudo apt-get install python3-secretstorage
sudo apt-get install gnome-keyring 

mkdir -p /tmp/c.app.hopsworks.ai
ln -s  /tmp/c.app.hopsworks.ai ~/hopsworks
docker run -p 8080:8080 \
  -v ~/hopsworks:/tmp/c.app.hopsworks.ai \
  --tty --rm -it ghcr.io/feldera/pipeline-manager:latest
 -->

## Contributors:
Ramin Darudi         - rdarudi@kth.se
Sebastian Schmülling - schmul@kth.se

# Air Quality Forecasting with Hopsworks Feature Store  
**Daily PM2.5 predictions using weather forecasts, lagged air-quality data, and an automated MLOps pipeline**

This project implements a complete end-to-end ML system that forecasts PM2.5 levels for three sensors in Lund. It implements:

- Historical backfill of PM2.5  
- Daily scraping & feature computation  
- Lag-1 / lag-2 / lag-3 PM2.5 features  
- Weather + air-quality Feature Groups  
- Feature Views for training  
- XGBoost model training + model selection  
- Registered model in Hopsworks Model Registry  
- Nightly batch inference via GitHub Actions  
- Dashboard published to GitHub Pages  

# Repository Structure

.gihub/workflows/air-quality-daily.yml → GitHub Actions daily inference workflow

/docs/air-quality/ → GitHub Pages dashboard (auto-published)

/notebooks/airquality/
1_air_quality_feature_backfill.ipynb
2_air_quality_feature_pipeline.ipynb
3_air_quality_training_pipeline.ipynb
4_air_quality_batch_inference.ipynb

Makefile 
requirements.txt
README.md

# Project Description

The system predicts upcoming PM2.5 concentrations by combining:

- Daily weather forecasts  
- Historical PM2.5 levels  
- 3 lag features (lag-1, lag-2, lag-3)  
- A 3-day rolling PM2.5 average   
- Feature Store–managed time-series data

## Sensors 

| Sensor   | Country | City | Street           |
|----------|---------|------|------------------|
| Sensor1  | Sweden  | Lund | bankgatan        |
| Sensor2  | Sweden  | Lund | linåkersvägen    |
| Sensor3  | Sweden  | Lund | trollebergsvägen |

Each sensor has:

- Latitude & longitude  
- AQICN API endpoint  
- Daily PM2.5 retrieval  
- Forecast generation  

## Data & Feature Store Architecture

The system uses **three Feature Groups** and **multiple Feature Views**.

---

## 1. **weather** Feature Group

Daily weather forecasts from Open-Meteo (12:00 UTC).

| Column                       | Type       |
|------------------------------|------------|
| date                         | timestamp  |
| temperature_2m_mean          | float      |
| precipitation_sum            | float      |
| wind_speed_10m_max           | float      |
| wind_direction_10m_dominant  | float      |
| city                         | string     |

---

Inserted every day via the daily feature pipeline.

## 2. **air_quality** Feature Group

Contains scraped PM2.5 values and engineered lagged features.

| Column         | Type      |
|----------------|-----------|
| date           | timestamp |
| pm25           | float     |
| country        | string    |
| street         | string    |
| url            | string    |
| city           | string    |
| pm25_3day_avg  | float     |
| pm25_lag_1day  | float     |
| pm25_lag_2day  | float     |
| pm25_lag_3day  | float     |

Two pipelines write to this FG:

### Backfill (Notebook 1)
- Historical PM2.5 loaded
- sorted by date
- rolling 3-day average + lags computed
- Inserted into FS

### Daily Feature Pipeline (Notebook 2)
- Scrape today's PM2.5 for each sensor
- Retrieve last 3 days from Feature Store
- Recompute lag-1, lag-2, lag-3 correctly
- Insert new row

---

## 3. **aq_predictions** Feature Group

Stores 7-day forecast outputs for each sensor.

| Column                      | Type     |
|-----------------------------|----------|
| country                     | string   |
| street                      | string   |
| city                        | string   |
| days_before_forecast_day    | bigint   |
| predicted_pm25              | float    |
| wind_direction_10m_dominant | float    |
| wind_speed_10m_max          | float    |
| precipitation_sum           | float    |
| temperature_2m_mean         | float    |

Populated by nightly batch inference.

---

# Feature Views

Feature Views combine weather + air-quality features needed by models.

We create four versions in the training pipeline:

- **FV No Lag**  
- **FV 1 Lag**  
- **FV 2 Lags**  
- **FV 3 Lags**  

Each view includes:
- All weather features  
- Encoded street  
- PM2.5 target  
- The corresponding lagged features  

Example:

air_quality_fv_3lags
→ weather features
→ pm25_lag_1day
→ pm25_lag_2day
→ pm25_lag_3day
→ pm25 as label

These FVs are used to train and compare multiple models.

---

# Model Training & Model Selection

Implemented in `3_air_quality_training_pipeline.ipynb`.

**Steps:**

1. Load training data from each Feature View  
2. Encode categorical features  
3. Train **four XGBoost regressors**  
4. Apply cross-validated hyperparameter tuning  
5. Compute CV MSE for each FV  
6. Automatically select **best performing model**  
7. Register the model + its Feature View to Hopsworks Model Registry

# Batch Inference

Implemented in `4_air_quality_batch_inference.ipynb`.

Every night GitHub Actions runs:

1. Load the registered best model  
2. Load its linked Feature View  
3. Fetch 7-day weather forecast  
4. Create inference dataset  
5. Feed historical + predicted lags (rolling forward)  
6. Predict PM2.5 for all sensors for all 7 days  
7. Insert all results into `aq_predictions` Feature Group  
8. Generate plots (hindcast + forecast)  
9. Export plots to `/docs/air-quality/assets/img/`  
10. Auto-publish dashboard on GitHub Pages 

---

# Automation (GitHub Actions)

`air-quality-daily.yml` runs at **23:00 UTC**.

Pipeline:

- Setup Python  
- Install dependencies  
- Run `make aq-feature` (daily feature updates)  
- Run `make aq-inference` (batch inference)  
- Commit generated plots + dashboard updates  
- GitHub Pages redeploys automatically  

---

# Dashboard (GitHub Pages)

Automatically updated nightly.

The dashboard shows:

- **7-day PM2.5 forecast** for each sensor  
- **1-day-ahead hindcast** (yesterday’s prediction vs actual)  
- One plot per sensor (Bankgatan, Linåkersvägen, Trollebergsvägen)

All plots are generated daily by the batch inference notebook and saved under  
`docs/air-quality/assets/img/`.

---

# Running the System Locally

```bash
export HOPSWORKS_API_KEY=API KEY

make aq-backfill       # Notebook 1 — historical data
make aq-feature        # Notebook 2 — daily features
make aq-train          # Notebook 3 — model training + registry
make aq-inference      # Notebook 4 — batch inference