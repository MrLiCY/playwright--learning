"""
Lesson 4: 实用异步技术
======================

学习目标：
1. 理解 page.route 的异步拦截机制
2. 学会在异步环境中执行 JavaScript
3. 理解 wait_for_selector 和 wait_for_timeout 的用法
4. 掌握项目中常见的异步操作组合
"""

import asyncio
from playwright.async_api import async_playwright, Route


# ============================================================================
# 第一部分：异步路由拦截 (page.route)
# ============================================================================

async def route_interception_demo():
    """
    演示项目中使用的路由拦截技术

    项目中的应用：
    - 拦截广告域名并 abort
    - 拦截媒体文件（图片、视频）并 abort（当 block_media=True 时）
    """

    print("\n" + "=" * 50)
    print("异步路由拦截演示")
    print("=" * 50)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            context = await browser.new_context()
            page = await context.new_page()

            # 记录拦截的请求
            intercepted_requests = []

            # 定义拦截处理函数 - 这是一个异步回调
            async def handle_route(route: Route):
                url = route.request.url

                # 拦截所有图片请求
                if any(ext in url for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                    print(f"  [拦截] 图片请求: {url[:60]}...")
                    intercepted_requests.append(url)
                    await route.abort()  # 中止请求
                else:
                    await route.continue_()  # 继续请求

            # 启用路由拦截 - 所有请求都会经过 handle_route
            await page.route("**/*", handle_route)
            print("已启用路由拦截（会拦截所有图片）")

            # 访问一个包含图片的页面
            await page.goto("https://example.com")
            print(f"总共拦截了 {len(intercepted_requests)} 个图片请求")

            # 项目中的实际用法：
            print("""
项目中的实际代码：

    # 拦截广告域名
    await page.route(
        "**/*",
        lambda route: (
            route.abort()
            if any(domain in route.request.url for domain in BLOCKED_DOMAINS)
            else route.continue_()
        ),
    )

关键点：
1. route 处理函数可以是普通函数或 async 函数
2. 必须调用 route.abort() 或 route.continue_()，否则请求会挂起
3. 这是异步操作，因为拦截决策可能需要异步逻辑（如查询数据库）
            """)

        finally:
            await browser.close()


# ============================================================================
# 第二部分：异步等待机制
# ============================================================================

async def waiting_mechanisms_demo():
    """
    演示项目中使用的各种等待机制

    项目中的应用：
    - check_func: 等待特定元素出现
    - wait_for_timeout: 固定时间等待
    """

    print("\n" + "=" * 50)
    print("异步等待机制演示")
    print("=" * 50)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://example.com")

            # 1. 等待特定选择器
            print("\n1. wait_for_selector - 等待元素出现")
            try:
                # 等待 h1 元素，最多等 5 秒
                await page.wait_for_selector("h1", timeout=5000)
                print("   h1 元素已找到")
            except Exception as e:
                print(f"   等待超时: {e}")

            # 2. 固定时间等待
            print("\n2. wait_for_timeout - 固定时间等待")
            print("   开始等待 1 秒...")
            await page.wait_for_timeout(1000)  # 1000ms = 1s
            print("   等待结束")

            # 3. 等待网络空闲
            print("\n3. goto 的 wait_until 参数")
            print("""
   wait_until 可选值：
   - load: 等待 load 事件（默认）
   - domcontentloaded: 等待 DOMContentLoaded 事件
   - networkidle: 等待网络空闲（500ms 没有网络请求）

   项目中的用法：
       response = await page.goto(url, wait_until="networkidle")

   如果网络一直不空闲，会超时，所以项目中会有 fallback：
       try:
           return await self.base_scrape(request, wait_until="load")
       except Exception:
           return await self.base_scrape(request, wait_until="networkidle")
            """)

        finally:
            await browser.close()


# ============================================================================
# 第三部分：异步执行 JavaScript
# ============================================================================

async def execute_javascript_demo():
    """
    演示如何在异步环境中执行 JavaScript

    这在爬虫中很有用：
    - 获取页面上 JavaScript 计算的值
    - 执行页面滚动
    - 修改页面 DOM
    """

    print("\n" + "=" * 50)
    print("异步执行 JavaScript 演示")
    print("=" * 50)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://example.com")

            # 1. 执行脚本并返回值
            print("\n1. 执行脚本并获取返回值")
            title = await page.evaluate("document.title")
            print(f"   页面标题: {title}")

            # 2. 获取页面信息
            print("\n2. 获取页面尺寸和滚动位置")
            page_info = await page.evaluate("""
                () => {
                    return {
                        width: document.documentElement.scrollWidth,
                        height: document.documentElement.scrollHeight,
                        scrollY: window.scrollY
                    }
                }
            """)
            print(f"   页面信息: {page_info}")

            # 3. 执行页面滚动
            print("\n3. 滚动页面")
            await page.evaluate("window.scrollTo(0, 500)")
            new_scroll = await page.evaluate("window.scrollY")
            print(f"   滚动后位置: {new_scroll}")

            # 4. 修改 DOM（项目中的场景）
            print("\n4. 修改 DOM 元素")
            await page.evaluate("""
                () => {
                    const h1 = document.querySelector('h1');
                    if (h1) {
                        h1.style.backgroundColor = 'yellow';
                        return '已修改 h1 样式';
                    }
                    return '未找到 h1';
                }
            """)
            print("   已尝试修改 h1 背景色")

        finally:
            await browser.close()


# ============================================================================
# 第四部分：综合练习 - 实现一个完整的异步爬虫函数
# ============================================================================

async def comprehensive_scraper_demo():
    """
    综合练习：实现一个类似项目中的完整异步爬虫函数

    功能：
    1. 启动带 stealth 的浏览器
    2. 拦截广告请求
    3. 导航到页面
    4. 等待特定元素
    5. 执行 JavaScript 获取额外信息
    6. 返回页面内容
    """

    print("\n" + "=" * 50)
    print("综合练习：完整异步爬虫实现")
    print("=" * 50)

    async def advanced_scrape(url: str, check_selector: str = None) -> dict:
        """
        高级异步爬虫函数

        这个函数展示了项目中常用的模式组合
        """
        from playwright_stealth import Stealth

        result = {
            "url": url,
            "title": None,
            "content": None,
            "meta_description": None,
            "success": False,
            "error": None
        }

        try:
            # 使用 stealth 包装器（项目中使用的反检测技术）
            async with Stealth().use_async(async_playwright()) as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=["--disable-blink-features=AutomationControlled"]
                )

                try:
                    context = await browser.new_context(
                        viewport={"width": 1920, "height": 1080}
                    )

                    try:
                        page = await context.new_page()

                        # 拦截广告和分析脚本
                        blocked_domains = ["googleads", "analytics", "tracking"]
                        await page.route("**/*", lambda route: (
                            route.abort()
                            if any(d in route.request.url for d in blocked_domains)
                            else route.continue_()
                        ))

                        # 导航到页面
                        response = await page.goto(url, wait_until="load")

                        # 等待特定选择器（如果指定）
                        if check_selector:
                            await page.wait_for_selector(
                                check_selector,
                                timeout=10000
                            )

                        # 等待动态内容加载
                        await page.wait_for_timeout(500)

                        # 收集信息
                        result["title"] = await page.title()
                        result["content"] = await page.content()
                        result["meta_description"] = await page.evaluate("""
                            () => {
                                const meta = document.querySelector('meta[name="description"]');
                                return meta ? meta.content : null;
                            }
                        """)
                        result["status_code"] = response.status if response else None
                        result["success"] = True

                    finally:
                        await context.close()

                finally:
                    await browser.close()

        except Exception as e:
            result["error"] = str(e)

        return result

    # 运行爬虫
    print("\n开始抓取...")
    result = await advanced_scrape(
        url="https://example.com",
        check_selector="h1"
    )

    print(f"抓取结果:")
    print(f"  URL: {result['url']}")
    print(f"  成功: {result['success']}")
    print(f"  标题: {result['title']}")
    print(f"  状态码: {result.get('status_code')}")
    print(f"  描述: {result['meta_description']}")
    print(f"  错误: {result['error']}")
    print(f"  内容长度: {len(result['content']) if result['content'] else 0} 字符")


