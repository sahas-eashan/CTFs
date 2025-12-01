<?php
if ($argc > 1) {
    $_GET['username'] = $argv[1];
}
if (!function_exists('mb_substr')) {
    function mb_substr($string, $start, $length = null, $encoding = null) {
        return $length === null ? substr($string, $start) : substr($string, $start, $length);
    }
}
include 'web/index.php';
?>
