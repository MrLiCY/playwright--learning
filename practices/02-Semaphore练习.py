import asyncio
import time

async def fetch_with_limit(name, delay, semaphore):
    """使用信号量"""
    async with semaphore:
        print(f"{name} 开始执行")
        await asyncio.sleep(delay)
        print(f"{name} 执行完成")
        return f"{name} 的数据"

async def batch_fetch(configs, max_concurrent=2):
    """批量抓取，限制并发数"""
    semaphore = asyncio.Semaphore(max_concurrent)

    # 创建任务， 每个任务都使用同一个 semaphore
    tasks = [
        fetch_with_limit(**configs, semaphore=semaphore) 
        for configs in configs
    ]

    results = await asyncio.gather(*tasks)
    return results

# 测试
configs = [
    {"name": "用户数据", "delay": 1},
    {"name": "订单数据", "delay": 1},
    {"name": "商品数据", "delay": 1},
    {"name": "库存数据", "delay": 1},
    {"name": "日志数据", "delay": 1},
]

async def main():
    print("限制最多2个并发")
    print("="*40)
    start = time.time()
    results = await batch_fetch(configs, max_concurrent=5)
    print(f"总耗时:{time.time() - start:.2f}秒")

if __name__ == "__main__":
    asyncio.run(main())