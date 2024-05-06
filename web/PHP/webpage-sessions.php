<?php
session_start();

// Function to get user permissions and password from text file
function getUserPermissions($userId) {
    // Path to the text file containing user permissions and passwords
    $filePath = 'permissions.txt';

    // Read the contents of the text file
    $permissionsData = file_get_contents($filePath);

    // Split the contents into an array of lines
    $lines = explode("\n", $permissionsData);

    // Iterate through each line to find the user ID and associated password
    foreach ($lines as $line) {
        // Extract user ID and password from the line using regular expressions
        if (preg_match('/Password\("(\d+)"\) = "([^"]+)"/', $line, $matches)) {
            $lineUserId = $matches[1];
            $password = $matches[2];
            // Check if the extracted user ID matches the provided user ID
            if ($lineUserId == $userId) {
                return ['password' => $password]; // Return the password associated with the user ID
            }
        }
    }

    // User ID not found, return an empty array or handle error as needed
    return [];
}

// Check if the user is authenticated
if (!isset($_SESSION['user_id'])) {
    header("Location: ./web/Debeg.php"); // Redirect to login page if not authenticated
    exit();
}

// Retrieve user permissions and password from text file
$userId = $_SESSION['user_id'];
$userData = getUserPermissions($userId);

// Generate webpage content based on user permissions
if (isset($userData['permissions'])) {
    // User has permissions, display appropriate content
    if (in_array('admin', $userData['permissions'])) {
        // Display admin dashboard
        include('admin_dashboard.php');
    } elseif (in_array('user', $userData['permissions'])) {
        // Display user dashboard
        include('user_dashboard.php');
    } else {
        // Display error page
        include('error_page.php');
    }
} elseif (isset($userData['password'])) {
    // Password is set for the user, handle password authentication or other actions
    // Implement your password authentication logic here
    $enteredPassword = ""; // Get the entered password from the form
    $storedPassword = $userData['password']; // Get the stored password from the file
    if ($enteredPassword == $storedPassword) {
        // Password authentication successful, display appropriate content
        include('authenticated_page.php');
    } else {
        // Password authentication failed, display error message or redirect to login page
        header("Location: ./web/Debeg.php"); // Redirect to login page
        exit();
    }
} else {
    // Invalid user or data format, display error message or redirect to login page
    header("Location: ./web/Debeg.php"); // Redirect to login page
    exit();
}
?>