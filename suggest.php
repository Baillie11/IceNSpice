<?php
require_once 'config.php';

$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $challengeIdea = trim($_POST['challenge_idea'] ?? '');
    
    if ($challengeIdea) {
        $subject = "New Challenge Suggestion for Ice n Spice";
        $emailMessage = "New challenge idea submitted:\n\n$challengeIdea";
        
        // Send email
        $headers = "From: " . SMTP_USERNAME . "\r\n";
        $headers .= "Reply-To: " . SMTP_USERNAME . "\r\n";
        
        if (mail(ADMIN_EMAIL, $subject, $emailMessage, $headers)) {
            $message = "Your challenge suggestion has been submitted!";
        } else {
            $message = "There was an error sending your suggestion. Please try again.";
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Suggest a Challenge</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 text-gray-800">

    <div class="flex flex-col items-center min-h-screen py-10 px-5">
        <h1 class="text-4xl font-bold text-red-500">Suggest a Challenge</h1>
        <p class="text-lg text-center text-gray-600 mt-4 max-w-xl">
            Have a great challenge idea? Submit it below, and it might be added to Ice n Spice!
        </p>

        <?php if ($message): ?>
            <div class="mt-4 p-3 <?= strpos($message, 'error') !== false ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700' ?> rounded">
                <?= htmlspecialchars($message) ?>
            </div>
        <?php endif; ?>

        <form action="suggest.php" method="POST" class="mt-6 w-full max-w-md bg-white p-5 rounded-lg shadow">
            <textarea name="challenge_idea" rows="4" placeholder="Enter your challenge idea..." required
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"></textarea>

            <button type="submit"
                    class="w-full mt-3 px-6 py-2 bg-red-500 text-white font-semibold rounded-lg shadow-md hover:bg-red-600 transition">
                Submit Suggestion
            </button>
        </form>

        <a href="index.php" class="mt-6 text-red-500 hover:underline text-lg">Back to Home</a>
    </div>

    <!-- Footer -->
    <footer class="text-center py-4 text-sm text-gray-600">
        Powered by <a href="https://www.clickecommerce.com.au" target="_blank" class="text-red-500 hover:underline">Click eCommerce</a>
    </footer>

</body>
</html>
