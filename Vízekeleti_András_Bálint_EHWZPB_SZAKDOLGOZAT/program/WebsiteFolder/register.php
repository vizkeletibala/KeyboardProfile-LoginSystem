<?php

header_remove('ETag');
header_remove('Pragma');
header_remove('Cache-Control');
header_remove('Last-Modified');
header_remove('Expires');

// set header
header('Expires: Sun, 01 Jan 2014 00:00:00 GMT');
header('Cache-Control: no-store, no-cache, must-revalidate');
header('Cache-Control: post-check=0, pre-check=0', FALSE);
header('Pragma: no-cache');

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // remove header
    

    ini_set('display_errors', 0);
    ini_set('log_errors', 1);
    ini_set('error_log', __DIR__ . '/error_log.txt');
    error_reporting(E_ALL);

    //var_dump($_POST);

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
        error_log("Error decoding JSON data");
        exit;
    }

    $data = [
        "username" => $username,
        "email" => $email,
        "password" => $password,
        "keyup" => $keyup,
        "keydown" => $keydown
    ];
    
    $json = json_encode($data);

    $result = file_put_contents("resources/data.json", $json);
    //echo "Data has been written to file\n";

    if ($result === false) {
        error_log("Failed to write data to file: resources/data.json");
    }

    /*
    putenv('PYTHONPATH=C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe');
    $pythonPath = getenv('PYTHONPATH');
    //echo "Python Path: $pythonPath";

    $command = 'C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe PythonFiles\RunModel.py "register"';
    */

    $pythonPath = '/usr/bin/python3';
    $scriptPath = '/var/www/html/szakdoga/PythonFiles/RunModel.py';
    $command = $pythonPath . ' ' . $scriptPath . ' "register"';

    try {
        $output = shell_exec($command);
        error_log("Shell output: " . $output);
    } catch (Exception $e) {
        error_log("Error executing command: " . $e->getMessage());
    }

    header("Location: register.html");
}

?>
