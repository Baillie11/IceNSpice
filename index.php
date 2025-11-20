<?php
require_once 'config.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ice n Spice</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 text-gray-800">

    <div class="min-h-screen flex items-center justify-center py-6 px-4">
        <div class="max-w-5xl w-full">
            
            <!-- Main Content Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
                
                <!-- Left Column: Logo & Description -->
                <div class="flex flex-col items-center lg:items-start text-center lg:text-left">
                    <img src="assets/icenspicelogo.png" alt="Ice n Spice Logo" class="w-40 md:w-48 mb-4">
                    
                    <h1 class="text-3xl md:text-4xl font-bold text-red-500 mb-3">Welcome to Ice n Spice</h1>
                    
                    <p class="text-base md:text-lg text-gray-600 mb-4">
                        A fun couples ice breaker game where individuals and couples complete exciting challenges together. Get ready to connect, laugh, and spice things up!
                    </p>
                    
                    <!-- Buttons for larger screens -->
                    <div class="hidden lg:flex flex-col gap-3 w-full max-w-xs">
                        <a href="setup.php" class="w-full">
                            <button class="w-full px-6 py-3 bg-red-500 text-white font-semibold text-lg rounded-lg shadow-md hover:bg-red-600 transition-all">
                                Start a New Game
                            </button>
                        </a>
                        
                        <a href="suggest.php" class="w-full">
                            <button class="w-full px-6 py-3 bg-green-500 text-white font-semibold text-lg rounded-lg shadow-md hover:bg-green-600 transition-all">
                                Suggest a Challenge
                            </button>
                        </a>
                        
                        <a href="admin_login.php" class="text-red-500 hover:underline text-center mt-2">
                            Admin Login
                        </a>
                    </div>
                </div>
                
                <!-- Right Column: How to Play -->
                <div class="bg-white rounded-lg shadow-lg p-6">
                    <h2 class="text-2xl font-semibold mb-4 text-center lg:text-left text-red-500">How to Play:</h2>
                    <ul class="space-y-3 text-base md:text-lg">
                        <li class="flex items-start">
                            <span class="text-red-500 mr-2 flex-shrink-0">✔️</span>
                            <span>Each player (individuals or couples) enters their name</span>
                        </li>
                        <li class="flex items-start">
                            <span class="text-red-500 mr-2 flex-shrink-0">✔️</span>
                            <span>The game randomly assigns player order</span>
                        </li>
                        <li class="flex items-start">
                            <span class="text-red-500 mr-2 flex-shrink-0">✔️</span>
                            <span>Complete fun challenges with the person or couple you are paired with!</span>
                        </li>
                    </ul>
                </div>
            </div>
            
            <!-- Buttons for mobile/tablet -->
            <div class="lg:hidden flex flex-col items-center gap-3 mt-6">
                <a href="setup.php" class="w-full max-w-xs">
                    <button class="w-full px-6 py-3 bg-red-500 text-white font-semibold text-lg rounded-lg shadow-md hover:bg-red-600 transition-all">
                        Start a New Game
                    </button>
                </a>
                
                <a href="suggest.php" class="w-full max-w-xs">
                    <button class="w-full px-6 py-3 bg-green-500 text-white font-semibold text-lg rounded-lg shadow-md hover:bg-green-600 transition-all">
                        Suggest a Challenge
                    </button>
                </a>
                
                <a href="admin_login.php" class="text-red-500 hover:underline text-lg mt-2">
                    Admin Login
                </a>
            </div>
            
        </div>
    </div>

</body>
</html>
