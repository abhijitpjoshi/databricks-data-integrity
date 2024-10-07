import numpy as np
from pyspark.sql import SparkSession
import mlflow.keras

# Detect anomalies function
def detect_anomalies(df_batch, model, scaler):
    pd_batch = df_batch.toPandas()
    pd_batch_scaled = scaler.transform(pd_batch)
    reconstructions = model.predict(pd_batch_scaled)
    reconstruction_errors = np.mean(np.square(pd_batch_scaled - reconstructions), axis=1)
    threshold = 0.02
    anomalies = reconstruction_errors > threshold
    pd_batch['anomaly_flag'] = anomalies
    return spark.createDataFrame(pd_batch)
