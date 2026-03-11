from playwright.sync_api import sync_playwright
import time

def main():
    print("开始练习元素定位。。。")

    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.baidu.com")

    # #练习1:使用css选择器id定位搜索框
    # print("练习1:使用css选择器id定位搜索框")
    # search_box_id = page.locator("#chat-textarea").first
    # search_box_id.fill("playwright学习路线")
    # print("输入完成，准备按回车提交")

    # page.wait_for_timeout(1000)  # 等待1秒看输入效果

    # # 直接按回车键提交，避免按钮可见性问题
    # search_box_id.press("Enter")
    # print("已按回车键提交")

    # page.wait_for_timeout(3000)  # 等待3秒看搜索效果

    # # 练习2:清空并重新搜索
    # print("练习2:清空输入框并开始新的搜索")
    # page.wait_for_timeout(1000)  # 等待页面稳定

    # # 重新定位当前可见的输入框
    # visible_textarea = page.locator("#chat-textarea").filter(visible=True)
    # visible_textarea.clear()
    # print("输入框已清空")

    # page.wait_for_timeout(500)
    # visible_textarea.fill("Python教程")
    # print("新的搜索内容已输入")

    # page.wait_for_timeout(1000)
    # visible_textarea.press("Enter")
    # print("第二次搜索已提交")

    # page.wait_for_timeout(3000)  # 等待第二次搜索结果

    # 练习3:使用css选择器class定位搜索框
    # print("使用css选择器class定位搜索框")
    # search_box_class = page.locator(".chat-input-textarea").filter(visible=True)
    # search_box_class.fill("Playwright教程")
    # print("输入完成，准备按回车提交")
    # search_box_class.press("Enter")
    # print("已按回车键提交")
    # page.wait_for_timeout(5000)
    # visible_textarea = page.locator(".chat-input-textarea").filter(visible=True)
    # visible_textarea.clear()
    # print("输入框已清空")
    # page.wait_for_timeout(500)
    # page.goto("https://www.baidu.com")

    # # 练习4:根据属性进行定位
    # search_box_attribute = page.locator("[class='mnav c-font-normal c-color-t']").filter(visible=True).first
    # search_box_attribute.click()
    # print("点击了百度首页的导航栏")
    # page.wait_for_timeout(3000)  # 等待3秒看点击效果
    # page.goto("https://www.baidu.com")  # 返回首页
    # search_list = page.locator("[data-ai-placeholder]")
    # print("根据属性定位到的元素数量:", search_list.count())
    # page.bring_to_front()  # 将浏览器窗口置于前台

    # # 练习5:使用文本内容定位元素
    # print("练习5:使用文本内容定位元素")
    # news_link = page.locator("text=新闻").first
    # print("找到新闻链接，准备点击")
    # news_link.click()
    # print("已点击新闻链接")
    # page.wait_for_timeout(3000)  # 等待3秒看点击效果
    # page.bring_to_front()  # 将浏览器窗口置于前台

    # # 练习5.2: 文本包含（正则表达式）
    # print("练习5.2:文本包含匹配")
    # # 匹配包含"百度"的文本元素
    # baidu_elements = page.locator("text=/百度.*/")
    # print(f"包含'百度'的元素数量: {baidu_elements.count()}")

    # print("练习5.3:组合文本")
    # tieba_link = page.locator(".mnav").filter(has_text="贴吧")
    # print("找到贴吧链接，准备点击")
    # tieba_link.click()
    # print("已点击贴吧链接")
    # page.wait_for_timeout(3000)  # 等待3秒看点击效果
    # page.bring_to_front()  # 将浏览器窗口置于前台

    # 练习6:使用xpath定位
    # print("练习6:使用xpath通过属性去定位")
    # xpath_input = page.locator("xpath=//textarea[@id='chat-textarea']").filter(visible=True).first
    # xpath_input.fill("使用XPath定位元素")
    # print("xpath通过class去定位")
    # xpath_input = page.locator("xpath=//textarea[contains(@class, 'chat-input-textarea')]").filter(visible=True)
    # xpath_input.clear()
    # page.wait_for_timeout(500)
    # xpath_input.fill("使用XPath通过class定位元素")
    # page.wait_for_timeout(1000)
    # page.goto("https://www.baidu.com") # 返回首页
    # print("xpath通过层级关系定位")
    # page.wait_for_timeout(1000)
    # news_link = page.locator("xpath=//div[@class='s-top-left-new s-isindex-wrap']/a[contains(text(), '新闻')]").first
    # news_link.click()
    # page.bring_to_front()  # 将浏览器窗口置于前台

    # 练习7:使用css组合选择器
    print("练习7:使用标签+属性组合")
    news_link = page.locator("a[href='http://news.baidu.com']").first
    print("找到新闻链接，准备点击")
    news_link.click()
    print("已点击新闻链接")
    page.wait_for_timeout(3000)  # 等待3秒看点击效果
    page.bring_to_front()  # 将浏览器窗口置于前台
    print("练习7.2:使用标签+class组合")
    search_box = page.locator("textarea.chat-input-textarea").filter(visible=True).first
    search_box.fill("使用标签+class组合定位元素")


    # 保持程序运行，直到你按回车
    print("按回车键退出程序...")
    input()
 


if __name__ == "__main__":
    main()

        