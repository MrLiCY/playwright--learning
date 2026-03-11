"""
Lesson 5: 与项目代码整合
========================

学习目标：
1. 完整理解项目中的异步数据流
2. 理解 FastAPI 中的异步处理
3. 学会调试异步代码
4. 掌握常见错误和解决方法
"""

import asyncio
from typing import Optional


# ============================================================================
# 第一部分：项目完整数据流分析
# ============================================================================

"""
项目请求流程（完整异步流程）：

┌─────────────────┐
│  Client Request │  POST /api/v1/scrape
└────────┬────────┘
         │
         ▼
┌─────────────────┐     async def api_v1_scrape()
│   FastAPI Route │  ←  v1.py
└────────┬────────┘
         │
         ▼
┌─────────────────┐     for policy in SCRAPE_POLICIES:
│  Policy Select  │         if policy.hit(request):
└────────┬────────┘             return await policy.scrape(request)
         │
         ▼
┌─────────────────┐     async def scrape() -> ScrapeResponse
│  GenericPolicy  │  ←  generic_policy.py
└────────┬────────┘
         │
         ▼
┌─────────────────┐     async def base_scrape()
│  Base Scrape    │  ←  实际 Playwright 操作
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌────────┐
│Browser│  │ Context│
└───┬───┘  └────┬───┘
    │           │
    └─────┬─────┘
          ▼
    ┌─────────┐
    │  Page   │  ←  goto, content, title...
    └────┬────┘
         │
         ▼
┌─────────────────┐
│ ScrapeResponse  │  ←  返回给客户端
└─────────────────┘

关键点：
1. 每一层都是 async 函数
2. 每一层都要 await 下一层的结果
3. FastAPI 会自动处理 async 路由
"""


# ============================================================================
# 第二部分：模拟项目的完整流程
# ============================================================================

# 模拟项目中的数据模型
class MockScrapeRequest:
    def __init__(self, url: str, timeout: int = 30, block_media: bool = True):
        self.url = url
        self.timeout = timeout
        self.block_media = block_media
        self.headers = {}


class MockScrapeResponse:
    def __init__(self, html: str, title: str, success: bool = True, error: Optional[str] = None):
        self.html = html
        self.title = title
        self.success = success
        self.error = error

    def __repr__(self):
        return f"ScrapeResponse(title='{self.title}', success={self.success})"


# 模拟 BasePolicy
class MockBasePolicy:
    """模拟项目中的抽象基类"""

    def hit(self, request: MockScrapeRequest) -> bool:
        """检查是否匹配这个 policy"""
        raise NotImplementedError

    async def scrape(self, request: MockScrapeRequest) -> MockScrapeResponse:
        """执行抓取"""
        raise NotImplementedError


