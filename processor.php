<?php
session_start();
header("Access-Control-Allow-Origin: *");

// Overwrite fallback: Direct string comparison for local debugging
define('ADMIN_PASSWORD', 'MorphicSecureAdmin2026!');
$log_file = '/home/brian/mini_ids/morphic_events.json';

$input = json_decode(file_get_contents("php://input"), true);
$action = isset($_GET['action']) ? $_GET['action'] : '';

// 💥 ACTIVE DECOMPRESSION TRAP MECHANIC
// Triggered if an attacker tries to look for exploits or scan backend strings
if ($action === 'exploit' || isset($_GET['scan'])) {
    header("Content-Encoding: gzip");
    header("Content-Type: text/html");
    header("X-Morphic-Defense: Decompression-Trap-Engaged");
    
    // Log the event before neutralizing the attacker's terminal socket
    $logs = file_exists($log_file) ? json_decode(file_get_contents($log_file), true) : [];
    $logs[] = [
        "timestamp" => date("Y-m-d H:i:s"),
        "policy" => "DECOMPRESSION TRAP",
        "source_ip" => $_SERVER['REMOTE_ADDR'],
        "details" => "Host triggered directory scanning. Delivered recursive GZIP memory exhaustion payload."
    ];
    file_put_contents($log_file, json_encode($logs, JSON_PRETTY_PRINT));

    // Deliver an intensive stream of compressed zero-data to flood their memory buffer
    // 1000 iterations creates an overwhelming memory allocation expansion on their tool
    $garbage_chunk = str_repeat("0", 65536); // 64KB block of raw zeros
    for ($i = 0; $i < 1000; $i++) {
        echo gzencode($garbage_chunk, 9);
        ob_flush();
        flush();
    }
    exit;
}

// Standard Authentication Endpoint Logic
if ($action === 'login') {
    header("Content-Type: application/json");
    $password = isset($input['password']) ? $input['password'] : '';
    if ($password === ADMIN_PASSWORD) {
        $_SESSION['authenticated'] = true;
        $_SESSION['token_expiry'] = time() + 3600;
        echo json_encode(["status" => "success", "message" => "Authentication successful."]);
        exit;
    }
    header("HTTP/1.1 401 Unauthorized");
    echo json_encode(["status" => "error", "message" => "Invalid admin credentials."]);
    exit;
}

// Session Validation Gate
if (!isset($_SESSION['authenticated']) || $_SESSION['authenticated'] !== true || time() > $_SESSION['token_expiry']) {
    session_destroy();
    header("HTTP/1.1 403 Forbidden");
    header("Content-Type: application/json");
    echo json_encode(["status" => "error", "message" => "Access denied."]);
    exit;
}

// Protected Actions
header("Content-Type: application/json");
if ($action === 'get_logs') {
    echo file_exists($log_file) ? file_get_contents($log_file) : json_encode([]);
} elseif ($action === 'purge_logs') {
    if (file_exists($log_file)) {
        file_put_contents($log_file, json_encode([]));
        echo json_encode(["status" => "success", "message" => "Logs cleared."]);
    }
} else {
    echo json_encode(["status" => "authenticated", "engine" => "Morphic-IPS Core Active Engine"]);
}
?>