# ============================================================================
# 第五部分：动手实验
# ============================================================================
"""
📝 实验任务：

1. 修改 route_interception_demo，尝试拦截并修改响应内容（使用 route.fulfill）
2. 在 execute_javascript_demo 中，尝试获取页面所有链接的 URL
3. 修改 comprehensive_scraper_demo，添加更多的错误处理逻辑
4. 尝试同时运行多个 advanced_scrape，使用 asyncio.gather

挑战任务：
- 实现一个可以递归爬取页面所有链接的爬虫
- 使用 asyncio.Semaphore 限制并发数量（防止同时打开太多浏览器）
"""

async def main():
    await route_interception_demo()
    await waiting_mechanisms_demo()
    await execute_javascript_demo()
    await comprehensive_scraper_demo()


if __name__ == "__main__":
    asyncio.run(main())


# ============================================================================
# 第六部分：关键问题自测
# ============================================================================
"""
🤔 思考问题：

1. 为什么 route 处理函数里必须调用 route.continue_() 或 route.abort()？
   答案：否则请求会一直挂起等待处理，导致页面加载卡住。

2. wait_for_selector 和 query_selector 有什么区别？
   答案：wait_for_selector 会等待元素出现（带超时），
         query_selector 立即返回，元素不存在时返回 None。

3. page.evaluate 中的代码在哪个上下文执行？
   答案：在页面的 JavaScript 上下文中执行，可以访问 document、window 等。

4. 项目中的 check_func 是做什么的？
   答案：policy 的子类可以重写这个方法，用于等待特定于该网站的内容出现。
         例如微信 policy 可以等待文章正文加载完成。

5. 为什么要 block 广告和媒体资源？
   答案：减少网络请求，加快页面加载速度，节省带宽，减少内存使用。
"""
