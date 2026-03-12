# Playwright 学习总结 - 第三课

> 学习日期: 2026-03-12
> 学习内容: 元素获取后的处理操作

---

## 📚 学习内容概览

### 1. 元素文本与属性操作
- ✅ 获取元素文本内容 (`inner_text()`, `text_content()`)
- ✅ 获取元素属性 (`get_attribute()`)
- ✅ 获取输入框的值 (`input_value()`)

### 2. 元素状态检查
- ✅ 检查元素可见性 (`is_visible()`)
- ✅ 检查元素是否可编辑 (`is_editable()`)
- ✅ 检查元素是否存在 (`count() > 0`)

### 3. 多元素处理
- ✅ 获取元素数量 (`count()`)
- ✅ 遍历元素列表 (`nth()`)
- ✅ 获取所有匹配元素 (`all()`)

### 4. 页面内容获取
- ✅ 获取页面完整 HTML (`page.content()`)
- ✅ 获取元素 HTML (`inner_html()`)

---

## 🎯 第三课: 元素获取后的处理

### 已练习内容回顾

```python
from playwright.sync_api import sync_playwright

def main():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.baidu.com")

    # 1. 获取元素文本
    news_link = page.locator("text=新闻").first
    news_text = news_link.inner_text()
    print(f"文本内容: {news_text}")

    # 2. 获取元素属性
    search_box = page.locator("#chat-textarea")
    placeholder = search_box.get_attribute("placeholder")
    print(f"占位符: {placeholder}")

    # 3. 遍历多个元素
    nav_links = page.locator("a.mnav")
    for i in range(nav_links.count()):
        link = nav_links.nth(i)
        print(f"链接 {i+1}: {link.inner_text()}")

    # 4. 检查元素状态
    print(f"是否可见: {search_box.is_visible()}")
    print(f"是否可编辑: {search_box.is_editable()}")

    # 5. 获取页面HTML
    html = page.content()
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
```

---

## 📖 元素内容获取方法详解

### 1. 获取文本内容的三种方式

```python
element = page.locator("#example")

# inner_text() - 获取可见文本（考虑 CSS 样式）
text = element.inner_text()
# 特点：忽略 display:none 的元素，返回渲染后的文本

# text_content() - 获取所有文本内容
text = element.text_content()
# 特点：获取完整的文本内容，包括隐藏的元素

# input_value() - 获取输入框的值
value = element.input_value()
# 特点：专门用于 input、textarea 等表单元素
```

**对比示例：**

```python
page.goto("data:text/html,<div id='test'>可见文字<span style='display:none'>隐藏文字</span></div>")

element = page.locator("#test")
print(element.inner_text())     # 输出: "可见文字"
print(element.text_content())   # 输出: "可见文字隐藏文字"
```

---

### 2. 获取元素属性

```python
element = page.locator("a#link")

# 获取单个属性
href = element.get_attribute("href")
title = element.get_attribute("title")
data_id = element.get_attribute("data-id")  # 自定义属性

# 获取所有属性（需要 evaluate）
all_attrs = element.evaluate("el => Object.fromEntries([...el.attributes].map(a => [a.name, a.value]))")
print(all_attrs)  # {'id': 'link', 'href': '...', 'class': '...'}
```

**常用属性获取：**

```python
# 链接相关
link = page.locator("a.external")
url = link.get_attribute("href")           # 链接地址
target = link.get_attribute("target")      # 打开方式 (_blank, _self)

# 图片相关
img = page.locator("img.logo")
src = img.get_attribute("src")             # 图片地址
alt = img.get_attribute("alt")             # 替代文本

# 表单相关
input_box = page.locator("input#username")
input_type = input_box.get_attribute("type")       # 输入类型 (text, password, email)
placeholder = input_box.get_attribute("placeholder")  # 占位符
required = input_box.get_attribute("required")     # 是否必填
max_length = input_box.get_attribute("maxlength")  # 最大长度
```

---

### 3. 获取元素 HTML

```python
element = page.locator("#container")

# inner_html() - 获取元素内部的 HTML
inner = element.inner_html()
# 结果: "<p>段落1</p><p>段落2</p>"

# outer_html() - 获取元素自身的 HTML（包含标签）
outer = element.evaluate("el => el.outerHTML")
# 结果: "<div id='container'><p>段落1</p><p>段落2</p></div>"
```

---

## 🔍 元素状态检查全解

### 1. 可见性相关

```python
element = page.locator("#target")

# is_visible() - 是否可见（在 DOM 中且 display 不为 none）
is_visible = element.is_visible()

# is_hidden() - 是否隐藏
is_hidden = element.is_hidden()

# 注意：元素必须存在才能调用这些方法
count = element.count()
if count > 0 and element.is_visible():
    print("元素存在且可见")
```

### 2. 交互状态

