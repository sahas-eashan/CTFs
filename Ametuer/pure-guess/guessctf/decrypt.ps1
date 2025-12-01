# Try multi-byte XOR decryption
$bytes = Get-Content "level1.zip" -Encoding Byte
$keys = @('lastguessctf', 'thisguessctf', 'flag{lastguessctf}', 'flag{thisguessctf}', 'guessctf')

foreach ($keyString in $keys) {
    Write-Host "Trying key: $keyString"
    $keyBytes = [System.Text.Encoding]::UTF8.GetBytes($keyString)
    $decrypted = @()
    
    for ($i = 0; $i -lt $bytes.Length; $i++) {
        $decrypted += $bytes[$i] -bxor $keyBytes[$i % $keyBytes.Length]
    }
    
    $outFile = "level1_$keyString.zip"
    [System.IO.File]::WriteAllBytes("$PWD\$outFile", [byte[]]$decrypted)
    
    # Check first 4 bytes
    $first4 = $decrypted[0..3]
    $hex = ($first4 | ForEach-Object { $_.ToString('X2') }) -join ' '
    Write-Host "  First 4 bytes: $hex"
    
    if ($first4[0] -eq 0x50 -and $first4[1] -eq 0x4B) {
        Write-Host "  FOUND VALID ZIP HEADER!" -ForegroundColor Green
        try {
            Expand-Archive -Path $outFile -DestinationPath "level1_extracted" -Force
            Write-Host "  Successfully extracted!" -ForegroundColor Green
            Get-ChildItem "level1_extracted"
        } catch {
            Write-Host "  Extraction failed: $_" -ForegroundColor Yellow
        }
    }
}
