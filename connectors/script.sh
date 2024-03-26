# Iniciar contenedor
/etc/confluent/docker/run &

# Esperar unos segundos
sleep 400

# Verificar si Connect está disponible
until nc -z localhost 8083; do
    echo "Connect aún no está disponible. Esperando..."
    sleep 10
done
echo "Connect está disponible. Cargando el conector..."

# Cargar la configuración del conector

(
  echo "POST /connectors HTTP/1.1"
  echo "Host: localhost:8083"
  echo "Content-Type: application/json"
  echo "Content-Length: $(wc -c < /connect-configs/mongo_sink_config.json)"
  echo
  cat /connect-configs/mongo_sink_config.json
) | nc localhost 8083