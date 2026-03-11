"""
Lesson 1: 同步 vs 异步 Playwright 基础对比
===========================================

学习目标：
1. 理解同步和异步代码的根本区别
2. 认识 Python 异步的三个关键字：async/await/async with
3. 对比同一段逻辑的同步和异步写法
"""

# ============================================================================
# 第一部分：同步代码（你熟悉的写法）
# ============================================================================
"""
同步 Playwright 特点：
- 使用 from playwright.sync_api import sync_playwright
- 代码从上到下顺序执行，每一步都等待完成才继续
- 简单直观，但效率较低（等待网络请求时 CPU 空闲）

同步代码示例：
"""

def sync_example():
    """这是一个同步函数的示例结构"""
    # from playwright.sync_api import sync_playwright
    #
    # with sync_playwright() as p:
    #     browser = p.chromium.launch()
    #     page = browser.new_page()
    #     page.goto("https://example.com")  # 阻塞等待页面加载
    #     title = page.title()              # 阻塞等待获取标题
    #     print(title)
    #     browser.close()
    pass


# ============================================================================
# 第二部分：异步代码（项目使用的写法）
# ============================================================================
"""
异步 Playwright 特点：
- 使用 from playwright.async_api import async_playwright
- 使用 async def 定义异步函数
- 使用 await 等待异步操作完成
- 使用 async with 管理异步上下文
- 可以在等待 I/O 时执行其他任务

异步代码示例：
"""

import asyncio
from playwright.async_api import async_playwright


async def async_basic_example():
    """
    最基础的异步 Playwright 示例

    关键概念：
    1. async def - 定义这是一个异步函数（协程）
    2. await - 等待异步操作完成，但不会阻塞整个程序
    3. async with - 异步上下文管理器，自动处理资源的进入和退出
    """
    # async with 会自动处理资源的清理
    # 等同于：
    #   playwright = await async_playwright().start()
    #   try:
    #       ... 执行代码 ...
    #   finally:
    #       await playwright.stop()

    async with async_playwright() as p:
        # await 表示"等待这个操作完成"，但会让出控制权
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # goto 是网络 I/O 操作，await 让程序可以在此期间做其他事
        await page.goto("https://baidu.com")

        title = await page.title()
        print(f"页面标题: {title}")

        await browser.close()


# ============================================================================
# 第三部分：动手实验
# ============================================================================
"""
📝 实验任务：

1. 先运行这个基础示例，观察输出
2. 注释掉某些 await，看看会发生什么错误
3. 尝试同时打开两个页面（先不要看 Lesson 2）

运行方法：
    cd ~/Desktop/playwright-learning
    python lesson1_basics.py
"""

async def main():
    """主函数 - 程序的入口点"""
    print("=" * 50)
    print("开始执行异步 Playwright 示例")
    print("=" * 50)

    await async_basic_example()

    print("=" * 50)
    print("示例执行完成")
    print("=" * 50)


# Python 异步程序的入口点标准写法
if __name__ == "__main__":
    # asyncio.run() 会创建一个事件循环并运行主协程
    asyncio.run(main())


# ============================================================================
# 第四部分：关键问题自测
# ============================================================================
"""
🤔 思考问题：

1. 如果不写 await page.goto()，会发生什么？
   答案：返回的是一个"协程对象"而不是真正的结果，页面不会实际跳转

2. 如果不写 async with，如何手动管理 playwright 生命周期？
   答案：需要手动 start() 和 stop()，且 stop() 也需要 await

3. 同步的 with 和异步的 async with 有什么区别？
   答案：async with 会调用异步的 __aenter__ 和 __aexit__ 方法

4. 为什么异步代码里每个操作都要 await？
   答案：因为 Playwright 的所有 I/O 操作都是异步的，
         浏览器操作本质上是"发送命令->等待响应"的网络通信
"""
