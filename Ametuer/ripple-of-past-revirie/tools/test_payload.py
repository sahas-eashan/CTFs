#!/usr/bin/env python3
"""
Quick helper to iterate on username payloads locally.

It renders web/index.php with an arbitrary ?username= value via render.php,
opens the resulting HTML in Playwright's Chromium, and prints every console
message + request so you can confirm your script fired before shipping it to
the remote bot.
"""

import argparse
import pathlib
import subprocess
import sys
from typing import Optional

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
RENDER_SCRIPT = ROOT / "render.php"
OUTPUT_HTML = ROOT / "rendered.html"


def render_payload(payload: str) -> pathlib.Path:
    """Run `php render.php <payload>` and dump the HTML to rendered.html."""
    if not RENDER_SCRIPT.exists():
        raise SystemExit(f"render.php not found at {RENDER_SCRIPT}")

    result = subprocess.run(
        ["php", str(RENDER_SCRIPT), payload],
        check=True,
        capture_output=True,
    )
    OUTPUT_HTML.write_bytes(result.stdout)
    return OUTPUT_HTML.resolve()


def browse(rendered: pathlib.Path, headless: bool, timeout_ms: int) -> None:
    """Open HTML in Chromium, echo console/network noise, wait a bit."""
    url = rendered.as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.on(
            "console",
            lambda msg: print(f"[console:{msg.type}] {msg.text}"),
        )
        page.on(
            "request",
            lambda req: print(f"[request] {req.method} {req.url}"),
        )
        page.on(
            "response",
            lambda resp: print(f"[response] {resp.status} {resp.url}"),
        )
        print(f"[+] Opening {url}")
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(timeout_ms)
        browser.close()


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render index.php with a payload and open it in Chromium.",
    )
    parser.add_argument(
        "payload",
        help="String to stuff into ?username=...",
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Show the real browser window (default: headless).",
    )
    parser.add_argument(
        "--wait",
        type=int,
        default=5000,
        help="How long to keep the page open (ms, default 5000).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> None:
    args = parse_args(argv)
    rendered = render_payload(args.payload)
    print(f"[+] Wrote {rendered}")
    browse(rendered, headless=not args.no_headless, timeout_ms=args.wait)


if __name__ == "__main__":
    main(sys.argv[1:])
