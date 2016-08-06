
#coding=utf-8
from numpy import *
from svmutil import *
import key_word
import judge_code

test_ques_path = "../config/test_question"
jieba_out_path = "../test_out/jieba_out"
class_out_path = "../test_out/class_out"
key_out_path = "../config/keyword"
limit = 1
classType = ["概念", "用法", "比较", "隶属", "代码例子", "原因", "与C语言无关的事实类", "选择判断", "计算", "else"]
classNum = len(classType)
pClass = [0]*classNum                # 某一类问题出现的总概率
pVect = [0]*classNum                 # 某一类问题各个特征值出现的概率

def loadDataSet():                         # 构建单词向量，问题类向量，特征值向量

    postingList = getPostingList(jieba_out_path)    # 单词向量
    classVec = getClassVec(class_out_path)          # 问题类向量
    keyVec = getKeyVec(key_out_path)                # 特征值向量

    return postingList,classVec,keyVec

def getPostingList(filepath):                  #获得单词向量
    jieba_out= open(filepath, "r")
    word_list = jieba_out.readlines()

    postingList=[[] for i in range(len(word_list))]
    for i in range(0, len(word_list)):
        word_line = word_list[i]
        for word in word_line.split():
            if word != "\n":   # 忽略掉空格
                postingList[i].append(word)
    jieba_out.close()
    return postingList

def getClassVec(filepath):                     # 获得问题类向量
    class_out= open(filepath, "r")
    classVec = []                                            
    class_list = class_out.readlines()

    for i in range(0, len(class_list)):
        tmp_class = class_list[i]
        err = 1
        for j in range(0, len(classType)):
            if tmp_class == classType[j]+"\n":
                classVec.append(j)  # 问题类向量编号0到9
                err = 0
                break
        if err == 1:
            print("this type not exist")
            print(i)
    print(len(classVec))
    class_out.close()

    return classVec

def getKeyVec(filepath):                     # 获得特征值向量
    key_out= open(filepath, "r")
    keyVec = []
    key_list = key_out.read()

    for key in key_list.split("\n"):
        if key != "\n":   # 忽略掉空格
            keyVec.append(key)
    key_out.close()
    return keyVec

def setOfWords2Vec(vocabList, inputSet):  # 将单词变成变成0或者1的数组
    returnVec = [0]*len(vocabList)

    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
    return returnVec

def trainNB(trainMatrix,trainCategory):  # 进行训练，统计出特征值出现的概率，类别的概率
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])

    for i in range(0,numTrainDocs):
        pClass[trainCategory[i]] = pClass[trainCategory[i]]+1

    for i in range(0,len(pClass)):
        pClass[i] = float(pClass[i])/float(numTrainDocs)

    pNum = [[] for i in range(numWords)]
    pDenom = [0]*classNum
    for i in range(0,len(pClass)):
        pNum[i] = ones(numWords)               #change to ones() 
        pDenom[i] = 2.0                           #change to 2.0

    for i in range(numTrainDocs):
        pNum[trainCategory[i]] += trainMatrix[i]
        pDenom[trainCategory[i]] += sum(trainMatrix[i])
    
    for i in range(0,len(pClass)):
        pVect[i] = log(pNum[i]/pDenom[i])          #change to log()

def classifyNB(vec2Classify):   # 根据概率进行判断
    p = [0]*classNum
    for i in range(0, len(p)):
        p[i] = sum(vec2Classify * pVect[i]) + log(pClass[i])
    return p.index(max(p)), p

def getThresholdForSVM(prob):  # 获得朴素贝叶斯的最大概率和第二大概率的差，作为阈值
    tmp_prob = prob
    for i in range(0,len(prob)):
        for j in range(0,len(prob)-1):
            if tmp_prob[j] < tmp_prob[j+1]:
                tmp = tmp_prob[j]
                tmp_prob[j] = tmp_prob[j+1]
                tmp_prob[j+1] = tmp
    return tmp_prob[0]-tmp_prob[1]

def testOneQuestion(test_ques, keyVec):
    if not judge_code.deteteTheCode(test_ques):         # 判断问题中是否有代码
        return 10, []
    else:
        tmp_vec = key_word.splitQuestion(test_ques)
        test_ques_vec = setOfWords2Vec(keyVec, tmp_vec)
        return classifyNB(test_ques_vec)

