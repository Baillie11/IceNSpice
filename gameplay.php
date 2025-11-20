<?php
require_once 'config.php';

// Check if players exist
if (!isset($_SESSION['players']) || empty($_SESSION['players'])) {
    redirect('setup.php');
}

$players = $_SESSION['players'];
$currentPlayerIndex = $_SESSION['current_player_index'] ?? 0;
$questionNumber = $_SESSION['current_question_number'] ?? 1;
$roundNumber = $_SESSION['current_round'] ?? 1;
$currentPlayer = $players[$currentPlayerIndex];

// Function to get matching player
function getMatchingPlayer($currentPlayer, $pairing, $players) {
    $potential = [];
    $currentName = $currentPlayer['name'];
    $currentSex = $currentPlayer['sex'];
    $currentOrientation = $currentPlayer['orientation'];
    $currentPartner = $currentPlayer['partner'] ?? null;
    
    foreach ($players as $p) {
        if ($p['name'] === $currentName) {
            continue;
        }
        if ($currentPartner && $p['name'] === $currentPartner) {
            continue;
        }
        
        $match = false;
        if ($pairing === "Male to Female" && $currentSex === "Male" && $p['sex'] === "Female") {
            $match = true;
        } elseif ($pairing === "Female to Male" && $currentSex === "Female" && $p['sex'] === "Male") {
            $match = true;
        } elseif ($pairing === "Male to Male" && $currentSex === "Male" && $p['sex'] === "Male") {
            $match = true;
        } elseif ($pairing === "Female to Female" && $currentSex === "Female" && $p['sex'] === "Female") {
            $match = true;
        } elseif ($pairing === "All") {
            $match = true;
        }
        
        if ($match) {
            if ($currentOrientation === "Straight" && in_array($pairing, ["Male to Male", "Female to Female"])) {
                continue;
            }
            if ($currentOrientation === "Gay" && ($pairing !== "Male to Male" || $p['sex'] !== "Male")) {
                continue;
            }
            if ($currentOrientation === "Lesbian" && ($pairing !== "Female to Female" || $p['sex'] !== "Female")) {
                continue;
            }
            $potential[] = $p['name'];
        }
    }
    
    return !empty($potential) ? $potential[array_rand($potential)] : null;
}

// Get random challenge
$db = getDb();
$stmt = $db->query("SELECT challenge_text, pairing FROM challenges ORDER BY RANDOM() LIMIT 1");
$row = $stmt->fetch(PDO::FETCH_ASSOC);

if ($row) {
    $challengeText = $row['challenge_text'];
    $pairing = $row['pairing'];
    $partnerName = getMatchingPlayer($currentPlayer, $pairing, $players);
    
    $challengeText = str_replace("USERNAME", $currentPlayer['name'], $challengeText);
    $challengeText = str_replace("PARTNERNAME", $partnerName ?: "someone", $challengeText);
} else {
    $challengeText = "No challenges available.";
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gameplay - Ice n Spice</title>
  <link rel="icon" type="image/png" href="assets/icenspicelogo.png">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-pink-100 min-h-screen">
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 p-4 max-w-7xl mx-auto">

    <!-- Logo (Top on mobile, left on desktop) -->
    <div class="lg:col-span-2 flex items-start justify-center lg:justify-start">
      <img src="assets/icenspicelogo.png" alt="Logo" class="h-16">
    </div>

    <!-- Challenge Display -->
    <div class="lg:col-span-8 text-center">
      <h1 class="text-3xl font-bold text-red-600 mb-2">Challenges</h1>
      <div class="flex justify-center space-x-8 mb-4">
        <p class="text-lg font-medium text-gray-700">Round <?= $roundNumber ?></p>
        <p class="text-lg font-medium text-gray-700">Question <?= $questionNumber ?></p>
      </div>

      <div class="bg-white p-6 rounded shadow text-xl font-semibold text-gray-800 min-h-[120px] flex items-center justify-center">
        <?= htmlspecialchars($challengeText) ?>
      </div>

      <form method="POST" action="next_turn.php" class="mt-6 flex justify-center space-x-4">
        <button type="submit" class="bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600">Next</button>
      </form>

      <form method="POST" action="skip_round.php" class="mt-2 flex justify-center">
        <button type="submit" class="bg-yellow-500 text-white px-6 py-2 rounded hover:bg-yellow-600">Skip Round</button>
      </form>

      <div class="mt-4 text-center">
        <a href="quit.php" class="text-red-500 hover:underline">Quit Game</a>
      </div>
    </div>

    <!-- Player Order (Bottom on mobile, right on desktop) -->
    <div class="lg:col-span-2">
      <h2 class="text-lg font-semibold text-gray-700 mb-2 text-center lg:text-left">Players</h2>
      <ul class="space-y-1">
        <?php foreach ($players as $index => $player): ?>
        <li class="<?= $index === $currentPlayerIndex ? 'text-xl font-bold text-blue-600' : 'text-gray-700' ?> text-center lg:text-left">
          <?= htmlspecialchars($player['name']) ?>
        </li>
        <?php endforeach; ?>
      </ul>
    </div>

  </div>
  
  <!-- Footer -->
  <footer class="text-center py-4 text-sm text-gray-600">
      Powered by <a href="https://www.clickecommerce.com.au" target="_blank" class="text-red-500 hover:underline">Click eCommerce</a>
  </footer>
</body>
</html>
