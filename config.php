<?php
// Load environment variables
require_once __DIR__ . '/env_loader.php';

// Database configuration
define('DB_FILE', __DIR__ . '/challenges.db');

// Admin credentials - loaded from .env file
define('ADMIN_USERNAME', env('ADMIN_USERNAME', 'admin'));
define('ADMIN_PASSWORD', env('ADMIN_PASSWORD', 'password123'));

// Email configuration - loaded from .env file
define('ADMIN_EMAIL', env('ADMIN_EMAIL', 'andrew@clickecommerce.com.au'));
define('SMTP_SERVER', env('SMTP_SERVER', 'smtp.gmail.com'));
define('SMTP_PORT', (int)env('SMTP_PORT', 587));
define('SMTP_USERNAME', env('SMTP_USERNAME', 'your_email@gmail.com'));
define('SMTP_PASSWORD', env('SMTP_PASSWORD', 'your_app_password'));

// Session configuration
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Initialize database
function initDatabase() {
    try {
        $db = new PDO('sqlite:' . DB_FILE);
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        $db->exec("
            CREATE TABLE IF NOT EXISTS challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intensity INTEGER NOT NULL CHECK(intensity BETWEEN 1 AND 10),
                orientation TEXT NOT NULL CHECK(orientation IN ('All', 'Straight', 'Bi', 'Gay', 'Lesbian')),
                pairing TEXT NOT NULL CHECK(pairing IN (
                    'Male to Female', 'Female to Male', 'Male to Male', 'Female to Female', 'All'
                )),
                challenge_text TEXT NOT NULL
            )
        ");
        
        return $db;
    } catch (PDOException $e) {
        die("Database connection failed: " . $e->getMessage());
    }
}

// Get database connection
function getDb() {
    static $db = null;
    if ($db === null) {
        $db = initDatabase();
    }
    return $db;
}

// Check if admin is logged in
function isAdminLoggedIn() {
    return isset($_SESSION['admin_logged_in']) && $_SESSION['admin_logged_in'] === true;
}

// Redirect helper
function redirect($url) {
    header("Location: $url");
    exit;
}
