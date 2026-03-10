<?php
// Level 2 PHP bridge — forwards NEO software requests to the FastAPI backend.
// The NEO machine calls this endpoint. This file calls FastAPI and returns the result.
// Nothing in the Python codebase knows this file exists.

$fastapi_url = "http://localhost:8000/api/inspect";

$image_data = file_get_contents("php://input");

$ch = curl_init($fastapi_url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $image_data);
curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
curl_close($ch);

header("Content-Type: application/json");
echo $response;
?>
