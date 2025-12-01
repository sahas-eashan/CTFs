from playwright.sync_api import sync_playwright
import pathlib
path = pathlib.Path('svg_anim.html').resolve().as_uri()
print('path', path)
with sync_playwright() as p:
    print('launching')
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on('console', lambda msg: print('console:', msg.type, msg.text))
    print('goto start')
    page.goto(path, wait_until='domcontentloaded')
    print('goto done')
    page.wait_for_timeout(2000)
    browser.close()
