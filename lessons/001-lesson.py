from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.baidu.com")

        title = page.title()
        print(f"Page title: {title}")

        page.wait_for_timeout(3000)
        
        browser.close()

if __name__ == "__main__":
    main()