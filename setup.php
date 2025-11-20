<?php
require_once 'config.php';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $orientation = $_POST['orientation'] ?? '';
    $sex = $_POST['sex'] ?? '';
    $partner = trim($_POST['partner'] ?? '');
    
    if ($name && $orientation && $sex) {
        if (!isset($_SESSION['players'])) {
            $_SESSION['players'] = [];
        }
        
        $_SESSION['players'][] = [
            'name' => $name,
            'orientation' => $orientation,
            'sex' => $sex,
            'partner' => $partner ?: null
        ];
    }
}

$players = $_SESSION['players'] ?? [];
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ice n Spice - Player Setup</title>
  <link rel="icon" type="image/png" href="assets/icenspicelogo.png">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-pink-100 flex flex-col min-h-screen">
  <div class="max-w-3xl mx-auto py-6 px-4">
    <!-- Logo -->
    <div class="flex justify-center mb-6">
      <img src="assets/icenspicelogo.png" alt="Ice n Spice Logo" class="h-20">
    </div>

    <!-- Heading -->
    <h1 class="text-3xl font-bold text-center text-red-600 mb-6">Get Ready to Break the Ice</h1>

    <!-- Player Form -->
    <form method="POST" action="setup.php" class="bg-white p-6 rounded-lg shadow space-y-4">
      <div>
        <label for="name" class="block text-sm font-semibold mb-1">Name</label>
        <input type="text" id="name" name="name" placeholder="Enter your name" required class="w-full p-2 border rounded">
      </div>

      <div>
        <label for="sex" class="block text-sm font-semibold mb-1">Sex</label>
        <select id="sex" name="sex" required class="w-full p-2 border rounded">
          <option value="Male">Male</option>
          <option value="Female">Female</option>
        </select>
      </div>

      <div>
        <label for="orientation" class="block text-sm font-semibold mb-1">Orientation</label>
        <select id="orientation" name="orientation" required class="w-full p-2 border rounded">
          <option value="Straight">Straight</option>
          <option value="Bi">Bi</option>
          <option value="Gay">Gay</option>
          <option value="Lesbian">Lesbian</option>
          <option value="All">All</option>
        </select>
      </div>

      <div>
        <label for="partner" class="block text-sm font-semibold mb-1">Partner (optional)</label>
        <select id="partner" name="partner" class="w-full p-2 border rounded">
          <option value="">-- Select Partner --</option>
          <?php foreach ($players as $player): ?>
          <option value="<?= htmlspecialchars($player['name']) ?>"><?= htmlspecialchars($player['name']) ?></option>
          <?php endforeach; ?>
        </select>
      </div>

      <button type="submit" class="w-full bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600">Add Player</button>
    </form>

    <!-- Players List -->
    <?php if (!empty($players)): ?>
    <div class="mt-8">
      <h2 class="text-xl font-semibold text-center text-gray-700 mb-2">Players in the Game</h2>
      <ul class="bg-white p-4 rounded-lg shadow divide-y divide-gray-200">
        <?php foreach ($players as $player): ?>
        <li class="py-2">
          <strong><?= htmlspecialchars($player['name']) ?></strong> (<?= htmlspecialchars($player['sex']) ?>, <?= htmlspecialchars($player['orientation']) ?>)
          <?php if ($player['partner']): ?>
            <span class="text-sm text-gray-500">– Partner: <?= htmlspecialchars($player['partner']) ?></span>
          <?php endif; ?>
        </li>
        <?php endforeach; ?>
      </ul>
      <div class="text-center mt-4">
        <a href="randomize.php" class="inline-block bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600">Start Game</a>
      </div>
    </div>
    <?php endif; ?>
  </div>
  
  <!-- Footer -->
  <footer class="text-center py-3 text-sm text-gray-600 mt-auto">
      Powered by <a href="https://www.clickecommerce.com.au" target="_blank" class="text-red-500 hover:underline">Click eCommerce</a>
  </footer>
</body>
</html>
