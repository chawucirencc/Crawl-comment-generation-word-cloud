#!/usr/bin/env.python
# -*- coding: utf-8 -*-
import requests
import re
import random
import jieba
import wordcloud
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from requests import RequestException

def get_url_list():
    """得到URL列表"""
    url_list = []
    for i in range(0, 50, 2):
        url = 'https://movie.douban.com/subject/1292052/comments?start=' \
              + str(i*10) + '&limit=20&sort=new_score&status=P'
        url_list.append(url)
    return url_list

def get_text(url_list, headers):
    """通过正则表达式提取出评论信息"""
    res = ''
    for i in url_list:
        try:
            r = requests.get(i, headers=headers)
            if r.status_code == 200:
                r.encoding = 'utf-8'
                text_list = re.findall(r'<span class="short">(.*?)</span>', r.text)
                for text in text_list:
                    res += text + '。'
        except RequestException:
            print(RequestException)
    return res

def save_result(res):
    """将结果保存到txt文件"""
    path = r'C:\Users\Talent\Desktop\res.txt'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(res)
    f.close()
    return path

def draw_wordcloud(path):
    """通过传入路径参数，读取之前保存的txt文件，画出词云图"""
    file = open(path, encoding='utf-8').readlines()
    word = ''
    for line in file:
        cut = jieba.cut(line)
        for i in cut:
            if i not in '，。“”？【】《》：！—（）.、':
                if len(i) > 1:
                    word += i + '/'
    font_path='C:\\Windows\\Fonts\\Deng.ttf'
    # 设置WordCloud参数
    wc = wordcloud.WordCloud(font_path=font_path, background_color='white', width=700, height=400, max_words=1000)
    wc.generate(word)
    wc.to_file('word3.png')
    plt.imshow(wc)
    plt.axis('off')
    plt.show()

def main():
    """主函数"""
    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
    ]
    user_agent = random.choice(my_headers)
    headers = {
        'User_Agent': user_agent,
        'Cookie': 'll="108231"; bid=lp6WDrc5nKc; _vwo_uuid_v2=D2003811F9920EDDB4CE4497C487751D9|a954d86b21a4eb3b3ccea6b2fe090eac; ap_6_0_1=1; ps=y; ue="1960595754@qq.com"; push_doumail_num=0; __utmz=30149280.1534871147.6.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=223695111.1534871152.6.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1535027767%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.804054632.1534244658.1534944165.1535027767.10; __utmc=30149280; __utma=223695111.1126706729.1534244658.1534944168.1535027767.10; __utmb=223695111.0.10.1535027767; __utmc=223695111; ap_v=1,6.0; as="https://movie.douban.com/subject/26752088/comments?start=40&limit=20&sort=new_score&status=P"; dbcl2="160936860:paffOo90ZWA"; ck=PQeC; push_noty_num=0; __utmv=30149280.16093; __utmb=30149280.2.10.1535027767; _pk_id.100001.4cf6=b7df88e2b11c58f8.1534244658.11.1535031771.1534944266.'
    }
    url_list = get_url_list()
    res = get_text(url_list, headers)
    path = save_result(res)
    draw_wordcloud(path)


main()      # 调用主函数
