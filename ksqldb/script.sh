#!/bin/bash

# Función para verificar si ksqldb-server está disponible
wait_for_ksqldb() {
    echo "Esperando a que ksqlDB esté disponible..."
    until curl -sSf http://ksqldb-server:8088/healthcheck; do
        echo "ksqlDB todavía no está disponible. Reintentando la conexión..."
        sleep 5
    done
    echo "ksqlDB ya está disponible."
}

# Tiempo de espera
sleep 240

# Llamar a la función para verificar si ksqldb-server está disponible
wait_for_ksqldb

# Ejecutar el script principal
echo "Ejecutando el script principal..."

# Llamada al script principal
/kafka/ksqldb/script_ksql.sh