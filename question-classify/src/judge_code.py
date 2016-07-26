#coding=utf-8
import jieba

jieba.load_userdict("../config/userdict.txt")

def ifIgnore(str):
    file_object = open("../config/filter.txt") #无视掉像是“c语言”，还有括号引号这样的字符串
    ignore = file_object.readlines()
    file_object.close()
    for tmp in ignore:
        if (str+"\n").encode("utf-8") == tmp:
            return False
    return True

def deteteTheCode(str):
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
            return False
    return True

if __name__ == "__main__":
    # test_str = "以下C语言程序中为什么用*t=n而不用return n；或者用return *t；?"
    # if deteteTheCode(test_str):
    #     print("No Code Exist")
    # else:
    #     print("Code Exist")

    fileIn = open("../train_data/train", 'r')
    fileOut = open("../test_out/filterOut", "w")
    lines = fileIn.readlines()
    for i in range(0, len(lines)):
        if (i%3) == 0:
            if deteteTheCode(lines[i].decode('utf-8')):
                fileOut.write(lines[i])
                fileOut.write(lines[i+1]+"\n")
    fileIn.close()
    fileOut.close()
