import papermill as pm
import json

if __name__ == "__main__":
    # Load sensors configuration (relative to project root)
    sensors_config_path = "mlfs/airquality/sensors_config.json"
    with open(sensors_config_path, 'r') as f:
        sensors_config = json.load(f)

    print(f"Loaded configuration for {sensors_config['city']}")
    print(f"Found {len(sensors_config['sensors'])} sensors\n")


    for sensor in sensors_config["sensors"]:
        print(f"Processing sensor in street {sensor['street']}, {sensors_config['city']}...")

        # Used /dev/null to discard output notebook
        pm.execute_notebook(
            "notebooks/airquality/1_air_quality_feature_backfill.ipynb",
            "/dev/null",
            parameters=dict(
                csv_file=sensor['csv_file'],
                aqicn_url=sensor['url'],
                country=sensors_config['country'],
                city=sensors_config['city'],
                street=sensor['street'],
            )
        )

        print(f"✓ Completed {sensor['street']}\n")
