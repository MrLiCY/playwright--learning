"""
Lesson 3: 项目中的异步模式详解
==============================

学习目标：
1. 理解项目中 async with 的嵌套模式
2. 理解 try-finally 在异步代码中的应用
3. 理解 Stealth 插件的异步用法
4. 掌握资源的正确清理顺序
"""

import asyncio
from playwright.async_api import async_playwright, Page, Browser, BrowserContext


# ============================================================================
# 第一部分：async with 的嵌套结构
# ============================================================================

async def nested_async_with_demo():
    """
    演示项目中常见的 async with 嵌套模式

    在你的项目中看到的结构：

    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch()
        try:
            context = await browser.new_context()
            try:
                page = await context.new_page()
                # ... 使用 page ...
            finally:
                await context.close()
        finally:
            await browser.close()
    """

    print("\n" + "=" * 50)
    print("async with 嵌套结构演示")
    print("=" * 50)

    # 最简单的形式：单层 async with
    async with async_playwright() as p:
        print("1. playwright 已启动")

        # browser 不使用 async with，需要手动 close
        browser = await p.chromium.launch()
        print("2. browser 已启动")

        try:
            context = await browser.new_context()
            print("3. context 已创建")

            try:
                page = await context.new_page()
                print("4. page 已创建")

                await page.goto("https://example.com")
                print("5. 页面已加载")

            finally:
                # 确保 context 被关闭，即使发生异常
                await context.close()
                print("6. context 已关闭")

        finally:
            # 确保 browser 被关闭，即使发生异常
            await browser.close()
            print("7. browser 已关闭")

    print("8. playwright 已停止")


# ============================================================================
# 第二部分：为什么需要 try-finally
# ============================================================================

async def error_handling_demo():
    """
    演示为什么在异步代码中必须正确清理资源

    场景：如果在 page.goto 时出错了，没有 try-finally 会怎样？
    """

    print("\n" + "=" * 50)
    print("错误处理和资源清理演示")
    print("=" * 50)

    async def bad_practice():
        """错误的做法：可能泄露资源"""
        print("\n[错误示范]")
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # 如果这里抛出异常，browser 和 page 都不会被关闭！
            await page.goto("https://invalid-url-that-does-not-exist.com")

            # 这行代码可能永远不会执行
            await browser.close()

    async def good_practice():
        """正确的做法：确保资源被清理"""
        print("\n[正确示范]")
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            try:
                page = await browser.new_page()
                try:
                    await page.goto("https://invalid-url-that-does-not-exist.com")
                finally:
                    # page 没有 close 方法，但 context 有
                    pass
            except Exception as e:
                print(f"  捕获到异常: {type(e).__name__}")
            finally:
                # 无论是否异常，browser 都会被关闭
                await browser.close()
                print("  browser 已正确关闭")

    # 尝试错误做法（会报错）
    try:
        await bad_practice()
    except Exception as e:
        print(f"  错误示范捕获异常: {type(e).__name__}")
        print("  ⚠️  注意：此时 browser 可能没有被正确关闭！")

    # 正确做法
    await good_practice()


# ============================================================================
# 第三部分：项目中的实际模式解析
# ============================================================================

