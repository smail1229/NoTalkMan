#coding=utf-8
import naive_bayesian_svm as nbs

if __name__ == "__main__":

    trainMatrix, classVec, keyVec, y, x  = nbs.data_processing()  # 处理数据，生成libsvm数据格式的训练数据
                                                       # 返回单词向量，问题类向量，特征值向量
                                                       # y,x 分别为libsvm需要的类别标签和问题的数据

    svm_model = nbs.data_training(trainMatrix, classVec, y, x)   # 设置pVect,pClass,返回svm的训练结果

    # ------------- 以上是数据预处理，和训练的部分----------------
    # ------------- 以下是测试的部分 ---------------------------

    print("训练完成，选择测试方式：\n1. 测试一个测试集\n2. 测试一个问题\n")
    choice = raw_input("选择：")
    if choice == "1":
        nbs.data_testing("../config/test_question", keyVec, svm_model)      # 进行朴素贝叶斯和svm结合的测试
    elif choice == "2":
        question = raw_input("输入中文问题：")

        question_class = nbs.predict_question(question, keyVec, svm_model)
        # 预测一个中文问题的类别，输入为：中文问题，中文特征值组成的向量，svm训练出的模型
        # 返回值为十个问题类中的一个：
        # classType = ["概念", "用法", "比较", "隶属",
        # "代码例子", "原因", "与C语言无关的事实类", "选择判断", "计算", "else"]
        # 如果问题中有代码，返回"内含代码"