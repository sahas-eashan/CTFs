#!/usr/bin/env python3
"""
Quick health check to verify all services are ready before submitting.
"""

import socket
import sys
import urllib.request
import urllib.error


def check_query_logger():
    """Check if query_logger.py is running on port 8000."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('127.0.0.1', 8000))
        sock.close()
        if result == 0:
            print("✓ Query logger is running on port 8000")
            return True
        else:
            print("✗ Query logger is NOT running on port 8000")
            print("  → Run: python tools\\query_logger.py --port 8000")
            return False
    except Exception as e:
        print(f"✗ Error checking query logger: {e}")
        return False


def check_ngrok(ngrok_url):
    """Check if ngrok URL is accessible."""
    if not ngrok_url:
        print("✗ No ngrok URL provided")
        print("  → Start ngrok: ngrok http 8000")
        print("  → Copy the HTTPS URL shown")
        return False

    try:
        # Try to access ngrok URL
        req = urllib.request.Request(ngrok_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=5)
        print(f"✓ Ngrok URL is accessible: {ngrok_url}")
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"✓ Ngrok URL is accessible (404 is expected): {ngrok_url}")
            return True
        print(f"✗ Ngrok URL returned error {e.code}: {ngrok_url}")
        return False
    except Exception as e:
        print(f"✗ Cannot reach ngrok URL: {e}")
        print(f"  URL: {ngrok_url}")
        print("  → Make sure ngrok is running: ngrok http 8000")
        return False


def check_internet():
    """Check internet connectivity to the CTF site."""
    try:
        req = urllib.request.Request(
            'https://web-ripple-of-past-revirie-tfk6tz07.amt.rs/',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        urllib.request.urlopen(req, timeout=5)
        print("✓ Can reach CTF bot URL")
        return True
    except Exception as e:
        print(f"✗ Cannot reach CTF bot: {e}")
        return False


def main():
    print("=" * 60)
    print("Ripple of Past Reverie - Setup Health Check")
    print("=" * 60)
    print()

    # Get ngrok URL from args if provided
    ngrok_url = sys.argv[1] if len(sys.argv) > 1 else None

    checks = [
        check_query_logger(),
        check_ngrok(ngrok_url),
        check_internet(),
    ]

    print()
    print("=" * 60)

    if all(checks):
        print("✓ ALL SYSTEMS GO! Ready to capture the flag.")
        print()
        if ngrok_url:
            print(f"Run this command to submit:")
            print(f'  GET_FLAG.bat "{ngrok_url}"')
        else:
            print("Provide your ngrok URL to check it:")
            print('  python tools\\check_setup.py "https://your-url.ngrok-free.dev"')
        sys.exit(0)
    else:
        print("✗ Some services are not ready. Fix the issues above.")
        print()
        print("Quick setup:")
        print("  1. Terminal 1: python tools\\query_logger.py --port 8000")
        print("  2. Terminal 2: ngrok http 8000")
        print("  3. Terminal 3: GET_FLAG.bat \"https://YOUR-NGROK-URL\"")
        sys.exit(1)


if __name__ == "__main__":
    main()