```python
element = page.locator("#input")

# is_enabled() - 是否启用（没有被 disabled）
is_enabled = element.is_enabled()

# is_disabled() - 是否禁用
is_disabled = element.is_disabled()

# is_editable() - 是否可编辑（启用、可见、非只读）
is_editable = element.is_editable()

# is_checked() - 复选框/单选框是否选中（仅用于 input[type=checkbox|radio]）
checkbox = page.locator("#agree")
is_checked = checkbox.is_checked()
```

### 3. 完整状态检查示例

```python
def check_element_state(page, selector):
    """完整检查元素状态"""
    locator = page.locator(selector)

    if locator.count() == 0:
        return {"exists": False}

    element = locator.first
    return {
        "exists": True,
        "visible": element.is_visible(),
        "enabled": element.is_enabled(),
        "editable": element.is_editable(),
        "checked": element.is_checked() if element.get_attribute("type") in ["checkbox", "radio"] else None,
    }

# 使用
state = check_element_state(page, "#submit-btn")
print(state)
# {'exists': True, 'visible': True, 'enabled': True, 'editable': False, 'checked': None}
```

---

## 📋 多元素处理方法

### 1. 获取元素数量

```python
items = page.locator(".list-item")
count = items.count()
print(f"共有 {count} 个列表项")
```

### 2. 遍历元素

```python
# 方式1：使用 nth() 遍历
items = page.locator(".list-item")
for i in range(items.count()):
    item = items.nth(i)
    title = item.locator(".title").inner_text()
    price = item.locator(".price").inner_text()
    print(f"{i+1}. {title} - {price}")

# 方式2：使用 all() 获取所有元素句柄
handles = items.all()  # 返回 Locator 列表
for handle in handles:
    print(handle.inner_text())

# 方式3：使用 all_inner_texts() 获取所有文本
texts = items.all_inner_texts()  # 返回字符串列表
print(texts)  # ['文本1', '文本2', '文本3']

# 方式4：使用 all_text_contents() 获取所有文本内容
texts = items.all_text_contents()  # 包含隐藏文本
```

### 3. 筛选特定元素

```python
# 使用 filter() 筛选
all_buttons = page.locator("button")
# 筛选可见的按钮
visible_buttons = all_buttons.filter(visible=True)
# 筛选包含特定文本的按钮
submit_buttons = all_buttons.filter(has_text="提交")
# 筛选包含子元素的按钮
danger_buttons = all_buttons.filter(has=page.locator(".icon-danger"))
```

### 4. 获取第一个/最后一个元素

```python
items = page.locator(".list-item")

first = items.first      # 第一个元素
last = items.last        # 最后一个元素
nth_3 = items.nth(2)     # 第3个元素（从0开始）
```

---

## 🧮 元素尺寸和位置

### 1. 获取元素边界框

```python
element = page.locator("#box")
bounding_box = element.bounding_box()

print(bounding_box)
# {
#     'x': 100.0,      # 左上角 x 坐标
#     'y': 200.0,      # 左上角 y 坐标
#     'width': 300.0,  # 宽度
#     'height': 150.0  # 高度
# }
```

### 2. 完整示例：获取元素位置和尺寸

```python
def get_element_info(page, selector):
    """获取元素的完整信息"""
    element = page.locator(selector)

    if element.count() == 0:
        return None

    box = element.bounding_box()
    return {
        "selector": selector,
        "text": element.inner_text(),
        "visible": element.is_visible(),
        "position": {"x": box["x"], "y": box["y"]},
        "size": {"width": box["width"], "height": box["height"]},
        "center": {
            "x": box["x"] + box["width"] / 2,
            "y": box["y"] + box["height"] / 2
        }
    }

info = get_element_info(page, "#login-btn")
print(info)
```

---

## 🖱️ 进阶：JavaScript 执行获取信息

### 1. 使用 evaluate 获取自定义信息

```python
element = page.locator("#custom-element")

# 获取元素的计算样式
computed_style = element.evaluate("el => getComputedStyle(el).color")
print(f"文字颜色: {computed_style}")

# 获取元素的子元素数量
child_count = element.evaluate("el => el.children.length")
print(f"子元素数量: {child_count}")

# 获取元素的父元素标签名
parent_tag = element.evaluate("el => el.parentElement?.tagName")
print(f"父元素: {parent_tag}")

# 获取元素在页面中的滚动位置
scroll_info = element.evaluate("""
    el => {
        const rect = el.getBoundingClientRect();
        return {
            top: rect.top + window.scrollY,
            left: rect.left + window.scrollX
        };
    }
""")
```

### 2. 在页面上执行 JavaScript

```python
# 获取页面标题
title = page.evaluate("() => document.title")

# 获取页面 URL
current_url = page.evaluate("() => window.location.href")

# 获取页面滚动位置
scroll_pos = page.evaluate("() => ({ x: window.scrollX, y: window.scrollY })")

# 获取所有 cookie
cookies = page.evaluate("() => document.cookie")

# 获取 localStorage
local_storage = page.evaluate("() => JSON.parse(JSON.stringify(localStorage))")

# 获取 sessionStorage
session_storage = page.evaluate("() => JSON.parse(JSON.stringify(sessionStorage))")
```

