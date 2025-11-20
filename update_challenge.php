<?php
require_once 'config.php';

if (!isAdminLoggedIn()) {
    redirect('admin_login.php');
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $id = (int)$_POST['id'];
    $challengeText = trim($_POST['challenge_text']);
    $intensity = (int)$_POST['intensity'];
    $orientation = $_POST['orientation'];
    $pairing = $_POST['pairing'];
    
    $db = getDb();
    $stmt = $db->prepare("UPDATE challenges SET challenge_text = ?, intensity = ?, orientation = ?, pairing = ? WHERE id = ?");
    $stmt->execute([$challengeText, $intensity, $orientation, $pairing, $id]);
}

redirect('admin.php');
