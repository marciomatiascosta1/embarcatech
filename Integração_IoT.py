import paho.mqtt.client as mqtt
import json
import time

# Configuração MQTT
BROKER = "mqtt.broker.url"
PORT = 1883
TOPIC = "energyfly/telemetry"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso!")
    else:
        print(f"Erro ao conectar: {rc}")

def send_data(client, data):
    message = json.dumps(data)
    client.publish(TOPIC, message)
    print(f"Dados enviados: {message}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.connect(BROKER, PORT, 60)

# Simulação de envio de dados
client.loop_start()
try:
    while True:
        simulated_data = {
            "voltage": np.random.uniform(11.0, 14.0),
            "temperature": np.random.uniform(20.0, 50.0),
            "timestamp": time.time()
        }
        send_data(client, simulated_data)
        time.sleep(5)  # Envia a cada 5 segundos
except KeyboardInterrupt:
    print("Encerrando...")
    client.loop_stop()
    client.disconnect()
