from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # ============= 第一层： 启动浏览器 =================
        print("第一层： 启动浏览器")
        browser = p.chromium.launch(headless=False) # False可见浏览器 True不可见浏览器

        # ============= 第二层： 创建页面 =================
        print("第二层： 创建第一个上下文（用户a）")
        context_a = browser.new_context()
        print("第二层： 创建第二个上下文（用户b）")
        context_b = browser.new_context()

        # ============= 第三层：创建页面 =================
        print("用户a打开第一个标签")
        page_a1 = context_a.new_page()
        print("用户a打开第二个标签")
        page_a2 = context_a.new_page()
        print("用户b打开第一个标签")
        page_b1 = context_b.new_page()

         # 让我们看看这些页面的关系
        print("\n" + "="*50)
        print("架构层次关系：")
        print("="*50)
        print("Browser (Chrome程序)")
        print("  ├─ Context A (用户A的隐身窗口)")
        print("  │   ├─ Page A1 (用户A的标签页1)")
        print("  │   └─ Page A2 (用户A的标签页2)")
        print("  └─ Context B (用户B的隐身窗口)")
        print("      └─ Page B1 (用户B的标签页1)")
        print("="*50 + "\n")

        # ============= 第四层： 页面操作 =================
        page_a1.goto("https://www.baidu.com")
        page_a2.goto("https://www.google.com")
        page_b1.goto("https://www.bing.com")

        print("\n 等待5秒， 观察浏览器窗口")
        page_a1.wait_for_timeout(5000)

        # ============= 清理资源 =================
        print("开始清理资源。。。")
        context_a.close()
        context_b.close()
        browser.close()
        print("资源清理完成，浏览器已关闭")

if __name__ == "__main__":
    main()