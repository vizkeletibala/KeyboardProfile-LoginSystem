<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    var_dump($_POST);

    $keyup = array();
    $keydown = array();

    $username = $_POST["username"];
    $password = $_POST["password"];
    $keyup = json_decode($_POST["keyup"], true);
    $keydown = json_decode($_POST["keydown"], true);

    if ($keyup === null || $keydown === null) {
        echo "Error decoding JSON data";
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
    echo "Data has been written to file\n";

    if ($result === false) {
        error_log("Failed to write data to file: resources/data.json");
    }

    putenv('PYTHONPATH=C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe');
    $pythonPath = getenv('PYTHONPATH');
    echo "Python Path: $pythonPath";

    $command = 'C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe PythonFiles\RunModel.py "login"';
    try {
        $output = shell_exec($command);
        echo "<pre>$output</pre>";
    } catch (Exception $e) {
        echo "Error executing command: " . $e->getMessage();
    }

    $jsonFilePath = 'resources/LoginResult.json';

    $jsonData = file_get_contents($jsonFilePath);

    $dataArray = json_decode($jsonData, true);

    if ($dataArray === null) {
        echo "Error decoding JSON data";
    } else {
        foreach ($dataArray as $key => $value) {
            // Store the value in a variable
            $storedValue = $value;
        }

        echo "Stored Value: " . $storedValue;
    }

    if ($storedValue === true) {
        header("Location: statistics.html");
        exit;
    }
    else {
        header("Location: login.html");
        exit;
    }

} else {
    echo "Invalid request method";

}

?>
