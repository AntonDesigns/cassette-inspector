<?php
// Level 2 only. This file lives on the NEO machine, not on the FastAPI server.
// The Trymax NEO software calls this endpoint. I forward the request straight
// to FastAPI and return the response. 


// The Python codebase never knows I exist.


// I am not active in Level 1. To enable Level 2:
//   1. Deploy this file to the NEO machine's web server
//   2. Uncomment app.include_router(inspect.router) in api/main.py
//   3. Make sure the NEO machine can reach PORT 8000 on the FastAPI server
//   4. Update FASTAPI_URL below to the actual network address of the server

define("FASTAPI_URL", "http://localhost:8000/api/inspect");
if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    header("Content-Type: application/json");
    echo json_encode(["error" => "Method not allowed"]);
    exit;
}

$body = file_get_contents("php://input");

if (empty($body)) {
    http_response_code(400);
    header("Content-Type: application/json");
    echo json_encode(["error" => "Empty request body"]);
    exit;
}
$ch = curl_init(FASTAPI_URL);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST,           true);
curl_setopt($ch, CURLOPT_POSTFIELDS,     $body);
curl_setopt($ch, CURLOPT_HTTPHEADER,     ["Content-Type: application/json"]);
curl_setopt($ch, CURLOPT_TIMEOUT,        10);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlError = curl_error($ch);
curl_close($ch);
if ($response === false) {
    http_response_code(502);
    header("Content-Type: application/json");
    echo json_encode(["error" => "Could not reach FastAPI: " . $curlError]);
    exit;
}
http_response_code($httpCode);
header("Content-Type: application/json");
echo $response;
