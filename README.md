# Playwright 异步学习指南

本项目根据 `playwright-server` 的代码实践，系统性地教授异步 Playwright 编程。

---

## 学习目标

完成本教程后，你将能够：
1. 理解项目中所有异步代码的含义
2. 区分同步和异步 Playwright 的写法
3. 正确使用 `async`/`await`/`async with`
4. 理解项目的完整数据流
5. 编写和调试自己的异步爬虫代码

---

## 课程大纲

### Lesson 1: 基础对比 (`lesson1_basics.py`)
**核心概念：**
- `async def` - 定义异步函数（协程）
- `await` - 等待异步操作完成，让出控制权
- `async with` - 异步上下文管理器

**动手实验：**
```bash
cd ~/Desktop/playwright-learning
python lesson1_basics.py
```

**思考问题：**
- 如果不写 `await` 会发生什么？
- 同步的 `with` 和异步的 `async with` 有什么区别？

---

### Lesson 2: 并发执行 (`lesson2_concurrency.py`)
**核心概念：**
- `asyncio.gather()` - 同时执行多个任务
- 串行 vs 并发的时间差异
- 任务的调度与执行

**动手实验：**
```bash
python lesson2_concurrency.py
```

**思考问题：**
- 为什么并发执行更快？
- `gather` 和 `for + await` 的区别是什么？

---

### Lesson 3: 项目模式 (`lesson3_project_patterns.py`)
**核心概念：**
- `async with` 的嵌套结构
- `try-finally` 资源清理
- 异步函数的链式调用

**项目代码结构解析：**
```python
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
```

---

### Lesson 4: 实用技术 (`lesson4_practical_techniques.py`)
**核心概念：**
- `page.route()` - 异步路由拦截
- `page.wait_for_selector()` - 等待元素
- `page.evaluate()` - 执行 JavaScript

**项目应用场景：**
- 拦截广告域名
- 等待动态内容加载
- 获取页面 JavaScript 计算的值

---

### Lesson 5: 项目整合 (`lesson5_project_integration.py`)
**核心概念：**
- 完整的数据流分析
- FastAPI 中的异步处理
- 调试技巧和常见错误

---

## 快速参考卡片

### 同步 vs 异步对比

| 同步代码 | 异步代码 |
|---------|---------|
| `from playwright.sync_api import sync_playwright` | `from playwright.async_api import async_playwright` |
| `with sync_playwright() as p:` | `async with async_playwright() as p:` |
| `browser = p.chromium.launch()` | `browser = await p.chromium.launch()` |
| `page.goto(url)` | `await page.goto(url)` |
| `title = page.title()` | `title = await page.title()` |

### 关键关键字

```python
# 定义异步函数
async def my_function():
    pass

# 等待异步操作
result = await some_async_function()

# 异步上下文管理器
async with async_playwright() as p:
    pass

# 同时运行多个任务
results = await asyncio.gather(task1(), task2(), task3())

# 运行主协程
asyncio.run(main())
```

### 项目中的标准结构

```python
async def scrape_page(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            context = await browser.new_context()
            try:
                page = await context.new_page()

                # 拦截广告
                await page.route("**/*", lambda route: (
                    route.abort() if "ads" in route.request.url
                    else route.continue_()
                ))

                # 导航并等待
                await page.goto(url, wait_until="load")
                await page.wait_for_timeout(1000)

                # 获取内容
                content = await page.content()
                title = await page.title()

                return {"title": title, "content": content}

            finally:
                await context.close()
        finally:
            await browser.close()
```

---

## 常见错误速查

| 错误 | 原因 | 解决方法 |
|-----|------|---------|
| `RuntimeError: Event loop is closed` | 在 loop 关闭后使用 | 确保所有 await 在 loop 关闭前完成 |
| `RuntimeWarning: coroutine was never awaited` | 忘记 await | 检查 async 函数调用前都有 await |
| `SyntaxError: 'await' outside async function` | 在非 async 函数中使用 await | 将函数改为 async def |
| `TimeoutError: Navigation timeout exceeded` | 页面加载超时 | 增加 timeout 或检查网络 |

---

## 学习建议

1. **先理解同步版本**：如果你熟悉同步 Playwright，对比学习会更轻松
2. **动手实验**：每个课程都有实验任务，一定要自己敲一遍代码
3. **调试模式**：运行时使用 `asyncio.run(main(), debug=True)` 获取更多信息
4. **循序渐进**：不要跳过课程，异步概念是层层递进的

---

## 下一步

完成所有课程后，你可以：
1. 阅读项目中的 `app/policies/generic_policy.py`，理解完整实现
2. 尝试修改项目代码，添加一个新的抓取 policy
3. 实现批量抓取功能，使用 `asyncio.gather` 并发处理多个 URL
4. 学习 `asyncio.Semaphore` 来限制并发数

---

## 参考资源

- [Playwright Python Async API](https://playwright.dev/python/docs/api/class-playwright)
- [Python asyncio 文档](https://docs.python.org/3/library/asyncio.html)
- [FastAPI Async 指南](https://fastapi.tiangolo.com/async/)
错误内容
临时内容
