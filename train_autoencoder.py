import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from pyspark.sql import SparkSession
from sklearn.preprocessing import MinMaxScaler
import mlflow
import mlflow.keras

# Autoencoder model definition
def create_autoencoder(input_dim):
    model = Sequential([
        Dense(64, activation='relu', input_shape=(input_dim,)),
        Dense(32, activation='relu'),
        Dense(64, activation='relu'),
        Dense(input_dim, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def train_autoencoder(df_batch):
    pd_batch = df_batch.toPandas()
    scaler = MinMaxScaler()
    pd_batch_scaled = scaler.fit_transform(pd_batch)
    
    autoencoder = create_autoencoder(input_dim=pd_batch_scaled.shape[1])
    with mlflow.start_run():
        autoencoder.fit(pd_batch_scaled, pd_batch_scaled, epochs=10, batch_size=32, verbose=0)
        mlflow.keras.log_model(autoencoder, "autoencoder_model")
        return autoencoder, scaler