def trainingDataForSVM(trainMatrix):    # 生成libsvm数据格式的训练数据
    x = []
    for trainVec in trainMatrix:
        xi = {}
        for i in range(0, len(trainVec)):
            xi[i+1] = trainVec[i]
        x.append(xi)
    return x


def setOfWords2Matrix(postingList, keyVec):   # 将整个矩阵变成向量
    trainMatrix = []
    for trainVec in postingList:                         
        trainMatrix.append(setOfWords2Vec(keyVec, trainVec))
    return trainMatrix

def data_processing():     #处理数据
    postingList,classVec,keyVec = loadDataSet()
    trainMatrix = setOfWords2Matrix(postingList, keyVec)   # 将整个矩阵变成向量
    y = classVec
    x = trainingDataForSVM(trainMatrix)    # 生成libsvm数据格式的训练数据

    return trainMatrix, classVec, keyVec, y, x

def data_training(trainMatrix, classVec, y, x):
    trainNB(trainMatrix, classVec)      # 设置pVect,pClass

    svm_model = svm_train(y, x, '-c 10000')
    return svm_model


def data_testing(testpath, keyVec, svm_model):   # 测试测试集的问题
    question_set = open(testpath, 'r')
    question_list = question_set.readlines()
    num = len(question_list)
    correct = 0
    question_class_vec = [0]*((num+1)/3)

    tmp_jieba_path = "../test_out/tmp_jieba"
    tmp_class_path = "../test_out/tmp_class"
    key_word.getWord(testpath, tmp_jieba_path, tmp_class_path)
    postingList = getPostingList(tmp_jieba_path)
    classVec = getClassVec(tmp_class_path)
    trainMatrix = setOfWords2Matrix(postingList, keyVec)
    y = classVec
    x = trainingDataForSVM(trainMatrix)           # 生成libsvm数据格式的测试数据

    low_threshold_y, low_threshold_x = [], []

    for i in range(0,num):
        if i%3 == 0:
            outcome, prob = testOneQuestion(question_list[i], keyVec)
            threshold = getThresholdForSVM(prob) # 获得阈值
            if outcome == 10:
                print("看不懂问题")
                question_class_vec[i/3] = outcome
            elif threshold < limit:                               # 小于阈值的丢到一个数组进行svm
                low_threshold_y.append(y[i/3])
                low_threshold_x.append(x[i/3])
                question_class_vec[i/3] = -1
            else:
                question_class_vec[i/3] = outcome

    p_label, p_acc, p_val = svm_predict(low_threshold_y, low_threshold_x, svm_model)
    j = 0
    for i in range(0,len(question_class_vec)):
        if question_class_vec[i] == -1:
            question_class_vec[i] = p_label[j]                # 朴素贝叶斯和svm都处理完之后，将结果拼到一个数组
            j = j+1


    for i in range(0,len(question_class_vec)):
        if question_class_vec[i] <= 9 and question_class_vec[i] >= 0:
            # print(classType[int(question_class_vec[i])]+"\n")
            if classType[int(question_class_vec[i])]+"\n" == question_list[3*i+1]:
                correct = correct+1
        else:
            print("Some problem at question "+str(i))
    question_set.close()

    num = (num+1)/3
    precision = float(correct)/float(num)
    print("correct: "+str(correct))
    print("total: "+str(num))
    print("precision: "+str(precision))

def predict_question(question, keyVec, svm_model):            # 预测一个问题
    outcome, prob_array = testOneQuestion(question, keyVec)
    if outcome == 10:
        print("看不懂问题")                                     # 问题中有过多无法识别的字符
    else:
        threshold = getThresholdForSVM(prob_array)
        if threshold >= limit:
            print("nb: "+classType[outcome]+"\n")
        else:
            tmp_vec = []
            tmp_vec.append(key_word.splitQuestion(question))
            ques_matrix = setOfWords2Matrix(tmp_vec, keyVec)
            y = [0]
            x = trainingDataForSVM(ques_matrix)
            p_label, p_acc, p_val = svm_predict(y, x, svm_model)
            print("svm: "+classType[int(p_label[0])]+"\n")
        

if __name__ == "__main__":

    trainMatrix, classVec, keyVec, y, x = data_processing()  # 处理数据，生成libsvm数据格式的训练数据
                                                             # 并返回单词向量，问题类向量，特征值向量

    svm_model = data_training(trainMatrix, classVec, y, x)   # 设置pVect,pClass,返回svm的训练结果

    data_testing(test_ques_path, keyVec, svm_model)          # 进行朴素贝叶斯和svm结合的测试
