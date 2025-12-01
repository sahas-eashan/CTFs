from playwright.sync_api import sync_playwright
import pathlib
path = pathlib.Path('dom_test2.html').resolve().as_uri()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on('console', lambda msg: print('console:', msg.type, msg.text))
    page.goto(path)
    page.wait_for_timeout(1000)
    browser.close()
