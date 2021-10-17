<?php
    // CONNECTING TO PROJECT DATABASE
$host = 'localhost';
$user = 'root';
$password = '';
$db = 'project';
// GLOBAL VARIABLE ACCESSIBLE BY ALL PHP DOCUMENTS
$link_project = mysqli_connect($host, $user, $password, $db);
?>