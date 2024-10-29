<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // Disable cache
    header_remove('ETag');
    header_remove('Pragma');
    header_remove('Cache-Control');
    header_remove('Last-Modified');
    header_remove('Expires');

    // set header
    header('Expires: Thu, 1 Jan 1970 00:00:00 GMT');
    header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
    header('Cache-Control: post-check=0, pre-check=0',false);
    header('Pragma: no-cache');

    header('Content-Type: application/json');

    // Suppress error reporting and log errors to a file
    ini_set('display_errors', 0);
    ini_set('log_errors', 1);
    ini_set('error_log', __DIR__ . '/error_log.txt');
    error_reporting(E_ALL);


    $data = json_decode(file_get_contents('php://input'), true);
    $keyup = array();
    $keydown = array();

    $username = $data["Username"];
    $password = $data["Password"];
    error_log("Username: " . $username . ", Password: " . $password);
    $temp = html_entity_decode(stripslashes($data["keyup"]));
    $keyup = json_decode($temp, true);
    $temp = html_entity_decode(stripslashes($data["keydown"]));
    $keydown = json_decode($temp, true);

    if ($keyup === null || $keydown === null) {
        error_log("Error decoding JSON data: keyup or keydown is null");
        echo json_encode(['success' => false, 'message' => 'Error decoding JSON data']);
        exit;
    }

    $data = [
        "username" => $username,
        "password" => $password,
        "keyup" => $keyup,
        "keydown" => $keydown
    ];

    $json = json_encode($data);
    $result = file_put_contents("resources/data.json", $json);

    if ($result === false) {
        error_log("Failed to write data to file: resources/data.json");
        echo json_encode(['success' => false, 'message' => 'Failed to write data to file']);
        exit;
    }

    $pythonPath = '/usr/bin/python3';
    $scriptPath = '/var/www/html/szakdoga/PythonFiles/RunModel.py';
    $command = $pythonPath . ' ' . $scriptPath . ' "login"';

    try {
        $output = shell_exec($command);
        error_log("Shell output: " . $output);
        if ($output === null) {
            throw new Exception("Shell execution returned null");
        }
    } catch (Exception $e) {
        error_log("Error executing command: " . $e->getMessage());
        echo json_encode(['success' => false, 'message' => 'Error executing command']);
        exit;
    }

    $jsonFilePath = 'resources/LoginResult.json';
    $jsonData = file_get_contents($jsonFilePath);

    if ($jsonData === false) {
        error_log("Failed to read JSON data from file: resources/LoginResult.json");
        echo json_encode(['success' => false, 'message' => 'Failed to read JSON data from file']);
        exit;
    }

    $dataArray = json_decode($jsonData, true);

    if ($dataArray === null) {
        error_log("Error decoding JSON data from file");
        echo json_encode(['success' => false, 'message' => 'Error decoding JSON data']);
        exit;
    }
    
    $storedValue = $dataArray['login result'] ?? false;

    if ($storedValue === true) {
        echo json_encode(['success' => true, 'message' => 'Login successful.']);
    } else {
        echo json_encode(['success' => false, 'message' => 'Login unsuccessful.']);
    }

} else {
    echo json_encode(['success' => false, 'message' => 'Invalid request method']);
}
?>
