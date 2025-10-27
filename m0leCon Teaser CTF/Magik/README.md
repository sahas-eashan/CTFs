# Magik Challenge - CTF Notes

## Summary
ImageMagick exploitation challenge where we need to execute `/readflag` SUID binary.

## Vulnerability
Unquoted bash variables in `convert.sh` allow argument injection, but file output is inaccessible.

## Status
- ✅ Command injection confirmed (semicolons work)
- ✅ Multiple exploitation techniques tested
- ❌ Cannot access created files via HTTP (all paths return 404 or index.php)
- ❌ Flag not retrieved

## Possible Issues
1. **Instance may have additional protections** not in provided source
2. **PHP routing** may prevent file access
3. **static/ directory may not exist** in running instance
4. **Working directory** may be different than expected
5. **File permissions** may prevent writing

## Exploits Created
- [exploit_bypass.py](exploit_bypass.py) - Comprehensive bypass attempts
- [exploit_direct.py](exploit_direct.py) - Direct flag write methods
- [test_semicolon.py](test_semicolon.py) - Semicolon injection tests
- [test_readflag.py](test_readflag.py) - Various output techniques

## Next Steps if Continuing
1. Get fresh instance
2. Test if actual command execution is happening (use `sleep` or network callback)
3. Try exfiltrating via DNS or HTTP callback
4. Check for WAF/proxy differences between local and remote
5. Review ImageMagick CVEs that don't require colon

## Analysis Files
- [SOLUTION.md](SOLUTION.md) - Initial analysis
- [DETAILED_ANALYSIS.md](DETAILED_ANALYSIS.md) - In-depth technical breakdown
- [results.txt](results.txt) - User-provided bypass techniques

## Key Learning
The challenge demonstrates:
- Unquoted variable expansion in bash scripts
- `proc_open()` behavior with array arguments
- PHP built-in server routing
- ImageMagick security considerations
