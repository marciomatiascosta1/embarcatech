import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

# Gerando dados simulados
def generate_data(samples=1000):
    voltage = np.random.uniform(11.0, 14.0, samples)
    temperature = np.random.uniform(20.0, 50.0, samples)
    energy_consumption = voltage * 0.5 + temperature * 0.3 + np.random.normal(0, 0.1, samples)
    X = np.array(list(zip(voltage, temperature)))
    y = np.array(energy_consumption)
    return X, y

# Construção do modelo
def build_model():
    model = Sequential([
        Dense(64, activation="relu", input_shape=(2,)),
        Dense(32, activation="relu"),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    return model

# Treinamento do modelo
X, y = generate_data()
model = build_model()
model.fit(X, y, epochs=20, batch_size=32, validation_split=0.2)

# Salvando o modelo
model.save("energyfly_model.h5")
print("Modelo treinado e salvo com sucesso!")
