$enc = Get-Content "level1.zip" -Encoding Byte
$wordlist = @(
    'password', 'guess', 'ctf', 'flag', 'pure', 'pureguess', 'pure-guess',
    'tutorial', 'memory', 'working', 'last', 'this', 'confused', 'confusion',
    'lastguess', 'thisguess', 'guessctflast', 'guessctfthis',
    'idonthavememory', 'idonthaveworkingmemory', 'nodontremember',
    'therewasnolast', 'firstguessctf', 'zerothguessctf',
    'flag{last}', 'flag{this}', 'flag{pure}', 'flag{guess}',
    'level0', 'level1', '0', '1'
)

foreach ($word in $wordlist) {
    $keyBytes = [System.Text.Encoding]::UTF8.GetBytes($word)
    $dec = for ($i = 0; $i -lt [Math]::Min(4, $enc.Length); $i++) {
        $enc[$i] -bxor $keyBytes[$i % $keyBytes.Length]
    }
    
    if ($dec[0] -eq 0x50 -and $dec[1] -eq 0x4B) {
        Write-Host "FOUND: $word" -ForegroundColor Green
        
        # Decrypt full file
        $decrypted = for ($i = 0; $i -lt $enc.Length; $i++) {
            $enc[$i] -bxor $keyBytes[$i % $keyBytes.Length]
        }
        [System.IO.File]::WriteAllBytes("$PWD\level1_decrypted_final.zip", [byte[]]$decrypted)
        
        # Try to extract
        try {
            Expand-Archive -Path "level1_decrypted_final.zip" -DestinationPath "level1_solved" -Force
            Write-Host "Successfully extracted!" -ForegroundColor Green
            Get-ChildItem "level1_solved" -Recurse
        } catch {
            Write-Host "Extraction error: $_" -ForegroundColor Yellow
        }
        break
    }
}

Write-Host "Brute force complete"
