<?php
// Include Composer's autoloader
require __DIR__ . '/../vendor/autoload.php';
// Load environment variables from .env file
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . '/../..');
$dotenv->load();
$db_path = $_ENV['PROJECT_ROOT'] . '/db/database.db';
$pdo = new PDO('sqlite:' . $db_path);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

function get_user_credentials($username) {
    global $pdo;

    $stmt = $pdo->prepare("SELECT hashed_password, salt FROM users WHERE username = ?");
    $stmt->execute([$username]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($row) {
        return [$row['hashed_password'], $row['salt']];
    } else {
        return [null, null];
    }
}

function create_token($username) {
    global $pdo;
    // Generate a random token
    $token = bin2hex(random_bytes(24));    
    $createdAt = date('Y-m-d H:i:s');
    $expiryDate = date('Y-m-d H:i:s', strtotime('+7 days')); // Set the token expiry date to 7 days in the future
    // Insert the token into the tokens table
    $stmt = $pdo->prepare("INSERT INTO tokens (userId, token, token_created_at, token_expires_at) VALUES (?, ?, ?, ?)");
    $stmt->execute([$username, $token, $createdAt, $expiryDate]);
    return $token;
}

function validate_token($token) {
    global $pdo;

    // Get the token from the tokens table
    $stmt = $pdo->prepare("SELECT userId, token_expires_at FROM tokens WHERE token = ?");
    $stmt->execute([$token]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($row && strtotime($row['token_expires_at']) > time()) {
        // Token is valid and not expired, return the username
        return $row['userId'];
    } else {
        // Token is invalid or expired, return null
        return null;
    }
}

?>