# Magik CTF Challenge - Solution Analysis

## Vulnerability
The `convert.sh` script uses unquoted bash variables:
```bash
convert $1 -resize 64x64 -background none -gravity center -extent 64x64 $2
```

Where:
- `$1` = PHP temporary file (user-uploaded image)
- `$2` = `static/<name>.png` where `<name>` is user-controlled via POST parameter

## Exploitation
Since `$2` is unquoted, spaces in the `name` parameter cause argument splitting.

### What Works:
1. ✓ Argument injection via spaces
2. ✓ Writing to `/app/` directory (static/ doesn't exist)
3. ✓ File upload with `application/octet-stream` MIME type

### What's Blocked:
1. ✗ Colon `:` character (blocks all ImageMagick protocols like `label:`, `caption:`, `text:`, etc.)
2. ✗ Direct read of `/flag.txt` (permission denied, owned by root, chmod 400)
3. ✗ Path traversal with `../`

### Required:
- Execute `/readflag` SUID binary to get the flag

## Attempted Approaches:
1. Protocol injection (`label:@/flag.txt`) - blocked by `:` filter
2. MSL file upload and triggering - couldn't reference MSL files
3. SVG/PS/EPS command injection - filtered or failed
4. Ghostscript delegate exploitation - disabled or protected
5. PHP file writing - ImageMagick only outputs image formats

## Next Steps:
The solution likely involves one of:
1. Finding an ImageMagick pseudo-protocol that doesn't use `:`
2. Exploiting a specific image format's delegate without `:`
3. Using MSL with a different trigger mechanism
4. Race condition or file operation exploit
5. Alternative ImageMagick RCE vector

## Note:
This challenge requires deep ImageMagick knowledge and possibly a CVE-specific exploit.
