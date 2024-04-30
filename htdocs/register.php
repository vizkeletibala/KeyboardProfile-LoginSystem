<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    var_dump($_POST);

    $keyup = array();
    $keydown = array();

    $username = $_POST["username"];
    $email = $_POST["email"];
    $password = $_POST["password"];
    $keyup = json_decode($_POST["keyup"], true);
    $keydown = json_decode($_POST["keydown"], true);

    if ($keyup === null || $keydown === null) {
        echo "Error decoding JSON data";
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
    echo "Data has been written to file\n";

    if ($result === false) {
        error_log("Failed to write data to file: resources/data.json");
    }

    putenv('PYTHONPATH=C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe');
    $pythonPath = getenv('PYTHONPATH');
    echo "Python Path: $pythonPath";

    $command = 'C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe PythonFiles\RunModel.py "register"';
    try {
        $output = shell_exec($command);
        echo "<pre>$output</pre>";
    } catch (Exception $e) {
        echo "Error executing command: " . $e->getMessage();
    }
}

?>
