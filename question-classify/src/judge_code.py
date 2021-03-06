#coding=utf-8
import jieba

jieba.load_userdict("../config/userdict.txt")
filter_data_path = "../config/train_question"
filter_path = "../config/filter.txt"
train_data_path = "../train_data/train"

def ifIgnore(str):
    file_object = open(filter_path) #无视掉像是“c语言”，还有括号引号这样的字符串
    ignore = file_object.readlines()
    file_object.close()
    for tmp in ignore:
        if (str+"\n").encode("utf-8") == tmp:
            return False
    return True

def deteteTheCode(str):               # 输入为一个中文问题，判断这个问题是否有代码
    codeCount= 0
    allTheText = jieba.cut(str, cut_all=False)
    for stri in allTheText:
        asc = ord(stri[0])
        if (asc >= 0 and asc <= 47) or (asc >= 58 and asc <= 127): #以英文字母或者字符开头的部分
            if ifIgnore(stri):
                # print stri
                codeCount+= 1
        else:
            codeCount = 0
        if codeCount >= 5: #如果超过5个，无法回答
            return False               # 有代码
    return True                        # 没代码

if __name__ == "__main__":
    # test_str = "以下C语言程序中为什么用*t=n而不用return n；或者用return *t；?"
    # if deteteTheCode(test_str):
    #     print("No Code Exist")
    # else:
    #     print("Code Exist")

    fileIn = open(train_data_path, 'r')
    fileOut = open(filter_data_path, "w")
    lines = fileIn.readlines()
    for i in range(0, len(lines)):
        if (i%3) == 0:
            if deteteTheCode(lines[i].decode('utf-8')):
                fileOut.write(lines[i])
                fileOut.write(lines[i+1]+"\n")
    fileIn.close()
    fileOut.close()
