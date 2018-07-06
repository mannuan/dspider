from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()
driver.maximize_window()

driver.get('https://www.kaola.com/')
# time.sleep(2)

# driver.switch_to_frame('x-URS-iframe')
# <div class="name head2 j-tag" id="auto-id-1527818410541">邮箱登录</div>
# driver.find_element_by_class_name('head2').click()
time.sleep(2)

# <input data-placeholder="网易邮箱帐号" name="email" data-type="email"
# data-loginname="loginEmail" data-required="true" class="j-inputtext
# dlemail" type="text" autocomplete="off" tabindex="1" spellcheck="false"
# id="auto-id-1527820362720" placeholder="网易邮箱帐号">
# loginEmail = driver.find_element_by_xpath("//*[@data-loginname='loginEmail']")

# 登录
# login_box = driver.find_element_by_css_selector('#loginbox2')
# iframe = login_box.find_element_by_css_selector('iframe')
# driver.switch_to.frame(iframe)
# driver.find_element_by_name('email').send_keys('vallzey@163.com')
# time.sleep(1)
# driver.find_element_by_name('password').send_keys('Vallzey1213')
# time.sleep(1)
# driver.find_element_by_id('dologin').click()
# time.sleep(5)

# 搜索
search = driver.find_element_by_id('topSearchInput').send_keys('手机壳')
time.sleep(1)
driver.find_element_by_id('topSearchBtn').click()
time.sleep(1)
titles = driver.find_elements_by_class_name('title')
titles[0].click()
time.sleep(1)

windows = driver.window_handles
driver.switch_to.window(windows[-1])
print(driver.title)

time.sleep(2)
driver.find_elements_by_css_selector('#j_skuwrap > div:nth-child(1) > div > ul > li > a')[0].click()
time.sleep(2)
driver.find_elements_by_css_selector('#j_skuwrap > div:nth-child(2) > div > ul > li > a')[0].click()
time.sleep(2)
driver.find_element_by_css_selector('#addCart.j-add2cart-btn').click()

time.sleep(20000)
driver.quit()