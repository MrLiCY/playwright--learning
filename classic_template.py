"""
Playwright 经典模板 - 同步版本
这是最常用的基础模板，可以直接复制使用
"""

from playwright.sync_api import sync_playwright

def main():
    """
    Playwright 的标准写法：
    1. 使用 sync_playwright() 上下文管理器
    2. launch() 启动浏览器
    3. new_context() 创建上下文
    4. new_page() 创建页面
    5. 进行各种操作
    6. 记得清理资源
    """
    with sync_playwright() as p:
        # ========== 第一步：启动浏览器 ==========
        browser = p.chromium.launch(
            headless=False,              # 是否无头模式（False=显示界面）
            args=[
                "--disable-blink-features=AutomationControlled",  # 反检测
            ]
        )

        # ========== 第二步：创建上下文 ==========
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},  # 视口大小
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"  # 用户代理
        )

        # ========== 第三步：创建页面 ==========
        page = context.new_page()

        # ========== 第四步：开始你的操作 ==========
        try:
            # 访问页面
            page.goto("https://www.baidu.com", timeout=30000)  # timeout 单位是毫秒

            # 经典操作系列（你会频繁用到的）：

            # 1. 获取页面信息
            title = page.title()
            url = page.url
            print(f"标题: {title}")
            print(f"URL: {url}")

            # 2. 等待操作（Playwright 的特色）
            page.wait_for_timeout(3000)  # 显式等待 3 秒

            # 3. 元素操作（后面会详细讲）
            # page.click("#selector")
            # page.fill("#input", "text")
            # page.get_by_text("内容").click()

            # 4. 获取页面内容
            # html = page.content()
            # text = page.inner_text("#element")

        except Exception as e:
            print(f"发生错误: {e}")

        finally:
            # ========== 第五步：清理资源 ==========
            context.close()
            browser.close()

if __name__ == "__main__":
    main()