<?php

// Definición de datos de MongoDB
$mongoHost = 'mongodb';
$mongoPort = 27017;
$dbName = 'my_tweets';
$username = 'admin';
$password = 'admin';

// Función para ejecutar una consulta a MongoDB y devolver el cursor para iterar sobre los resultados
function executeQuery($mongoClient, $collection, $filter = []) {
    $query = new MongoDB\Driver\Query($filter);
    return $mongoClient->executeQuery($collection, $query);
}

try {
    // Conexión a MongoDB
    $mongoClient = new MongoDB\Driver\Manager("mongodb://{$username}:{$password}@{$mongoHost}:{$mongoPort}");
    
    // Consultar resultados de la colección de la bbdd
    $collection = $dbName . '.kafka_tweets';

    // Contadores por sentimientos
    $counters = ['POS' => 0, 'NEU' => 0, 'NEG' => 0];
    $totalMessages = 0;
    $totalSentimentScore = 0;

    // Consulta para obtener todos los documentos de la colección
    $query = new MongoDB\Driver\Query([]);
    $cursor = executeQuery($mongoClient, $collection, $query);

    /// Conteo de sentimientos
    foreach ($cursor as $document) {
        $sentiment = $document->sentiment;
        $totalMessages++;
        $totalSentimentScore += ($sentiment === 'POS') ? 1 : (($sentiment === 'NEU') ? 0 : -1);
        $counters[$sentiment]++;
    }

    // Calcular el sentimiento promedio
    $averageSentiment = $totalSentimentScore / $totalMessages;

    // Calcular porcentajes para cada tipo de opinión
    $percentagePOS = ($counters['POS'] / $totalMessages) * 100;
    $percentageNEU = ($counters['NEU'] / $totalMessages) * 100;
    $percentageNEG = ($counters['NEG'] / $totalMessages) * 100;

    // Mostrar el resultado de contar tweets por sentimiento
    echo "<hr>";  
    echo "<h2>Número de tweets por sentimiento</h2>";
    foreach ($counters as $sentiment => $count) {
        $icon = ($sentiment === 'POS') ? '😊' : (($sentiment === 'NEU') ? '😐' : '😞');
        echo "<p>Número de mensajes $icon $sentiment: $count</p>";
    }

    // Resultados agregados
    echo "<hr>";  
    echo "<h2>Estadísticas</h2>";

    // Mostrar el total de mensajes almacenados
    echo "<p>Total de mensajes almacenados: $totalMessages</p>";

    // Mostrar el sentimiento promedio
    echo "<p>Sentimiento promedio: $averageSentiment</p>";

    // Mostrar los porcentajes para cada tipo de opinión
    echo "<p>Porcentaje de mensajes positivos: " . number_format($percentagePOS, 2) . "%</p>";
    echo "<p>Porcentaje de mensajes neutrales: " . number_format($percentageNEU, 2) . "%</p>";
    echo "<p>Porcentaje de mensajes negativos: " . number_format($percentageNEG, 2) . "%</p>";

    // Mostrar desplegable con los diferentes sentimientos
    echo "<hr>";   
    echo "<h2>Revisión de tweets para cada sentimiento</h2>";
    echo "<form method='GET'>";
    echo "<select name='sentiment'>";
    foreach ($counters as $sentiment => $count) {
        $icon = ($sentiment === 'POS') ? '😊' : (($sentiment === 'NEU') ? '😐' : '😞');
        echo "<option value='$sentiment'>$icon $sentiment</option>";
    }
    echo "</select>";
    echo "<input type='submit' value='Mostrar mensajes'>";
    echo "</form>";

    // Mensajes por sentimiento
    if (isset($_GET['sentiment'])) {
        $selectedSentiment = $_GET['sentiment'];
        echo "<h4>Tweets categorizados como $selectedSentiment</h4>";
        $filter = ['sentiment' => $selectedSentiment];
        $cursor = executeQuery($mongoClient, $collection, $filter);
        foreach ($cursor as $document) {
            echo "<p>" . $document->msg . "</p>";
        }
    }
    
// Control de errores
} catch (MongoDB\Driver\Exception\Exception $e) {
    echo "Fallo al conectar a MongoDB: " . $e->getMessage();
} catch (Exception $e) {
    echo "An error occurred: " . $e->getMessage();
}

?>
