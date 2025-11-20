<?php
require_once 'config.php';

if (!isAdminLoggedIn()) {
    redirect('admin_login.php');
}

if (isset($_GET['id'])) {
    $id = (int)$_GET['id'];
    
    $db = getDb();
    $stmt = $db->prepare("DELETE FROM challenges WHERE id = ?");
    $stmt->execute([$id]);
}

redirect('admin.php');
