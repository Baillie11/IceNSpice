<?php
require_once 'config.php';

// Check if players exist
if (!isset($_SESSION['players']) || empty($_SESSION['players'])) {
    redirect('setup.php');
}

// Shuffle the players
shuffle($_SESSION['players']);

// Initialize game state
$_SESSION['current_player_index'] = 0;
$_SESSION['current_question_number'] = 1;
$_SESSION['current_round'] = 1;

// Redirect to gameplay
redirect('gameplay.php');
