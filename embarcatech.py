# Importação de bibliotecas
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.optimizers import Adam

# Simulação de dados históricos para treinamento
np.random.seed(42)  # Define a semente para garantir reprodutibilidade
data = np.random.rand(1000, 3)  # 1000 amostras com 3 variáveis: tensão, corrente e temperatura
labels = np.random.rand(1000, 1)  # Rótulos simulados para consumo futuro

# Divisão dos dados em treino e teste
train_data = data[:800]       # 80% dos dados para treinamento
train_labels = labels[:800]   # Rótulos correspondentes para treinamento
test_data = data[800:]        # 20% dos dados para teste
test_labels = labels[800:]    # Rótulos correspondentes para teste

# Definição do modelo de IA
model = Sequential([
    LSTM(64, activation='relu', input_shape=(3, 1), return_sequences=True),  # Primeira camada LSTM
    LSTM(32, activation='relu'),  # Segunda camada LSTM
    Dense(16, activation='relu'),  # Camada totalmente conectada com 16 neurônios
    Dense(1)  # Saída única para previsão do consumo
])

# Compilação do modelo
model.compile(
    optimizer=Adam(learning_rate=0.001),  # Otimizador Adam com taxa de aprendizado de 0,001
    loss='mse',                           # Função de perda: erro quadrático médio
    metrics=['mae']                       # Métrica de avaliação: erro absoluto médio
)

# Redimensionamento dos dados para formato esperado pelo LSTM
train_data_reshaped = train_data.reshape((train_data.shape[0], train_data.shape[1], 1))
test_data_reshaped = test_data.reshape((test_data.shape[0], test_data.shape[1], 1))

# Treinamento do modelo
history = model.fit(
    train_data_reshaped, train_labels,  # Dados de treino
    epochs=50,                          # Número de épocas
    batch_size=32,                      # Tamanho do lote
    validation_data=(test_data_reshaped, test_labels)  # Dados de validação
)

# Função para realizar previsões em tempo real
def predict_energy(voltage, current, temperature):
    """
    Recebe tensão, corrente e temperatura como entrada
    e realiza a previsão de consumo de energia.
    """
    input_data = np.array([[voltage, current, temperature]])
    input_data_reshaped = input_data.reshape((input_data.shape[0], input_data.shape[1], 1))
    predicted_energy = model.predict(input_data_reshaped)
    return predicted_energy[0][0]

# Salvando o modelo treinado em um arquivo
model.save('energyfly_ai_model.h5')

# Carregando o modelo treinado para uso posterior
loaded_model = tf.keras.models.load_model('energyfly_ai_model.h5')

