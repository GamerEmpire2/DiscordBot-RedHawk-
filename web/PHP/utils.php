<?php
// FILE: utils.php

function findDotenvFile($startDir) {
    $dir = $startDir;
    while (basename($dir) !== 'web') {
        $dir = dirname($dir);
        if ($dir === '/' || $dir === '\\') {
            // We've reached the root directory and didn't find the 'web' directory
            return false;
        }
    }
    // Go up one level from 'web' to the project root
    $dir = dirname($dir);
    if (!file_exists($dir . '/.env')) {
        // .env file not found in project root
        return false;
    }
    return $dir . '/.env';
}