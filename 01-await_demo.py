import asyncio
import time

async def say_hello():
    print("Hello 开始")
    await asyncio.sleep(1)  # 模拟网络请求
    print("Hello 结束")
    return "Hello 的结果"

async def experiment_1():
    print("\n=== 实验 1: await 的作用===")
    print("错误写法\n")
    result = say_hello()  # 注意：这里没有 await！
    print(f"   得到的结果: {result}")
    print(f"   类型: {type(result)}")
    print("   ⚠️   注意：函数并没有真正执行！")
    print("正确写法\n")
    print("\n2. 正确写法（使用 await）：")
    result = await say_hello()  # 这里加了 await
    print(f"   得到的结果: {result}")
    print(f"   类型: {type(result)}")

async def task(name, delay):
    """模拟一个耗时的异步任务"""
    print(f'[{name}] 开始 （学要{delay}秒）')
    await asyncio.sleep(delay)  # 模拟耗时操作
    print(f'[{name}] 结束')
    return f'{name} 的结果'

async def experiment_2():
    print("\n=== 实验 2: 多任务并发执行 ===")
    print("1.串行执行")
    start = time.time()
    await task("任务1", 1)
    await task("任务2", 1)
    await task("任务3", 1)
    print(f" 总耗时：{time.time() - start:.2f}秒")

    print("\n2.并行执行")
    start = time.time()
    results = await asyncio.gather(
        task("任务1", 1),
        task("任务2", 1),
        task("任务3", 1)    
    )
    print(f'总耗时: {time.time() - start:.2f}秒')
    print(f'结果: {results}')

    
async def experiment_3():
    from playwright.async_api import async_playwright
    
    print("\n=== 实验3: Playwright 中的await ===\n")

    async with async_playwright() as p:
        print("1.Playwright 已启动")
        browser = await p.chromium.launch()
        print("2.浏览器已打开")
        page = await browser.new_page()
        print("3.新页面已创建")
        await page.goto("https://baidu.com")
        print("4.页面已加载")
        title = await page.title()
        print(f"5.页面标题: {title}")
        await browser.close()
        print("6.浏览器已关闭")


async def main():
    await experiment_1()
    await experiment_2()
    await experiment_3()

if __name__ == "__main__":
    asyncio.run(main())
    