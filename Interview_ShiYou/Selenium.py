from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
from selenium.webdriver.support.select import Select


# 通过备好的currency_code.txt实现货币代号到货币名称的转换
def get_currency_name(currency_code):
    currency_file = open('currency_code.txt', 'r', encoding='utf-8')
    for line in currency_file:
        name, code = line.strip().split(' ')
        if code == currency_code:
            currency_file.close()
            return name
    currency_file.close()
    return "未找到对应的货币名称"


# 在文件操作处增加异常处理
try:
    currency_file = open('currency_code.txt', 'r', encoding='utf-8')
    # 其他文件操作代码...
except FileNotFoundError:
    print("文件未找到")
except IOError:
    print("文件读取错误")

# 设置日期和货币代号
date = sys.argv[1]
currency_code = sys.argv[2]
currency_name = get_currency_name(currency_code)  # 通过自定义方法获取待查货币名称

# 创建浏览器实例
browser = webdriver.Chrome()  # 可以改浏览器，但要确保有对应的驱动
date_send = date[0:4] + '-' + date[4:6] + '-' + date[6:]  # 提取输入年份、月份、日期并转化为待输入

# 打开中国银行外汇牌价网站
url = "https://www.boc.cn/sourcedb/whpj/"
browser.get(url)

# 定位起始日期输入框并输入日期 （均通过id定位）
start_date = browser.find_element(By.ID, 'erectDate')  # Find the search box
start_date.send_keys(date_send)

end_date = browser.find_element(By.ID, 'nothing')  # Find the search box
end_date.send_keys(date_send)

# 定位货币代号输入框并输入代号 （通过id定位）
currency_input = browser.find_element(By.ID, "pjname")

# 使用 Select 对象来操作<select>元素
select = Select(currency_input)

# 根据货币名称找到对应的<option>并选择
select.select_by_visible_text(currency_name)

# 点击查询按钮 (查询按钮无id，通过XPATH来定位）
query_button = browser.find_element(By.XPATH, '//*[@id="historysearchform"]/div/table/tbody/tr/td[7]/input')
query_button.click()

time.sleep(5)  # 等待页面加载完成，可以根据实际网速调整等待时间

# 获取现汇卖出价
exchange_rate = browser.find_element(By.XPATH, '/html/body/div/div[4]/table/tbody/tr[2]/td[4]').text

# 将爬取到的数据写入文件result.txt (这里模式'a'为追加写，也可以改为'w'，覆盖写）
with open("result.txt", "a") as file:
    file.write(f"日期：{date}, 货币代号：{currency_code}, 货币名称：{currency_name}，现汇卖出价：{exchange_rate}\n")

# 关闭浏览器
browser.quit()
