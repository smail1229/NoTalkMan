# 问题分类部分

## 文件的解释

## question-classify ───┬─ config ───────┬─── filter.txt      judge_code.py识别字符时，无视掉的部分
##                      │                ├─── keyword         问题分类所需的特征值的集
##                      │                ├─── test_question   测试集
##                      │                ├─── train_question  将五千个问题用judge_code.py过滤后，不含代码的问题
##                      │                └─── userdict.txt    结巴分词导入的词库
##                      │
##                      │  config: 程序需要的数据
##                      │
##                      ├──── src ───────┬─── judge_code.py    判断中文问题中是否有太多无法识别的字符
##                      │                ├─── key_word.py      数据预处理，并使用tfidf找出问题分类所需的特征值
##                      │                ├─── main.py          主函数
##                      │                └─── naive_bayesian_svm.py   使用朴素贝叶斯和svm对问题
##                      │
##                      │  src: 代码
##                      │
##                      ├─ test_out ─────┬─── outcome          使用朴素贝叶斯分类后的结果
##                      │                └─── sortOut          根据tfidf的值排序后的，中文问题中出现的词
##                      │
##                      │  test_out: 用来做参考的输出数据，对程序没影响
##                      │
##                      └─ train_data ─────── train    五千个问题作为训练集
##
##                         train_data: 训练数据

## 运行方式：
## 配置好：1.结巴分词 2.libsvm
## python main.py