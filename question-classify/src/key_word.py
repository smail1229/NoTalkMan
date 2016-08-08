#coding=utf-8

import jieba
import os
import math

jieba.load_userdict("../config/userdict.txt")
train_data_path = "../config/train_question"

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

def splitQuestion(question):                # 用结巴分词将问题分词
    word_vec = []
    splitWord = jieba.cut(question, cut_all=False)
    for singleWord in splitWord:
        if singleWord != " " and singleWord != "\n":   # 忽略掉空格和换行
            word_vec.append(singleWord.encode('utf-8'))
    return word_vec

def getWord(fileName):     # 将文件获得分词后的数据写入
    if os.path.exists(fileName):
        train_file= open(fileName, "r")
        allWord = train_file.readlines()
        split_word_set = set()   # 训练集的问题，分词之后的集，用set是因为不要重复的词语
        split_word_vec = [[] for i in range((len(allWord))/3)]   # 训练集的问题，分词之后的数组
        class_vec = []                                           # 训练集的问题类的数组
        train_file.close()
        for i in range(0,len(allWord)):
            word = allWord[i]
            if i%3 == 0:
                splitWord = splitQuestion(word) # 用结巴分词
                for singleWord in splitWord:
                    split_word_set.add(singleWord)
                    split_word_vec[i/3].append(singleWord)
                    #print(singleWord.encode('utf-8'))
            elif i%3 == 1:
                class_vec.append(word)
        return split_word_set,class_vec,split_word_vec
    else:
        return [],[]

def getHighFrequency(word_set, word_vec):     # 将文件获得分词后的数据写入
    high_freq_word = [] # 保存高频词
    high_freq = []
    word_array = []
    word_count = [] # 将出现次数保存在数组中
    for word in word_set:
        word_array.append(word) # 将词语保存在数组中
        word_count.append(0)

    allWord = []
    for i in range(0, len(word_vec)):
        for j in range(0, len(word_vec[i])):
            allWord.append(word_vec[i][j]) # 将词语保存在数组中

    all_word_count = len(allWord) # 训练集词语总数


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


def getLowEntropy(high_freq_word_array, high_freq_array, allWord):     # 将文件获得分词后的数据写入
    word_array = high_freq_word_array
    freq_array = high_freq_array
    idf_array = []
    low_entr_word = [] # 保存idf低的词
    for i in range(0, len(word_array)):
        idf = 0 # idf的值
        n = 0 # 该高频词出现的问题数
        for word in allWord:
            word_count = len(word) # 一个问题中的词语个数
            for singleWord in word:
                if singleWord == word_array[i]:
                    n = n+1
                    break
        prob = float(n)/float(len(allWord))  # 出现行数/总行数
        idf = freq_array[i]*math.log(float(1)/prob)
        low_entr_word.append(word_array[i])
        idf_array.append(idf)

    return sort(low_entr_word, idf_array)


if __name__ == "__main__":
    split_word_set,class_vec,split_word_vec = getWord(train_data_path)  # 完成分词
    high_freq_word,high_freq = getHighFrequency(split_word_set, split_word_vec) # 获得高频词
    low_entr_word, idf  = getLowEntropy(high_freq_word, high_freq, split_word_vec)# 获得信息熵低的词

    length = len(low_entr_word)
    sortOut = open("../test_out/sortOut", "w")
    for i in range(0,length):
        sortOut.write(low_entr_word[i]+" "+str(idf[i])+"\n")
    sortOut.close()
