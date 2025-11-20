<?php
require_once 'config.php';

if (!isAdminLoggedIn()) {
    redirect('admin_login.php');
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $file = $_FILES['file'];
    
    if ($file['error'] === UPLOAD_ERR_OK) {
        $handle = fopen($file['tmp_name'], 'r');
        
        if ($handle) {
            $db = getDb();
            $count = 0;
            
            // Skip header row
            $header = fgetcsv($handle);
            
            // Process each row
            while (($data = fgetcsv($handle)) !== false) {
                if (count($data) >= 4) {
                    $challengeText = trim($data[0]);
                    $intensity = (int)$data[1];
                    $orientation = trim($data[2]);
                    $pairing = trim($data[3]);
                    
                    if ($challengeText) {
                        $stmt = $db->prepare("INSERT INTO challenges (challenge_text, intensity, orientation, pairing) VALUES (?, ?, ?, ?)");
                        $stmt->execute([$challengeText, $intensity, $orientation, $pairing]);
                        $count++;
                    }
                }
            }
            
            fclose($handle);
            $_SESSION['import_message'] = "Successfully imported $count challenges.";
        }
    } else {
        $_SESSION['import_message'] = "Error uploading file.";
    }
}

redirect('admin.php');
