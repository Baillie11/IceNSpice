<?php
require_once 'config.php';

if (!isset($_SESSION['players']) || empty($_SESSION['players'])) {
    redirect('setup.php');
}

$currentRound = $_SESSION['current_round'] ?? 1;

if ($currentRound < 10) {
    $_SESSION['current_round'] = $currentRound + 1;
    $_SESSION['current_question_number'] = 1;
    $_SESSION['current_player_index'] = 0;
} else {
    // Game over, return to home
    session_destroy();
    redirect('index.php');
}

redirect('gameplay.php');
