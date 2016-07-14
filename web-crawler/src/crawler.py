#coding=utf-8
import urllib
import urllib2
import os 
import os.path
import sys
import re
import requests

data = None
#post头部
headers = {
    }

path = "/home/aaa/桌面/问答/NoTalkMan/NoTalkMan/web-crawler/output_c/"

hostname = "http://zhidao.baidu.com"

def getId(url):
    reg = r'http://zhidao.baidu.com/question/(.+?).html'
    urlRe = re.compile(reg)
    urlList = re.findall(urlRe,url)
    if len(urlList) != 0:
        return urlList[0]
    else:
        return "fail"

def ifBadHtml(html):
    reg = r'<img class="word-replace" src="(.+?)">'
    badRe = re.compile(reg)
    badList = re.findall(badRe,html)
    if len(badList) != 0:
        return 1
    else:
        return 0

def getHtml(url):
    request = urllib2.Request(url, data, headers)
    print("Getting Response...")
    response = urllib2.urlopen(request)

    html = response.read()

    mk = ifBadHtml(html)
    while (mk == 1):
        request = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(request)
        print("Getting Response...")
        html = response.read()
        mk = ifBadHtml(html)
    return html

def getKeyword(html):
    reg = r'<meta name="keywords" content="(.+?)"/>'
    keywordRe = re.compile(reg)
    keywordList = re.findall(keywordRe,html)
    if len(keywordList) != 0:
    	result = keywordList[0]+"\n"
        return result
    else:
        return "fail\n"

def getUrl(html):
    reg = r'<link rel="canonical" href="(.+?)"/>'
    urlRe = re.compile(reg)
    urlList = re.findall(urlRe,html)
    if len(urlList) != 0:
    	result = urlList[0]+"\n"
        return result
    else:
        return "fail\n"

def getTitle(html):
    reg = r'<a href="/browse/.+?">(.+?)</a>'
    titleRe = re.compile(reg)
    titleList = re.findall(titleRe,html)
    result = ""
    if len(titleList) != 0:
    	for title in titleList:
    	    result = result+title+" "
        return result+"\n"
    else:
        return "fail\n"

def getQuestion(html):
    reg = r'<span class="ask-title ">(.+?)</span>'
    questionRe = re.compile(reg)
    questionList = re.findall(questionRe,html)
    if len(questionList) != 0:
    	result = questionList[0]+"\n"
        return result
    else:
        return "fail\n"

def getDescription(html):
    reg = r'accuse="qContent">(.+?)</pre>'
    descriptionRe = re.compile(reg)
    descriptionList = re.findall(descriptionRe,html)
    if len(descriptionList) != 0:
    	result = descriptionList[0]+"\n"
        return result
    else:
        return "none\n"

def getAnswer(html):
    reg = r'-content-.+?" accuse="aContent" class=".+?">(.+?)</pre>'
    answerRe = re.compile(reg)
    answerList = re.findall(answerRe,html)
    if len(answerList) != 0:
    	result = answerList[0]+"\n"
        return result
    else:
        return "fail\n"

def getGood(html):
    reg = r'data-evaluate="(.+?)"'
    goodRe = re.compile(reg)
    goodList = re.findall(goodRe,html)
    if len(goodList) != 0:
    	result = goodList[0]+"\n"
        return result
    else:
        return "fail\n"

def getQuality(html):
    reg = r'<div class="quality-content-detail content">\n(.+?)\n</div>'
    qualityRe = re.compile(reg)
    qualityList = re.findall(qualityRe,html)

    if len(qualityList) != 0:
    	result = qualityList[0]+"\n"
        return result
    else:
        return "none\n"

def getMoreUrl(html):

    reg = r'<a href="(.+?relate_question_.+?)" target="_blank"'
    moreUrlRe = re.compile(reg)
    moreUrlList = re.findall(moreUrlRe,html)
    return moreUrlList

def writeHtml(trueUrl, html):

    output = open(path+trueUrl, 'w')

    # 1. 特征值
    keyword = getKeyword(html)
    output.write(keyword)

    # 2. 标签
    title = getTitle(html)
    output.write(title)

    # 3. 问题
    question = getQuestion(html)
    output.write(question)

    # 4. 问题描述 (可能为空)
    description = getDescription(html)
    output.write(description)

    # 5. 回答
    answer = getAnswer(html)
    output.write(answer)

    # 6. 回答点赞数
    good = getGood(html)
    output.write(good)

    # 7. 专业回答 (可能为空)
    quality = getQuality(html)
    output.write(quality)

    # 8. 其他问题链接
    moreUrlList = getMoreUrl(html)

    result = ""
    if len(moreUrlList) != 0:
        for moreUrl in moreUrlList:
            result = result+hostname+moreUrl+"\n"
    else:
        result = "fail\n"
    output.write(result)

    output.close()

    return moreUrlList



# 1. 特征值
# 2. 标签
# 3. 问题
# 4. 问题描述 (可能为空)
# 5. 回答
# 6. 回答点赞数
# 7. 专业回答 (可能为空)
# 8. 其他问题链接