<?php

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get the input values from the form
    $username = $_POST["username"];
    $email = $_POST["email"];
    $password = $_POST["password"];

    // Create an associative array with the input values
    $data = [
        "username" => $username,
        "email" => $email,
        "password" => $password
    ];

    // Convert the array to JSON
    $json = json_encode($data);

    // Write the JSON data to a file
    $result = file_put_contents("resources/data.json", $json);

    // Check if the file write was successful
    if ($result === false) {
        // Log the error
        error_log("Failed to write data to file: resources/data.json");
    }

    // Redirect to a success page or perform any other actions
    header("Location: register.html");
    exit;
}

?>

<!-- Your HTML form goes here -->
<!-- Make sure to set the form action to register.php and use the POST method -->