async def project_pattern_analysis():
    """
    逐行解析 app/policies/generic_policy.py 中的异步模式
    """

    print("\n" + "=" * 50)
    print("项目代码模式分析")
    print("=" * 50)

    print("""
项目中的代码结构（简化版）：

    async with Stealth().use_async(async_playwright()) as p:
        # ↑ 启动 playwright 并应用 stealth 伪装

        browser = await p.chromium.launch(...)
        try:
            # ↑ 启动浏览器

            context = await browser.new_context(...)
            try:
                # ↑ 创建上下文（隔离的浏览器会话）

                page = await context.new_page()
                # ↑ 创建页面

                response = await page.goto(url, ...)
                # ↑ 导航到 URL

                content = await page.content()
                # ↑ 获取页面内容

                return content

            finally:
                await context.close()
                # ↑ 确保上下文关闭

        finally:
            await browser.close()
            # ↑ 确保浏览器关闭

关键点：
1. Stealth 包装器会自动处理 playwright 的启动和停止
2. browser 和 context 使用 try-finally 确保关闭
3. page 不需要显式 close，context 关闭时会自动清理
4. 每一层都可能抛出异常，所以都需要清理逻辑
""")

    # 实际演示这个结构
    async with async_playwright() as p:
        print("1. 启动 playwright")

        browser = await p.chromium.launch(headless=True)
        print("2. 启动 browser")

        try:
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080}
            )
            print("3. 创建 context")

            try:
                page = await context.new_page()
                print("4. 创建 page")

                await page.goto("https://example.com")
                print("5. 加载页面")

                title = await page.title()
                print(f"6. 获取标题: {title}")

            finally:
                await context.close()
                print("7. 关闭 context")

        finally:
            await browser.close()
            print("8. 关闭 browser")


# ============================================================================
# 第四部分：异步函数的链式调用
# ============================================================================

async def async_chain_demo():
    """
    演示项目中 async 函数的链式调用模式

    项目中的调用链：
    api_v1_scrape (v1.py)
        └── scrape_policy.scrape (base.py 定义的抽象方法)
                └── base_scrape (generic_policy.py)
                        └── playwright 操作
    """

    print("\n" + "=" * 50)
    print("异步函数链式调用演示")
    print("=" * 50)

    async def step3():
        """模拟最底层的异步操作"""
        await asyncio.sleep(0.1)
        return "Step 3 完成"

    async def step2():
        """中间层，调用底层"""
        print("  Step 2 开始")
        result = await step3()  # 等待底层完成
        print(f"  Step 2 收到: {result}")
        return f"Step 2 完成 ({result})"

    async def step1():
        """最上层，调用中间层"""
        print("Step 1 开始")
        result = await step2()  # 等待中间层完成
        print(f"Step 1 收到: {result}")
        return f"Step 1 完成 ({result})"

    final_result = await step1()
    print(f"最终结果: {final_result}")

    print("""
关键理解：
1. 每个 async 函数返回的是一个 "协程对象"，不是实际结果
2. 必须用 await 才能获取实际结果
3. 调用链中的每一层都要 await，形成 "异步调用链"
4. 这种模式和同步代码的调用链类似，只是加了 async/await
""")


# ============================================================================
# 第五部分：动手实验
# ============================================================================
"""
📝 实验任务：

1. 运行代码，观察 async with 嵌套的执行顺序
2. 在 step2 中故意抛出异常，观察清理是否仍然执行
3. 尝试不使用 try-finally，模拟资源泄露的情况
4. 思考：为什么 page 不需要显式 close？

提示：
- asyncio.run() 会处理顶层的异常，但程序中的资源需要你自己清理
"""

async def main():
    await nested_async_with_demo()
    await error_handling_demo()
    await project_pattern_analysis()
    await async_chain_demo()


if __name__ == "__main__":
    asyncio.run(main())


# ============================================================================
# 第六部分：关键问题自测
# ============================================================================
"""
🤔 思考问题：

1. 为什么 browser 和 context 需要手动 close，而 page 不需要？
   答案：page 是 context 的子资源，context.close() 会自动清理所有 page。
         browser 和 context 是独立的顶层资源，需要显式关闭。

2. async with 和 try-finally 可以互换吗？
   答案：不可以完全互换。async with 用于支持上下文管理协议的对象
         (有 __aenter__ 和 __aexit__ 方法)，而 try-finally 是通用模式。
         项目中 playwright 用 async with，browser 用 try-finally。

3. 如果忘记 await 会怎样？
   答案：会得到一个协程对象而不是实际结果，且不会真正执行操作。
         严重时会导致 "never awaited" 警告或运行时错误。

4. 项目中的 Stealth().use_async() 做了什么？
   答案：这是一个插件，它包装了 playwright，
         在启动时注入反检测脚本，让浏览器更难被识别为自动化工具。
"""
