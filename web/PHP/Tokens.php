<?php

// Include Composer's autoloader
require __DIR__ . './vendor/autoload.php';

// Load environment variables from .env file
$dotenv = Dotenv::createImmutable(__DIR__);
$dotenv->load();

// Get the path to the file containing the tokens from the environment variable
$tokensFilePath = getenv('300TOKENS');

// Check if the tokens file path is empty or not set
if (!$tokensFilePath || !file_exists($tokensFilePath)) {
    echo 'Error: TOKENS_FILE environment variable is not set or points to a non-existing file.';
    exit;
}

// Read tokens from file
$tokensFileContents = file_get_contents($tokensFilePath);
$tokens = explode("\n\n", $tokensFileContents);

// Check if there are tokens available
if (empty($tokens)) {
    echo 'Error: The tokens file is empty.';
    exit;
}

// Pick a random token from the list
$token = trim($tokens[array_rand($tokens)]);

// Write token to file
file_put_contents('./text-files/token_of_the_day.txt', $token);

echo 'Token of the day generated and saved to token_of_the_day.txt';
?>
