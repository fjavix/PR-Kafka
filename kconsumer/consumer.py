#!/usr/bin/env python

import json
import logging
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer, KafkaProducer
from transformers import pipeline

# Inicializar el pipeline de análisis de sentimientos
sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

# Configuración del consumidor y productor de Kafka
consumer = KafkaConsumer('tweets',
                         group_id='tweet-group',
                         bootstrap_servers=['broker:29092'],
                         auto_offset_reset='earliest')

producer = KafkaProducer(bootstrap_servers='broker:29092')

# Definición de un nuevo topic para los datos procesados
output_topic = 'tweets_processed'

# Función para crear un nuevo topic
def create_topic():
    admin_client = KafkaAdminClient(bootstrap_servers="broker:29092")
    
    # Se crea el topic 'tweets_processed' con las configuraciones específicas
    new_topic = NewTopic(name=output_topic, num_partitions=1, replication_factor=1)

    # Control de errores
    try:
        admin_client.create_topics([new_topic])
        print(f"Topic '{output_topic}' creado exitosamente.")
    except Exception as e:
        print(f"No se pudo crear el topic '{output_topic}': {str(e)}")

# Se crea el nuevo topic antes de procesar los mensajes
create_topic()

# Suscribirse al topic 'tweets'
consumer.subscribe(['tweets'])

# Procesar mensajes
for message in consumer:
    # Decodificar el mensaje JSON
    tweet = json.loads(message.value.decode('utf8'))
    
    # Realizar el análisis de sentimientos
    sentiment_result = sentiment_pipeline(tweet['msg'])
    
    # Agregar los resultados del análisis al tweet
    tweet['sentiment'] = sentiment_result[0]['label']
    tweet['sentiment_score'] = sentiment_result[0]['score']
    
    # Convertir el tweet de nuevo a JSON
    processed_tweet = json.dumps(tweet)

    # Imprimir el tweet procesado
    print("Mensaje procesado:", processed_tweet)
    
    # Enviar el tweet procesado al nuevo topic en Kafka
    producer.send(output_topic, processed_tweet.encode('utf-8'))