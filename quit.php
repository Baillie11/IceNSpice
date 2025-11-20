<?php
require_once 'config.php';

// Clear game session data
unset($_SESSION['players']);
unset($_SESSION['current_player_index']);
unset($_SESSION['current_question_number']);
unset($_SESSION['current_round']);

redirect('index.php');
