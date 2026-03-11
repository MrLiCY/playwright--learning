"""
Lesson 2: 并发执行 - 异步的真正威力
====================================

学习目标：
1. 理解什么是并发（Concurrency）
2. 学会同时处理多个页面/任务
3. 理解 asyncio.gather 的作用
4. 对比：同步串行 vs 异步并发
"""

import asyncio
import time
from playwright.async_api import async_playwright


# ============================================================================
# 第一部分：串行执行（低效）
# ============================================================================

async def scrape_one_page(p, url: str, delay: int = 1) -> str:
    """
    模拟抓取一个页面的异步函数

    Args:
        p: playwright 对象
        url: 要抓取的 URL
        delay: 模拟页面加载延迟（秒）

    Returns:
        页面标题
    """
    print(f"[开始] 抓取 {url}")

    browser = await p.chromium.launch()
    page = await browser.new_page()

    # 模拟页面加载（实际使用时会自动等待页面加载）
    await page.goto(url)
    await asyncio.sleep(delay)  # 模拟额外等待

    title = await page.title()
    await browser.close()

    print(f"[完成] {url} -> 标题: {title}")
    return title


async def sequential_scrape(urls: list[str]):
    """
    串行抓取：一个接一个地执行

    时间成本：delay1 + delay2 + delay3 + ...
    """
    print("\n" + "=" * 50)
    print("串行执行模式（低效）")
    print("=" * 50)

    start_time = time.time()

    async with async_playwright() as p:
        results = []
        for url in urls:
            # 等待每个任务完成才继续下一个
            result = await scrape_one_page(p, url, delay=2)
            results.append(result)

    elapsed = time.time() - start_time
    print(f"\n串行执行耗时: {elapsed:.2f} 秒")
    return results


# ============================================================================
# 第二部分：并发执行（高效）
# ============================================================================

async def concurrent_scrape(urls: list[str]):
    """
    并发抓取：同时执行多个任务

    时间成本：max(delay1, delay2, delay3, ...)
    """
    print("\n" + "=" * 50)
    print("并发执行模式（高效）")
    print("=" * 50)

    start_time = time.time()

    async with async_playwright() as p:
        # asyncio.gather 同时启动所有任务
        # 关键：所有任务在 "等待 I/O" 时可以相互让出 CPU
        tasks = [scrape_one_page(p, url, delay=2) for url in urls]
        results = await asyncio.gather(*tasks)

    elapsed = time.time() - start_time
    print(f"\n并发执行耗时: {elapsed:.2f} 秒")
    return results


# ============================================================================
# 第三部分：理解 asyncio.gather
# ============================================================================
"""
asyncio.gather(*aws) 详解：

1. 接受多个 awaitable 对象（协程）
2. 同时调度它们执行
3. 返回一个列表，包含所有结果（按传入顺序）
4. 等待所有任务完成才返回

重要特性：
- 如果某个任务出错，默认会取消其他任务
- 可以设置 return_exceptions=True 来捕获异常而不中断
"""

async def demo_gather_behavior():
    """演示 gather 的行为"""

    async def task(name: str, delay: float):
        print(f"  任务 {name} 开始")
        await asyncio.sleep(delay)  # 模拟 I/O 等待
        print(f"  任务 {name} 完成")
        return f"结果-{name}"

    print("\n" + "=" * 50)
    print("asyncio.gather 行为演示")
    print("=" * 50)

    # 创建 3 个任务，分别耗时 0.3, 0.2, 0.1 秒
    results = await asyncio.gather(
        task("A", 0.3),
        task("B", 0.2),
        task("C", 0.1),
    )

    print(f"所有结果: {results}")
    print("注意：任务完成的顺序是 C(0.1s) -> B(0.2s) -> A(0.3s)")
    print("但结果列表的顺序仍然是 [A, B, C]")


# ============================================================================
# 第四部分：项目的实际应用
# ============================================================================
"""
在你的爬虫项目中，asyncio.gather 的潜在应用场景：

1. 同时抓取多个页面（批量任务）
2. 一个页面中同时执行多个独立的 JavaScript 查询
3. 同时处理多个不同的检查条件

但注意：Browser 实例不是线程安全的，每个并发任务应该有自己的 browser 或 page
"""


# ============================================================================
# 第五部分：动手实验
# ============================================================================
"""
📝 实验任务：

1. 运行程序，观察串行和并发的时间差异
2. 修改 concurrent_scrape 中的 delay 值，看看对总时间的影响
3. 尝试在 concurrent_scrape 中创建多个 browser，对比单个 browser 多个 page

预期结果：
- 串行：3 个任务 × 2 秒 = 约 6 秒
- 并发：3 个任务同时执行 = 约 2 秒（取决于最慢的任务）
"""

async def main():
    test_urls = [
        "https://baidu.com",
        "https://www.google.com/",
        "https://www.gov.cn/zhuanti/2026nztj/2026qglh/yw/202603/content_7061992.htm",
    ]

    # 演示 gather 行为
    await demo_gather_behavior()

    # 串行执行
    await sequential_scrape(test_urls)

    # 并发执行
    await concurrent_scrape(test_urls)


if __name__ == "__main__":
    asyncio.run(main())


# ============================================================================
# 第六部分：关键问题自测
# ============================================================================
"""
🤔 思考问题：

1. 为什么并发执行更快？
   答案：因为在等待网络响应（I/O）时，程序可以去执行其他任务，
         而不是空等。CPU 利用率更高。

2. asyncio.gather 和直接 for + await 有什么区别？
   答案：gather 是"同时启动"所有任务，for+await 是"一个一个"执行。
         类比：gather 像是同时煮三壶水，for+await 像是煮完一壶再煮下一壶。

3. 如果并发任务中有一个出错了会怎样？
   答案：默认情况下，gather 会取消其他未完成的任务并抛出异常。
         可以设置 return_exceptions=True 来捕获所有异常。

4. 项目的 base_scrape 里为什么不用 gather？
   答案：因为这是一个单页面抓取函数，内部没有并发的需求。
         但如果要实现批量抓取功能，就可以用 gather 来并发多个 base_scrape 调用。
"""
