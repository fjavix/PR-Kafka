#!/usr/bin/env python

import json
import logging
import random
import csv
import time
import random

from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer

# Registrar errores
log = logging.getLogger(__name__)

# Función para crear un nuevo topic
def create_topic():
    admin_client = KafkaAdminClient(bootstrap_servers="broker:29092")    

    # Se crea el topic 'tweets' con las configuraciones específicas
    new_topic = NewTopic(name="tweets", num_partitions=1, replication_factor=1)

    # Control de errores
    try:
        admin_client.create_topics([new_topic])
        print("Topic 'tweets' creado exitosamente.")
    except Exception as e:
        print(f"No se pudo crear el topic 'tweets': {str(e)}")

# Se crea el topic antes de enviar los mensajes
create_topic()

# Se crea el Productor Kafka
producer = KafkaProducer(
    bootstrap_servers=['broker:29092'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

# Función para el caso de éxito en la producción del mensaje
def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

# Función para el caso de error
def on_send_error(ex):
    log.error('Ha ocurrido un error', exc_info=ex)

# Se lee el archivo csv y se producen los mensajes
with open('tweets.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        key = row[0]
        value = {'msg': row[3]}
        producer.send('tweets', key=key.encode('utf-8'), 
                      value=value).add_callback(on_send_success).add_errback(on_send_error)
    
        # Se definen diferentes intervalos de tiempo de espera entre mensajes (medido en segundos)
        intervalos = [0, 1, 2, 3]
        
        # Seleccionar aleatoriamente el intervalo de tiempo de espera
        tiempo_entre_mensajes = random.choice(intervalos)
        
        # Para los casos que el tiempo de espera es distinto a 0, esperar 1, 2 o 3 segundos
        if tiempo_entre_mensajes != 0:
            time.sleep(tiempo_entre_mensajes)
        

producer.flush()


