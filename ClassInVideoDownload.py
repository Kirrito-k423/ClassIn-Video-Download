# coding=utf-8

import os
import sys
import json
import re
from urllib import parse
import urllib.request
from requests import Session

def report(a,b,c):
    '''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print ('%.2f%%' % per)
# ————————————————
# 版权声明：本文为CSDN博主「爱python的王三金」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/qq_37275405/article/details/80780925
def download_single_lesson(url):
    session = Session()
    lessonKey = parse.parse_qs(parse.urlparse(
        url).query).get('lessonKey', [])[0]
    lesson_info_url = "https://www.eeo.cn/saasajax/webcast.ajax.php?action=getLessonLiveInfo"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    }
    if len(lessonKey) == 0:
        return False
    else:
        data = {
            'lessonKey': lessonKey
        }
    try:
        resp = session.post(url=lesson_info_url, headers=headers, data=data)
        text = resp.json()
        CourseName = text['data']['courseName']
        path = os.getcwd()+"/ClassInVideo/" + CourseName + "/" + \
            text['data']['lessonData']['fileList'][0]['CreateTime'][5:10] + "/"
        if(not os.path.exists(path)):
            os.makedirs(path)
        for play in text['data']['lessonData']['fileList']:
            CreateDate = play['CreateTime'].replace(':', '-')
            filename = CreateDate[:10]+'-'+CreateDate[11:]+".mp4"
            url = play['Playset'][0]['Url']
            storepath = path + filename
            if os.path.isfile(storepath):
                if int(play['Size']) == os.path.getsize(storepath):
                    print("文件 "+storepath+" 已经下载好")
                    continue
                else:
                    print("存在大小不一致重名文件 "+storepath+" 将要覆盖它")
            print("Downloading: " + filename + " ...")
            urllib.request.urlretrieve(url, storepath,reporthook=report)
            print("Download: " + filename + " Done!")
        return True
    except:
        print('请关闭clash等代理，稍后重试')


def main():
    filepaths = os.getcwd() + "/todo/"
    filelist = os.listdir(filepaths)
    for html_file in filelist:
        if html_file[-5:] != '.html':
            continue
        with open(filepaths + html_file, "r", encoding='utf-8') as html:
            text = html.read()
            lesson_urls = re.findall("https://www.eeo.cn/live.php\S{27,27}", text)
            for lesson_url in lesson_urls:
                if not download_single_lesson(lesson_url):
                    print(lesson_url + "下载失败！")
        print(html_file + "下载完成！")

main()
