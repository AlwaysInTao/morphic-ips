<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $attacker_ip = $_SERVER['REMOTE_ADDR'];
    $payload = json_decode(file_get_contents('php://input'), true);
    $hardware_hash = $payload['canvas_hash'] ?? 'unknown_hardware';

    $incident_card = [
        'timestamp' => date('Y-m-d H:i:s'),
        'attacker_ip' => $attacker_ip,
        'hardware_fingerprint' => $hardware_hash,
        'anonymity_tool_active' => 'CHECKING...'
    ];

    // Write natively directly to our central project workspace folder
    file_put_contents(__DIR__ . '/ids_trigger.json', json_encode($incident_card));
    chmod(__DIR__ . '/ids_trigger.json', 0666);

    header('Content-Type: application/json');
    echo json_encode(['status' => 'acknowledged']);
}
?>
