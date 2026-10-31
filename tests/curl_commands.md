# API cURL commands

Run these commands in PowerShell after starting Django at `http://127.0.0.1:8000` and seeding the database. These use the native `curl.exe`. Replace the credentials with an account you create locally.

```powershell
$base = "http://127.0.0.1:8000/api"

function Invoke-CurlJson {
    param([string]$Path, [hashtable]$Payload, [string]$Token = "")
    $bodyFile = Join-Path $env:TEMP "cars-dealership-request.json"
    $json = $Payload | ConvertTo-Json -Compress
    [IO.File]::WriteAllText($bodyFile, $json, [Text.UTF8Encoding]::new($false))
    try {
        $curlArgs = @("-sS", "-X", "POST", "-H", "Content-Type: application/json")
        if ($Token) { $curlArgs += @("-H", "Authorization: Token $Token") }
        $curlArgs += @("--data-binary", "@$bodyFile", "$base$Path")
        & curl.exe @curlArgs
    } finally {
        Remove-Item -LiteralPath $bodyFile -ErrorAction SilentlyContinue
    }
}

# Register once, or skip this step if you already have an account.
Invoke-CurlJson "/register/" @{ username = "YOUR_USERNAME"; email = "you@example.test"; password = "YOUR_PASSWORD" }

# Login and retain the token for protected calls.
$login = Invoke-CurlJson "/loginuser/" @{ username = "YOUR_USERNAME"; password = "YOUR_PASSWORD" } | ConvertFrom-Json
$token = $login.token

# Public dealership and review data.
$dealers = curl.exe -sS "$base/getalldealers/" | ConvertFrom-Json
$dealerId = $dealers[0].id
curl.exe -sS "$base/getdealerbyid/$dealerId/"
curl.exe -sS "$base/getdealerreviews/$dealerId/"
curl.exe -sS "$base/getdealersbyState/KS/"
curl.exe -sS "$base/getallcarmakes/"
Invoke-CurlJson "/analyzereview/" @{ review = "Fantastic services" }

# Authenticated review submission and logout.
Invoke-CurlJson "/dealers/$dealerId/reviews/" @{ text = "A helpful and friendly team." } $token
curl.exe -sS -X POST -H "Authorization: Token $token" "$base/logoutuser/"
```

The local database used for the captured outputs contains demonstration data. No usable credentials are committed here.
