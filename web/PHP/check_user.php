<?php
$userId = $_GET['userId'];
$filename = 'allowed-users.txt';

// Read the file content
$fileContent = file_get_contents($filename);

if ($fileContent !== false) {
    // Remove whitespace and newlines
    $fileContent = preg_replace('/\s+/', '', $fileContent);

    // Extract user IDs as an array
    preg_match_all('/\[(.*?)\]/', $fileContent, $matches);

    // Flatten the array and remove empty strings
    $userIds = array_filter(explode(',', implode(',', $matches[1])));

    // Convert user IDs to strings
    $userIds = array_map('strval', $userIds);

    // Check if the user ID is in the array
    if (in_array($userId, $userIds)) {
        echo 'UserID found in the file.';
    } else {
        echo 'UserID not found in the file.';
    }
} else {
    echo 'File not found or could not be read.';
}