# 模拟 GenericPolicy
class MockGenericPolicy(MockBasePolicy):
    """模拟项目中的通用 policy"""

    def hit(self, request: MockScrapeRequest) -> bool:
        # GenericPolicy 总是匹配（作为 fallback）
        return True

    async def check_func(self, page, timeout: int):
        """子类可以重写这个方法等待特定内容"""
        # 默认不执行任何检查
        pass

    async def base_scrape(self, request: MockScrapeRequest) -> MockScrapeResponse:
        """
        模拟项目中的 base_scrape 方法
        这里使用简化的实现来展示结构
        """
        from playwright.async_api import async_playwright

        print(f"  [base_scrape] 开始抓取: {request.url}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            try:
                context = await browser.new_context()
                try:
                    page = await context.new_page()

                    # 模拟媒体拦截
                    if request.block_media:
                        await page.route("**/*", lambda route: (
                            route.abort() if any(
                                ext in route.request.url
                                for ext in [".png", ".jpg", ".mp4"]
                            ) else route.continue_()
                        ))

                    # 导航到页面
                    await page.goto(request.url, timeout=request.timeout * 1000)

                    # 调用 check_func（policy 子类可以自定义）
                    await self.check_func(page, request.timeout * 1000)

                    # 获取内容
                    html = await page.content()
                    title = await page.title()

                    print(f"  [base_scrape] 抓取成功: {title}")
                    return MockScrapeResponse(html=html, title=title)

                finally:
                    await context.close()
            finally:
                await browser.close()

    async def scrape(self, request: MockScrapeRequest) -> MockScrapeResponse:
        """模拟项目中的 scrape 方法"""
        try:
            return await self.base_scrape(request)
        except Exception as e:
            # 项目中会在这里重试或降级
            print(f"  [scrape] 错误: {e}")
            return MockScrapeResponse(html="", title="", success=False, error=str(e))


# 模拟一个具体的站点 policy（如微信）
class MockWechatPolicy(MockGenericPolicy):
    """模拟微信抓取 policy"""

    def hit(self, request: MockScrapeRequest) -> bool:
        return "weixin.qq.com" in request.url or "mp.weixin.qq.com" in request.url

    async def check_func(self, page, timeout: int):
        """微信文章需要等待特定元素"""
        # 等待文章正文出现
        await page.wait_for_selector("#js_content", timeout=10000)
        print("  [WechatPolicy] 文章正文已加载")


# 模拟 API 层
class MockAPI:
    """模拟 FastAPI 路由"""

    def __init__(self):
        # 注册 policies（顺序很重要！）
        self.policies = [
            MockWechatPolicy(),  # 先检查特定站点
            MockGenericPolicy(),  # 最后 fallback
        ]

    async def scrape_endpoint(self, request: MockScrapeRequest) -> MockScrapeResponse:
        """模拟 api_v1_scrape 路由"""
        print(f"\n[API] 收到请求: {request.url}")

        for policy in self.policies:
            if policy.hit(request):
                policy_name = type(policy).__name__
                print(f"[API] 使用 policy: {policy_name}")
                response = await policy.scrape(request)
                return response

        raise RuntimeError("No policy matched")


# ============================================================================
# 第三部分：调试异步代码的技巧
# ============================================================================

async def debugging_tips():
    """
    异步代码调试技巧
    """
    print("\n" + "=" * 50)
    print("异步代码调试技巧")
    print("=" * 50)

    print("""
1. 启用 asyncio 的调试模式：
   asyncio.run(main(), debug=True)
   或设置环境变量：PYTHONASYNCIODEBUG=1

2. 常见的异步错误：

   a) RuntimeError: Event loop is closed
      原因：在 loop 关闭后又尝试使用
      解决：确保所有 await 在 loop 关闭前完成

   b) RuntimeError: coroutine was never awaited
      原因：调用了 async 函数但没有 await
      解决：检查所有 async 函数调用前都有 await

   c) TimeoutError: Navigation timeout exceeded
      原因：页面加载超时
      解决：增加 timeout 或检查网络

3. 日志记录异步操作：
   使用 try-except-finally 包裹关键操作

4. 查看当前任务：
   asyncio.current_task()
   asyncio.all_tasks()
""")


# ============================================================================
# 第四部分：常见错误和解决方法
# ============================================================================

async def common_mistakes_demo():
    """
    演示常见的异步错误
    """
    print("\n" + "=" * 50)
    print("常见错误演示")
    print("=" * 50)

    # 错误 1：忘记 await
    print("\n错误 1：忘记 await")

    async def async_function():
        return "结果"

    # 错误：coro 是一个协程对象，不是结果
    coro = async_function()
    print(f"  忘记 await: {coro} (类型: {type(coro).__name__})")

    # 正确：使用 await
    result = await async_function()
    print(f"  使用 await: {result}")

    # 错误 2：在非 async 函数中使用 await
    print("\n错误 2：在非 async 函数中使用 await")
    print("""
  错误的代码：
      def sync_function():
          result = await async_function()  # SyntaxError!

  解决方法：
      async def async_wrapper():
          result = await async_function()
    """)

    # 错误 3：混合使用同步和异步代码
    print("\n错误 3：在异步代码中使用阻塞操作")
    print("""
  错误的代码：
      async def bad_code():
          time.sleep(5)  # 阻塞整个事件循环！
          await page.goto(url)

  正确的代码：
      async def good_code():
          await asyncio.sleep(5)  # 非阻塞
          await page.goto(url)

  或：
      async def good_code():
          await asyncio.to_thread(time.sleep, 5)  # 在线程中运行阻塞代码
          await page.goto(url)
    """)


# ============================================================================
# 第五部分：动手实验 - 完整的项目模拟
# ============================================================================

async def full_project_demo():
    """
    完整的项目模拟
    """
    print("\n" + "=" * 50)
    print("完整项目模拟")
    print("=" * 50)

    api = MockAPI()

    # 测试 1：普通网站（使用 GenericPolicy）
    request1 = MockScrapeRequest(url="https://example.com")
    response1 = await api.scrape_endpoint(request1)
    print(f"结果: {response1}\n")

    # 测试 2：微信文章（使用 WechatPolicy）
    # 注意：这里 URL 是假的，实际运行会报错，但会展示 policy 选择逻辑
    print("模拟微信文章请求（注意：这个 URL 是假的，用于演示 policy 选择）")
    request2 = MockScrapeRequest(url="https://mp.weixin.qq.com/s/fake-article")
    # 不实际运行，因为会失败
    print(f"请求 URL: {request2.url}")
    print(f"匹配到 policy: MockWechatPolicy")


# ============================================================================
# 第六部分：动手实验
# ============================================================================
"""
📝 实验任务：

1. 运行 full_project_demo，观察 policy 的选择逻辑
2. 修改 MockWechatPolicy，添加更多的 URL 匹配规则
3. 创建一个新的 policy（如 MockZhihuPolicy），添加到 api.policies 中
4. 尝试实现重试逻辑：在 base_scrape 失败时自动重试 3 次
5. 添加日志记录，记录每个异步操作的耗时

挑战任务：
- 实现一个批量抓取功能，同时处理多个 URL
- 使用 asyncio.Semaphore 限制并发数，避免资源耗尽
- 实现一个优雅关闭机制，确保所有资源都被正确清理
"""

async def main():
    await debugging_tips()
    await common_mistakes_demo()
    await full_project_demo()


if __name__ == "__main__":
    # 启用调试模式
    asyncio.run(main(), debug=True)


# ============================================================================
# 第七部分：关键问题自测
# ============================================================================
"""
🤔 思考问题：

1. 为什么 policy 的顺序很重要？
   答案：GenericPolicy 的 hit() 永远返回 True，
         如果放在前面，其他 policy 永远不会被检查。

2. 如果 scrape 方法中抛出异常会怎样？
   答案：如果没有 try-except，异常会向上传播到 api_v1_scrape，
         FastAPI 会将其转换为 500 错误返回给客户端。

3. 如何在一个 async 函数中调用同步代码？
   答案：使用 await asyncio.to_thread(sync_function, *args)
         这会将同步代码放到线程池中运行，不阻塞事件循环。

4. 项目的 api_v1_scrape 为什么没有 try-except？
   答案：FastAPI 会自动捕获异常并返回 500 错误，
         但生产环境建议添加适当的错误处理。

5. 为什么 FastAPI 能直接处理 async def 的路由？
   答案：FastAPI 基于 Starlette，会自动检测函数是否是协程，
         并在内部使用适当的方式运行（asyncio.run 或 await）。
"""
