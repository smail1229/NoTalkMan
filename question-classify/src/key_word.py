#coding=utf-8

import jieba
import os
import math

jieba.load_userdict("../config/userdict.txt")
train_data_path = "../test_out/filterOut"
jieba_out_path = "../test_out/jieba_out"

def sort(array1, array2):   # 为idf排个序
    length = len(array1)
    for j in range(0,length-1):
        for i in range(0,length-1):
            if array2[i] >  array2[i+1]:
                tmp2 = array2[i]
                array2[i] = array2[i+1]
                array2[i+1] = tmp2
                tmp1 = array1[i]
                array1[i] = array1[i+1]
                array1[i+1] = tmp1
    return array1, array2


def getWord(fileName):     # 将文件获得分词后的数据写入
    if os.path.exists(fileName):
        train_file= open(fileName, "r")
        jieba_out= open(jieba_out_path, "w")
        split_word_set = set()
        allWord = train_file.readlines()
        train_file.close()
        for i in range(0,len(allWord)):
            if i%3 == 0:
                word = allWord[i]
                splitWord = jieba.cut(word, cut_all=False) # 用结巴分词
                for singleWord in splitWord:
                    if singleWord != " ":   # 忽略掉空格
                        if singleWord == "\n":
                            jieba_out.write((singleWord).encode('utf-8'))
                        else:
                            jieba_out.write((singleWord+" ").encode('utf-8'))
                            split_word_set.add(singleWord.encode('utf-8'))
        jieba_out.close()
        return split_word_set
    else:
        return split_word_set

def getHighFrequency(word_set, fileName):     # 将文件获得分词后的数据写入
    if os.path.exists(fileName):
        jieba_out = open(fileName, "r")
        high_freq_word = [] # 保存高频词
        high_freq = []
        word_array = []
        word_count = [] # 将出现次数保存在数组中
        for word in word_set:
            word_array.append(word) # 将词语保存在数组中
            word_count.append(0)

        allWord = jieba_out.read().replace("\n", " ").split()
        all_word_count = len(allWord) # 训练集词语总数

        jieba_out.close()

        for word in allWord: # 求出现次数
            for i in range(0, len(word_array)):
                if word_array[i] == word:
                    word_count[i] = word_count[i]+1

        for i in range(0, len(word_count)):          # 设置一个阈值，返回高于阈值概率的
            freq = float(word_count[i])/float(all_word_count) # 出现次数/训练集词语总数
            if freq >= 0:
                # print(word_array[i]+" "+str(freq))
                high_freq_word.append(word_array[i])
                high_freq.append(freq)    

        return high_freq_word,high_freq
    else:
        return high_freq_word,high_freq


def getLowEntropy(high_freq_word_array, high_freq_array, fileName):     # 将文件获得分词后的数据写入
    if os.path.exists(fileName):
        jieba_out = open(fileName, "r")
        allWord = jieba_out.readlines()
        jieba_out.close()
        word_array = high_freq_word_array
        freq_array = high_freq_array
        idf_array = []
        low_entr_word = [] # 保存idf低的词
        for i in range(0, len(word_array)):
            idf = 0 # idf的值
            n = 0 # 该高频词出现的问题数
            for word in allWord:
                word_count = len(word.split()) # 一个问题中的词语个数
                for singleWord in word.split():
                    if singleWord == word_array[i]:
                        n = n+1
                        break
            prob = float(n)/float(len(allWord))  # 出现行数/总行数
            idf = freq_array[i]*math.log(float(1)/prob)
            low_entr_word.append(word_array[i])
            idf_array.append(idf)

        return sort(low_entr_word, idf_array)
    else:
        return [],[]


if __name__ == "__main__":
    allWord = getWord(train_data_path)  # 完成分词
    high_freq_word,high_freq = getHighFrequency(allWord, jieba_out_path) # 获得高频词
    low_entr_word, idf  = getLowEntropy(high_freq_word, high_freq, jieba_out_path)# 获得信息熵低的词

    length = len(low_entr_word)
    sortOut = open("../test_out/sortOut", "w")
    for i in range(0,length):
        sortOut.write(low_entr_word[i]+" "+str(idf[i])+"\n")
    sortOut.close()
