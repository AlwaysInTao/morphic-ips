<?php
session_start();
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");

// Overwrite fallback: Direct string comparison for local debugging
define('ADMIN_PASSWORD', 'MorphicSecureAdmin2026!');
$log_file = '/home/brian/mini_ids/morphic_events.json';

$input = json_decode(file_get_contents("php://input"), true);
$action = isset($_GET['action']) ? $_GET['action'] : '';

// Authentication Endpoint Logic
if ($action === 'login') {
    $password = isset($input['password']) ? $input['password'] : '';
    // Directly match string parameters 
    if ($password === ADMIN_PASSWORD) {
        $_SESSION['authenticated'] = true;
        $_SESSION['token_expiry'] = time() + 3600;
        echo json_encode(["status" => "success", "message" => "Authentication successful."]);
        exit;
    }
    header("HTTP/1.1 401 Unauthorized");
    echo json_encode(["status" => "error", "message" => "Invalid admin password credentials."]);
    exit;
}

// Session Validation Gate
if (!isset($_SESSION['authenticated']) || $_SESSION['authenticated'] !== true || time() > $_SESSION['token_expiry']) {
    session_destroy();
    header("HTTP/1.1 403 Forbidden");
    echo json_encode(["status" => "error", "message" => "Access denied. Valid login session required."]);
    exit;
}

// Protected Actions
if ($action === 'get_logs') {
    if (file_exists($log_file)) {
        echo file_get_contents($log_file);
    } else {
        echo json_encode([]);
    }
} elseif ($action === 'purge_logs') {
    if (file_exists($log_file)) {
        file_put_contents($log_file, json_encode([]));
        echo json_encode(["status" => "success", "message" => "Telemetry log stream cleared cleanly."]);
    }
} else {
    echo json_encode(["status" => "authenticated", "engine" => "Morphic-IPS Core Active Engine"]);
}
?>
