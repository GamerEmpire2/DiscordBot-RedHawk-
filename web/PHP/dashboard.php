<?php
session_start();

// Check if the user is logged in
if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true) {
    header("Location: login.php"); // Redirect to login page if not logged in
    exit();
}

// Check if "LogInToken" cookie is set
if (!isset($_COOKIE['LogInToken'])) {
    // Redirect to login page if "LogInToken" cookie is not set
    header("Location: login.php");
    exit();
}

// TODO: Instead of selecting a token of the day, you should generate a new token whenever a user logs in and save the token in the
//       session and in the database along with the user ID and expiration. Then, when the user logs in, you should compare the token in the session
//       with the token in the database to authenticate the user and token Expiration.

// Get the token of the day from session
$tokenOfTheDay = $_SESSION['token_of_the_day'];

// Get the "LogInToken" cookie value
$loginToken = $_COOKIE['LogInToken'];

// Compare the tokens
if ($loginToken !== $tokenOfTheDay) {
    // Redirect to login page if tokens do not match
    header("Location: login.php");
    exit();
}

// If tokens match, user is authenticated and can access the dashboard
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
</head>
<body>
    <h2>Welcome to the Dashboard</h2>
    <p>You are logged in.</p>
    <a href="logout.php">Logout</a>
</body>
</html>
