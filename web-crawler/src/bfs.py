#coding=utf-8
import crawler
import urllib2
import Queue
import os

allUrl = set()
path = "/home/aaa/桌面/问答/NoTalkMan/NoTalkMan/web-crawler/"
hostname = "http://zhidao.baidu.com"

def ifExist(url):
    mk = 0
    for tmpUrl in allUrl:
        if tmpUrl == url:
            mk = 1
            break
    return mk

def bfs(longUrl):
    bfsQueue = Queue.Queue(0)
    bfsQueue.put(longUrl)
    cnt = 1
    while(bfsQueue.qsize() != 0 or cnt == 10000):
        html = crawler.getHtml(bfsQueue.get())
        url = crawler.getId(crawler.getUrl(html))
        if ifExist(url) == 0:
            allUrl.add(url)
            print(cnt)
            cnt = cnt+1
            moreUrlList = crawler.writeHtml(url, html)
            for moreUrl in moreUrlList:
                bfsQueue.put(hostname+moreUrl)
        else:
            print("already used, queue size:")
            print(bfsQueue.qsize())

urllib2.socket.setdefaulttimeout(100) # 另一种方式
bfs("http://zhidao.baidu.com/question/344067897")




# 1. 特征值
# 2. 标签
# 3. 问题
# 4. 问题描述 (可能为空)
# 5. 回答
# 6. 回答点赞数
# 7. 专业回答 (可能为空)
# 8. 其他问题链接