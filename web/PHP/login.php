<?php
session_start();

// Check if the user is already logged in
if (isset($_SESSION['username'])) {
    header("Location: admin.php");
    exit();
}

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Predefined admin credentials
    $admin_username = 'admin';
    $admin_password = 'admin123';

    $username = $_POST['username'];
    $password = $_POST['password'];

    // Validate credentials
    if ($username === $admin_username && $password === $admin_password) {
        $_SESSION['username'] = $username;
        header("Location: admin.php");
        exit();
    } else {
        $error = "Invalid username or password";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Red Hawks MC</title>
    <link rel="stylesheet" type="text/css" href="./CSS/main_body_colors.css">
    <link rel="stylesheet" type="text/css" href="./CSS/header_colors.css">
    <style>
        body {
            font-family: "Timesi.ttf", Times, serif;
        }
    </style>

</head>
<body>

    <header>
        <div class="header-left">
            <img src="./Images/emblem_512.png" alt="Logo" class="logo">
            <h1>Red Hawks Mercenary Company</h1>
           </div>
        <nav>
            <a href="home.html">Home</a>
            <a href="Login.html">Dashboard</a>
            <a href="">Coming Soon</a>
            <a href="aboutus.html">About</a>
            <a href="admiral_rules.html">Admiral Rules</a>
            <a href="staffmembers.html">Staff Members</a>
        </nav>
    </header>
