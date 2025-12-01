from playwright.sync_api import sync_playwright
import pathlib
path = pathlib.Path('malformed.html').resolve().as_uri()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(path)
    scripts = page.query_selector_all('script')
    print('script count', len(scripts))
    for i,s in enumerate(scripts):
        print(i, s.get_attribute('nonce'), s.inner_html())
    browser.close()
