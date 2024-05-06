<?php
session_start();

// Define user ID's and passwords
$users = [
    'Tony' => 'Ktt573009',
    'jane456' => 'pass456'
];

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve form data
    $userId = $_POST['userID'];
    $enteredPassword = $_POST['password'];

    // Check if the user ID exists and password matches
    if (isset($users[$userId]) && $users[$userId] === $enteredPassword) {
        // Password authentication successful, set session
        $_SESSION['loggedin'] = true;

        // Fetch the token of the day
        $tokenFilePath = './text-files/token_of_the_day.txt';
        if (file_exists($tokenFilePath)) {
            $tokenOfTheDay = file_get_contents($tokenFilePath);
            // Set the token of the day in session
            $_SESSION['token_of_the_day'] = $tokenOfTheDay;
            // Set the token of the day as a cookie named "LogInToken"
            setcookie('LogInToken', $tokenOfTheDay, time() + 86400, '/'); // Cookie lasts for a day days
        } else {
            // Token file not found or empty
            $_SESSION['token_of_the_day'] = null;
        }

        // Redirect to dashboard
        header("Location: dashboard.php");
        exit();
    } else {
        // Password authentication failed, display error message
        $loginError = "Invalid username or password.";
    }    
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <?php if(isset($loginError)) echo "<p style='color:red;'>$loginError</p>"; ?>
    <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
        <label for="userID">User ID:</label><br>
        <input type="text" id="userID" name="userID"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
