from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser - p.chromium.launch(headless=False)

        context_a = browser.new_context()
        context_b = browser.new_context()

        page_a1 = context_a.new_page()
        page_b1 = context_b.new_page()

        page_a1.goto("https://www.baidu.com")
        page_a1.fill("")