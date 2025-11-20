<?php
require_once 'config.php';

unset($_SESSION['admin_logged_in']);
redirect('index.php');
