import asyncio
import time
from playwright.async_api import async_playwright

async def get_data(name, delay):
    print(f"{name} 开始")
    await asyncio.sleep(delay)  # 模拟 I/O 操作
    print(f"{name} 完成, 耗时 {delay} 秒")
    return f"{name} 的数据"

async def start_tasks(configs):
    tasks = [fetch_data(**config) for config in configs]
    results =  await asyncio.gather(*tasks)
    return results

async def fetch_data(name, delay):
    print(f"{name} 开始")
    await asyncio.sleep(delay)  # 模拟 I/O 操作
    print(f"{name} 完成")
    return f"{name} 的数据"

async def main():

    # print("开始串行执行")
    # print("\n" + "=" * 50)
    # start = time.time()
    # await fetch_data("A", 3)
    # await fetch_data("B", 2)
    # await fetch_data("C", 1)
    # elapsed = time.time() - start
    # print(f"总耗时: {elapsed:.2f} 秒")
    # print("\n" + "=" * 50)

    # print("开始并行执行")
    # print("\n" + "=" * 50)
    # start_time = time.time()
    # results = await asyncio.gather(
    #     fetch_data("A", 3),
    #     fetch_data("B", 2),
    #     fetch_data("C", 1)
    # )
    # elapsed = time.time() - start_time
    # print(f"总耗时: {elapsed:.2f} 秒")
    # print("\n" + "=" * 50)
    # print(f"结果: {results}")

    configs = [
        {"name": "用户数据", "delay": 1},
        {"name": "订单数据", "delay": 2},
        {"name": "商品数据", "delay": 1}
    ]

    start = time.time()
    results = await start_tasks(configs)
    print(f"总耗时: {time.time() - start:.2f} 秒")
    print(f"结果: {results}")



if __name__ == "__main__":
    asyncio.run(main())