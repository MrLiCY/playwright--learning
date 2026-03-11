from playwright.sync_api import sync_playwright

def main():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.baidu.com")
    print("页面加载完成\n")

    print("=== 练习1: 获取元素文本内容 ===")

    news_link = page.locator("text=新闻").first
    news_text = news_link.inner_text()
    print(f"新闻链接文本内容: {news_text}\n")

    search_box = page.locator("#chat-textarea").filter(visible=True)
    placeholder = search_box.get_attribute("placeholder")
    print(f"搜索框占位符文本: {placeholder}\n")

    print("\n获取所有导航链接")
    nav_links = page.locator("a.mnav")
    for i in range(max(1, nav_links.count())):
        link = nav_links.nth(i)
        link_text = link.inner_text()
        print(f"导航链接 {i+1}: {link_text}")
    page.wait_for_timeout(2000)

    print("\n=== 练习2: 获取元素状态 ===")
    # 检查搜索框是否可见
    is_visible = search_box.is_visible()
    print(f"搜索框是否可见: {is_visible}")
    
    is_enabled = search_box.is_editable()
    print(f"搜索框是否可编辑: {is_enabled}")

    exists = page.locator("#chat-textarea").count() > 0
    print(f"搜索框是否存在: {exists}")

    page.wait_for_timeout(2000)

    page_html = page.content()
    print(f"页面HTML内容长度: {len(page_html)}")
    page_html = page.content()                                                                                                                                                                                   
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(page_html)                                                                                                                                                                                       
    print("HTML已保存到 page.html")

    print("回车结束程序")
    input()

if __name__ == "__main__":
    main()
