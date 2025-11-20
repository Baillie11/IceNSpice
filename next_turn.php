<?php
require_once 'config.php';

if (!isset($_SESSION['players']) || empty($_SESSION['players'])) {
    redirect('setup.php');
}

$players = $_SESSION['players'];
$currentPlayerIndex = $_SESSION['current_player_index'] ?? 0;
$questionNumber = $_SESSION['current_question_number'] ?? 1;
$currentRound = $_SESSION['current_round'] ?? 1;

// Move to next player
$currentPlayerIndex = ($currentPlayerIndex + 1) % count($players);
$questionNumber++;

// Check if round is complete
$totalQuestions = count($players) * 2;
if ($questionNumber > $totalQuestions) {
    if ($currentRound < 10) {
        $currentRound++;
        $questionNumber = 1;
    } else {
        // Game over, return to home
        session_destroy();
        redirect('index.php');
    }
}

// Update session
$_SESSION['current_player_index'] = $currentPlayerIndex;
$_SESSION['current_question_number'] = $questionNumber;
$_SESSION['current_round'] = $currentRound;

redirect('gameplay.php');
