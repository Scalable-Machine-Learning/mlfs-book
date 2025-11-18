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


# Air Quality Forecasting with Hopsworks Feature Store  
**Daily PM2.5 predictions using weather forecasts, lagged air-quality data, and an automated MLOps pipeline**

This project implements a complete end-to-end ML system that forecasts PM2.5 levels for three sensors in Lund. It implements:

- Backfill historical air quality data  
- Fetch and process daily weather forecasts  
- Compute lag-1, lag-2, lag-3 PM2.5 features  
- Build feature groups + feature views in Hopsworks  
- Train and register ML model on historical data   
- Run nightly feature update and batch inference  
- Publish visualisations to GitHub Pages  

## Repository Structure

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

## Project Description

The system predicts upcoming PM2.5 concentrations by combining:

- Daily weather forecasts  
- Historical PM2.5 levels  
- 3 lag features (lag-1, lag-2, lag-3)  
- A 3-day rolling PM2.5 average   
- Feature Store–managed time-series data

### Sensors Included


Sensor1: { "country": "Sweden", "city": "Lund", "street": "bankgatan" },
Sensor2: { "country": "Sweden", "city": "Lund", "street": "linåkersvägen" },
Sensor3: { "country": "Sweden", "city": "Lund", "street": "trollebergsvägen" }


## Hopsworks features

### weather

| Column                       | Type       |
|------------------------------|------------|
| date                         | timestamp  |
| temperature_2m_mean          | float      |
| precipitation_sum            | float      |
| wind_speed_10m_max           | float      |
| wind_direction_10m_dominant  | float      |
| city                         | string     |


### air_quality

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


### aq_predictions

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


