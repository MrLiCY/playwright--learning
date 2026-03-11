"""
Playwright 异步模板 - 高性能版本
当你需要并发操作多个页面时使用这个
"""

import asyncio
from playwright.async_api import async_playwright

async def main():
    """
    异步版本的关键区别：
    1. 使用 async_playwright() 而不是 sync_playwright()
    2. 所有操作都要加 await
    3. 使用 async/await 语法
    """
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        # 创建上下文
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )

        # 创建页面
        page = await context.new_page()

        try:
            # 访问页面（注意每个操作都要 await）
            await page.goto("https://www.baidu.com")

            # 获取信息（也要 await）
            title = await page.title()
            url = page.url
            print(f"标题: {title}")
            print(f"URL: {url}")

            # 等待（也要 await）
            await page.wait_for_timeout(3000)

        except Exception as e:
            print(f"发生错误: {e}")

        finally:
            # 清理资源（也要 await）
            await context.close()
            await browser.close()

if __name__ == "__main__":
    # 运行异步函数
    asyncio.run(main())