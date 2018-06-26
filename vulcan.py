#!/usr/bin/python3
#-*- coding:utf-8 -*-

from selenium import webdriver  #导入Selenium
import requests
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import os  #导入os模块
import time
import urllib.request
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait

brower = webdriver.PhantomJS()
img_file = "E:\python脚本\练习\captcha.png"
wait = WebDriverWait(brower,10)

#登陆
def login(url,username,password,movie):
    brower.get(url)
    brower.find_element_by_css_selector('[class="login"]').click()
    name = brower.find_element_by_id('form_email')
    name.clear()
    name.send_keys(username)
    pwd = brower.find_element_by_id('form_password')
    pwd.clear()
    pwd.send_keys(password)
    # pic_src = brower.find_element_by_id('captcha_image').get_attribute('src')
    # #调用验证码的方法
    # cap_value = get_yzm(pic_src,img_file)
    # yan_zheng_ma = brower.find_element_by_id('captcha_field')
    # yan_zheng_ma.clear()
    # yan_zheng_ma.send_keys(cap_value)
    brower.find_element_by_css_selector('[class="bn-submit"]').click()
    print('登陆成功')
    # print(brower.current_url)
    brower.get("https://movie.douban.com")
    # print(brower.page_source)
    seach(movie)



#获取验证码
def get_yzm(src,img_file):
    print("正在保存验证码图片")
    captchapicfile = img_file
    urllib.request.urlretrieve(src,filename=captchapicfile)
    im = Image.open(captchapicfile)
    im = im.convert('L')
    im = im.point(tab(),'1')
    im.show()
    print("请输入验证码：")
    captcha_value = input()
    return captcha_value

def tab(threshold=140):
    table = []  
    for i in range(256):  
        if i < threshold:  
            table.append(0)  
        else:  
            table.append(1)  
    return table


#搜索电影
def seach(movie_name):
    inp_query = brower.find_element_by_id('inp-query')
    inp_query.clear()
    inp_query.send_keys(movie_name)
    submit = brower.find_element_by_css_selector('[type="submit"]')
    submit.click()
    time.sleep(1)
    brower.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[1]/a').click()
    # print(brower.page_source)
    print("进入详情")
    into_comment()
    get_comment()

#进入短评列表
def into_comment():
    brower.find_element_by_xpath('//*[@id="comments-section"]/div[1]/h2/span/a').click()
    print("进入短评列表")

def get_comment():
    wait.until(lambda brower : brower.find_element_by_css_selector('[class="next"]'))
    time.sleep(1)
    d = {}
    for i in range(1,21):
        comment = brower.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/p'.format(str(i))).text
        comment_name = brower.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[1]/span'.format(str(i))).text
        votes = brower.find_element_by_xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[1]/span'.format(str(i))).text
        #构建字典
        data = {
            'comment': comment,
            'comment_name': comment_name,
            'votes': int(votes)
        }
        comment.insert_one(data)
        print('*'*100)
        d[i] = data
        print(data)
        print("成功存入数据库")
    # for i in range(len(d)):
    #     print(d[i+1])
    # print(d)



if __name__ == '__main__':
    params={}
    params['form_email']='XieJunJieEnd@aliyun.com'  
    params['form_password']='f19179a06954edd0'#这里写上已有的用户名和密码 
    params['source']='http://www.douban.com' 
    params['movie'] = ""
    login(params['source'], params['form_email'], params['form_password'],params['movie'])
