<?php
require_once 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    
    if ($username === ADMIN_USERNAME && $password === ADMIN_PASSWORD) {
        $_SESSION['admin_logged_in'] = true;
        redirect('admin.php');
    } else {
        $error = "Invalid credentials";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="flex flex-col items-center justify-center min-h-screen bg-gray-100 text-gray-800">

    <h1 class="text-3xl font-bold text-red-500">Admin Login</h1>

    <?php if (isset($error)): ?>
        <div class="mt-4 p-3 bg-red-100 text-red-700 rounded"><?= htmlspecialchars($error) ?></div>
    <?php endif; ?>

    <form action="admin_login.php" method="POST" class="mt-6 w-full max-w-sm bg-white p-5 rounded-lg shadow">
        <input type="text" name="username" placeholder="Username" required
               class="w-full px-4 py-2 border border-gray-300 rounded-lg">
        <input type="password" name="password" placeholder="Password" required
               class="w-full mt-3 px-4 py-2 border border-gray-300 rounded-lg">
        <button type="submit" class="w-full mt-3 px-6 py-2 bg-red-500 text-white font-semibold rounded-lg shadow-md hover:bg-red-600 transition">
            Login
        </button>
    </form>

    <a href="index.php" class="mt-4 text-blue-500 hover:underline">Back to Home</a>

    <!-- Footer -->
    <footer class="text-center py-4 text-sm text-gray-600 mt-8">
        Powered by <a href="https://www.clickecommerce.com.au" target="_blank" class="text-red-500 hover:underline">Click eCommerce</a>
    </footer>

</body>
</html>
