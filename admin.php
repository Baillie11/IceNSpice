<?php
require_once 'config.php';

if (!isAdminLoggedIn()) {
    redirect('admin_login.php');
}

$db = getDb();
$message = '';

// Handle new challenge submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['challenge_text'])) {
    $challengeText = trim($_POST['challenge_text']);
    $intensity = (int)$_POST['intensity'];
    $orientation = $_POST['orientation'];
    $pairing = $_POST['pairing'];
    
    if ($challengeText) {
        $stmt = $db->prepare("INSERT INTO challenges (intensity, orientation, pairing, challenge_text) VALUES (?, ?, ?, ?)");
        $stmt->execute([$intensity, $orientation, $pairing, $challengeText]);
        $message = "Challenge added successfully!";
    }
}

// Get all challenges
$stmt = $db->query("SELECT * FROM challenges ORDER BY id");
$challenges = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Admin - Ice n Spice</title>
  <link rel="icon" type="image/png" href="assets/icenspicelogo.png">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    textarea:focus {
      min-height: 6rem;
    }
  </style>
</head>
<body class="bg-gray-100 text-gray-800 flex flex-col min-h-screen">
  <div class="flex-grow p-4 md:p-6">
  <div class="max-w-6xl mx-auto">
    <h1 class="text-2xl md:text-3xl font-bold mb-6 text-center text-red-500">Admin Panel - Manage Challenges</h1>

    <?php if ($message): ?>
      <div class="bg-green-100 text-green-700 p-3 rounded mb-4"><?= htmlspecialchars($message) ?></div>
    <?php endif; ?>

    <!-- Add New Challenge Form -->
    <form method="POST" action="admin.php" class="bg-white p-4 rounded-lg shadow-md mb-6">
      <h2 class="text-xl font-semibold mb-4">Add New Challenge</h2>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block mb-1 text-sm font-semibold">Challenge Text</label>
          <textarea name="challenge_text"
                    placeholder="Enter challenge here"
                    class="p-2 border rounded w-full resize-y min-h-[2.5rem]"
                    required></textarea>
        </div>

        <div>
          <label class="block mb-1 text-sm font-semibold">Intensity (1–10)</label>
          <select name="intensity" class="p-2 border rounded w-full" required>
            <?php for ($i = 1; $i <= 10; $i++): ?>
            <option value="<?= $i ?>"><?= $i ?></option>
            <?php endfor; ?>
          </select>
        </div>

        <div>
          <label class="block mb-1 text-sm font-semibold">Orientation</label>
          <select name="orientation" class="p-2 border rounded w-full" required>
            <option value="Straight">Straight</option>
            <option value="Bi">Bi</option>
            <option value="Gay">Gay</option>
            <option value="Lesbian">Lesbian</option>
            <option value="All">All</option>
          </select>
        </div>

        <div>
          <label class="block mb-1 text-sm font-semibold">Pairing</label>
          <select name="pairing" class="p-2 border rounded w-full" required>
            <option value="Male to Female">Male to Female</option>
            <option value="Female to Male">Female to Male</option>
            <option value="Male to Male">Male to Male</option>
            <option value="Female to Female">Female to Female</option>
            <option value="All">All</option>
          </select>
        </div>
      </div>
      <button type="submit" class="mt-4 px-6 py-2 bg-red-500 text-white rounded hover:bg-red-600">Add Challenge</button>
    </form>

    <!-- Bulk Import Form -->
    <div class="bg-pink-100 p-4 rounded mb-6">
      <h3 class="text-lg font-semibold mb-2">📥 Bulk Import Challenges</h3>
      <form action="bulk_import.php" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv" required class="mb-2">
        <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Import</button>
      </form>
      <p class="text-sm text-gray-600 mt-2">
        File format: CSV with headers → <code>challenge_text,intensity,orientation,pairing</code>
      </p>
    </div>

    <!-- Challenge Count -->
    <h2 class="text-2xl font-semibold mb-2">Existing Challenges</h2>
    <div class="text-center text-sm text-gray-600 mb-4">
      Total Challenges: <strong><?= count($challenges) ?></strong>
    </div>

    <!-- Column Headings -->
    <div class="grid grid-cols-1 md:grid-cols-6 gap-4 items-center bg-yellow-300 p-4 rounded-t shadow mb-0 font-semibold">
      <div class="text-center">#</div>
      <div>Challenge Text</div>
      <div>Intensity</div>
      <div>Orientation</div>
      <div>Pairing</div>
      <div class="text-center">Actions</div>
    </div>

    <!-- Challenge List -->
    <?php foreach ($challenges as $index => $challenge): ?>
    <form method="POST" action="update_challenge.php"
          class="grid grid-cols-1 md:grid-cols-6 gap-4 items-center bg-white p-4 <?= $index === 0 ? '' : 'rounded' ?> shadow mb-4">
      <input type="hidden" name="id" value="<?= $challenge['id'] ?>">
      <div class="text-gray-500 font-semibold text-center"><?= $index + 1 ?></div>
      <textarea name="challenge_text"
                class="p-2 border rounded w-full resize-y min-h-[2.5rem]"
                required><?= htmlspecialchars($challenge['challenge_text']) ?></textarea>
      <select name="intensity" class="p-2 border rounded w-full">
        <?php for ($i = 1; $i <= 10; $i++): ?>
        <option value="<?= $i ?>" <?= $challenge['intensity'] == $i ? 'selected' : '' ?>><?= $i ?></option>
        <?php endfor; ?>
      </select>
      <select name="orientation" class="p-2 border rounded w-full">
        <?php foreach (['Straight', 'Bi', 'Gay', 'Lesbian', 'All'] as $option): ?>
        <option value="<?= $option ?>" <?= $challenge['orientation'] == $option ? 'selected' : '' ?>><?= $option ?></option>
        <?php endforeach; ?>
      </select>
      <select name="pairing" class="p-2 border rounded w-full">
        <?php foreach (['Male to Female', 'Female to Male', 'Male to Male', 'Female to Female', 'All'] as $option): ?>
        <option value="<?= $option ?>" <?= $challenge['pairing'] == $option ? 'selected' : '' ?>><?= $option ?></option>
        <?php endforeach; ?>
      </select>
      <div class="flex flex-col md:flex-row justify-center gap-2">
        <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Save</button>
        <a href="delete_challenge.php?id=<?= $challenge['id'] ?>"
           class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 text-center"
           onclick="return confirm('Are you sure you want to delete this challenge?');">Delete</a>
      </div>
    </form>
    <?php endforeach; ?>

    <div class="mt-6 text-center">
      <a href="admin_logout.php" class="text-red-500 hover:underline">Logout</a>
    </div>
  </div>
  </div>
  
  <!-- Footer -->
  <footer class="text-center py-3 text-sm text-gray-600 mt-auto">
      Powered by <a href="https://www.clickecommerce.com.au" target="_blank" class="text-red-500 hover:underline">Click eCommerce</a>
  </footer>
</body>
</html>