---

## 💾 页面内容保存

### 1. 保存页面 HTML

```python
# 获取完整 HTML
html = page.content()

# 保存到文件
with open("page.html", "w", encoding="utf-8") as f:
    f.write(html)
```

### 2. 保存截图

```python
# 页面截图
page.screenshot(path="page.png")

# 全页面截图（包含滚动区域）
page.screenshot(path="full_page.png", full_page=True)

# 元素截图
element = page.locator("#chart")
element.screenshot(path="element.png")

# 指定区域截图
page.screenshot(path="region.png", clip={"x": 0, "y": 0, "width": 800, "height": 600})
```

### 3. 保存 PDF（仅 Chromium）

```python
page.pdf(path="page.pdf")
page.pdf(path="page.pdf", format="A4", print_background=True)
```

---

## 🔥 实战技巧

### 技巧1：等待元素满足特定条件

```python
# 等待元素可见
page.locator("#result").wait_for(state="visible", timeout=5000)

# 等待元素隐藏
page.locator("#loading").wait_for(state="hidden", timeout=5000)

# 等待元素从 DOM 中移除
page.locator("#temp").wait_for(state="detached")

# 等待元素附加到 DOM
page.locator("#new-element").wait_for(state="attached")
```

### 技巧2：智能等待内容变化

```python
# 等待元素文本包含特定内容
page.locator("#status").filter(has_text="加载完成").wait_for()

# 等待元素数量变化
page.wait_for_function("() => document.querySelectorAll('.item').length >= 10")
```

### 技巧3：表单数据提取

```python
def extract_form_data(page, form_selector):
    """提取表单中所有输入框的值"""
    form_data = {}
    inputs = page.locator(f"{form_selector} input, {form_selector} textarea, {form_selector} select")

    for i in range(inputs.count()):
        input_el = inputs.nth(i)
        name = input_el.get_attribute("name") or input_el.get_attribute("id")
        if name:
            value = input_el.input_value()
            form_data[name] = value

    return form_data

# 使用
data = extract_form_data(page, "#user-form")
print(data)  # {'username': 'john', 'email': 'john@example.com'}
```

### 技巧4：表格数据提取

```python
def extract_table_data(page, table_selector):
    """提取表格数据为列表字典"""
    table = page.locator(table_selector)

    # 获取表头
    headers = table.locator("thead th, tr:first-child td").all_inner_texts()

    # 获取数据行
    rows = table.locator("tbody tr, tr:not(:first-child)")
    data = []

    for i in range(rows.count()):
        row = rows.nth(i)
        cells = row.locator("td").all_inner_texts()
        row_data = dict(zip(headers, cells))
        data.append(row_data)

    return data

# 使用
table_data = extract_table_data(page, "#data-table")
for row in table_data:
    print(row)
```

---

## ⚠️ 常见陷阱和解决方案

### 陷阱1：元素不存在时调用方法

```python
# ❌ 错误：直接调用可能导致异常
text = page.locator("#missing").inner_text()  # TimeoutError!

# ✅ 正确：先检查存在性
locator = page.locator("#missing")
if locator.count() > 0:
    text = locator.inner_text()
else:
    text = None
```

### 陷阱2：多个元素匹配时

```python
# ❌ 错误：默认操作第一个，可能不是想要的
page.locator("button").click()  # 点击第一个按钮

# ✅ 正确：明确指定或使用 filter
code = page.locator("button").filter(has_text="确认").click()
# 或
page.locator("button[type='submit']").click()
```

### 陷阱3：动态加载内容

```python
# ❌ 错误：立即获取可能为空
items = page.locator(".dynamic-item").all_inner_texts()  # 可能为空列表

# ✅ 正确：先等待元素出现
page.wait_for_selector(".dynamic-item", timeout=5000)
items = page.locator(".dynamic-item").all_inner_texts()
```

---

## 📚 练习题建议

1. **网页信息采集器**
   - 访问一个新闻网站
   - 提取所有文章标题和链接
   - 保存到 JSON 文件

2. **表单数据备份**
   - 自动填写表单
   - 提取所有输入值
   - 保存为配置文件

3. **商品价格监控**
   - 访问电商网站
   - 提取商品名称和价格
   - 检测价格变化

4. **页面结构分析**
   - 分析页面所有链接
   - 统计各类元素数量
   - 生成页面结构报告

---

## 🎯 下一步学习

第四课预告：实战技巧和高级应用
- 网络请求拦截和监听
- 文件上传和下载处理
- 弹窗和对话框处理
- 多标签页和 iframe 操作

---

**第三课学习完成！继续加油，掌握元素操作是爬虫开发的基础！** 🚀

---

*生成日期: 2026-03-12*
*学习者: lichenyang*
*学习进度: 第三课完成*
