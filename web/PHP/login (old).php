<?php
session_start(); // Start a new or resume an existing session
// Include Composer's autoloader
require __DIR__ . '/vendor/autoload.php';
// Include the database.php file
require __DIR__ . '/database.php';

// Check if the user is already logged in
if (isset($_COOKIE['token'])) {
    // Get the token from the cookie
    $token = $_COOKIE['token'];

    // Validate the token
    $userId = validate_token($token);

    if ($userId) {
        // Token is valid, log the user in
        $_SESSION['loggedin'] = true;
        $_SESSION['userId'] = $userId; // Store the user ID in the session
    
        // Regenerate session ID
        session_regenerate_id(true);

        // Redirect to dashboard
        header("Location: dashboard.php");
        exit();
    }
}

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve form data
    $username = $_POST['username'];
    $enteredPassword = $_POST['password'];

    // Get the hashed password and salt for the user
    list($hashedPassword, $salt) = get_user_credentials($username);

    // Hash the entered password with the salt
    $hashedEnteredPassword = hash('sha256', $enteredPassword . $salt);

    // Check if the user exists and password matches
    if ($hashedPassword && $hashedEnteredPassword === $hashedPassword) {
        // Password authentication successful, set session
        $_SESSION['loggedin'] = true;
        // Regenerate session ID
        session_regenerate_id(true);
        // Create a token for the user
        $token = create_token($username);
        // Set the token as a secure HTTP-only cookie
        setcookie('token', $token, [
            'expires' => time() + 60 * 60 * 24 * 7, // 7 days
            'path' => '/',
            'secure' => true, // Set to false if not using HTTPS
            'httponly' => true,
            'samesite' => 'Strict',
        ]);
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
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
