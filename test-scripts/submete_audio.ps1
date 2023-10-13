$filePath = "c:\Users\gustavo.lima\Videos\ironmeidi.mp3"
$fileBytes = [System.IO.File]::ReadAllBytes($filePath)
$base64File = [System.Convert]::ToBase64String($fileBytes)
$headers = @{
    "Content-Type" = "multipart/form-data"
}
Invoke-WebRequest -Uri "http://localhost:5000/upload" -Method POST -Headers $headers -Body @{file = $base64File}
