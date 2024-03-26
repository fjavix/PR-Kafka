#!/bin/bash

# Endpoint de ksqldb
KSQLDB_ENDPOINT="http://ksqldb-server:8088"

# Función para verificar si el stream existe
check_stream_existence() {
    echo "Verificando la existencia del stream..."
    stream_response=$(curl -sSf -w "\n%{http_code}\n" -X POST -H "Content-Type: application/vnd.ksql.v1+json" --data '{"ksql":"DESCRIBE tweets_processed_stream;"}' $KSQLDB_ENDPOINT/ksql)
    stream_status=$(echo "$stream_response" | tail -n 1)

    if [[ "$stream_status" -eq 200 ]]; then
        return 0
    elif [[ "$stream_status" -eq 404 ]]; then
        return 1
    else
        echo "No se encuentra el stream. Respuesta del servidor: $stream_status"
        return 2
    fi
}

# Función para verificar si la tabla existe
check_table_existence() {
    echo "Verificando la existencia de la tabla..."
    table_response=$(curl -sSf -w "\n%{http_code}\n" -X POST -H "Content-Type: application/vnd.ksql.v1+json" --data '{"ksql":"DESCRIBE sentiment_counts;"}' $KSQLDB_ENDPOINT/ksql)
    table_status=$(echo "$table_response" | tail -n 1)

    if [[ "$table_status" -eq 200 ]]; then
        return 0
    elif [[ "$table_status" -eq 404 ]]; then
        return 1
    else
        echo "No se encuentra la tabla. Respuesta del servidor: $table_status"
        return 2
    fi
}

# Verificar si el stream existe
if check_stream_existence; then
    echo "El stream existe."
else
    echo "El stream no existe."

    # Crear stream
    echo "Creando stream..."
    create_stream_response=$(curl -sSf -w "\n%{http_code}\n" -X POST -H "Content-Type: application/vnd.ksql.v1+json" --data '{"ksql": "CREATE STREAM tweets_processed_stream (MSG VARCHAR, SENTIMENT VARCHAR, SENTIMENT_SCORE DOUBLE) WITH (KAFKA_TOPIC='\''tweets_processed'\'', VALUE_FORMAT='\''JSON'\'');"}' $KSQLDB_ENDPOINT/ksql)
    echo "$create_stream_response - Stream creado"
fi

# Verificar si la tabla existe
if check_table_existence; then
    echo "La tabla existe."
else
    echo "La tabla no existe."

    # Crear tabla
    echo "Creando tabla..."
    create_table_response=$(curl -sSf -w "\n%{http_code}\n" -X POST -H "Content-Type: application/vnd.ksql.v1+json" --data '{"ksql": "CREATE TABLE sentiment_counts AS SELECT SENTIMENT, COUNT(*) AS count FROM tweets_processed_stream GROUP BY SENTIMENT EMIT CHANGES;"}' $KSQLDB_ENDPOINT/ksql)
    echo "$create_table_response - Tabla creada"
fi

# Se mantiene el contenedor en ejecución
tail -f /dev/null

