from playwright.sync_api import sync_playwright
import pathlib
path = pathlib.Path('rendered.html').resolve().as_uri()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(path, wait_until='domcontentloaded')
    count = page.locator('script').count()
    print('script count', count)
    for i in range(count):
        node = page.locator('script').nth(i)
        print(i, node.get_attribute('nonce'), node.inner_html()[:30])
    browser.close()
