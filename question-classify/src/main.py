#coding=utf-8
from key_word import *
from naive_bayesian_svm import *

if __name__ == "__main__":
    allWord = getWord("../config/train_question", "../test_out/jieba_out", "../test_out/class_out")

    trainMatrix, classVec, keyVec, y, x  = data_processing()  # 处理数据，生成libsvm数据格式的训练文件
                                                       # 并返回单词向量，问题类向量，特征值向量

    svm_model = data_training(trainMatrix, classVec, y, x)   # 设置pVect,pClass,返回svm的训练结果

    print("训练完成，选择测试方式：\n1. 测试一个测试集\n2. 测试一个问题\n")
    choice = raw_input("选择：")
    if choice == "1":
        data_testing("../config/test_question", keyVec, svm_model)      # 进行朴素贝叶斯和svm结合的测试
    elif choice == "2":
    	question = raw_input("输入问题：")
        predict_question(question, keyVec, svm_model)