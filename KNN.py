# -*- coding: utf-8 -*-
from numpy import *
from os import listdir
import operator
import matplotlib
import matplotlib.pyplot as plt

class KNN:
    def createDataSet(self):
        group = array([[1.0, 1.1], [1.0, 1.0], [0.0, 0.0], [0.0, 0.1]])
        labels = ['A', 'A', 'B', 'B']
        return group, labels

    def classify0(self, inX, dataSet, labels, k):
        dataSetSize = dataSet.shape[0]
        diffMat = tile(inX, (dataSetSize, 1)) - dataSet

        sgDiffMat = diffMat**2
        sgDistances = sgDiffMat.sum(axis=1)
        distances = sgDistances**0.5
        sortedDistIndicies = distances.argsort()  #排序，sortedDistIndicies中是数字元素从小到大排序序号的数组，如：2，3，6，7，1，4，5
        classCount={}
        for i in range(k):
            voteIlabel = labels[sortedDistIndicies[i]]                                           #获取排在前K个labels
            classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1                           #此处定义了一个空字典，字典的key是标签值，并用标签值去获取，如果之前有了，则+1，否则赋0
        sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)  #排序，operator.itemgetter(1)表示取第2个元素来进行排序
        return sortedClassCount[0][0]

    def file2matrix(self, filename):
            fr = open(filename)
            numberOfLines = len(fr.readlines())     #获取文件行数
            returnMat = zeros((numberOfLines, 3))   #将文件中的数据放到返回的矩阵中
            classLabelVector = []                   #初始化一个空的标签对象作为将来的返回对象
            fr = open(filename)
            index = 0
            for line in fr.readlines():
                line = line.strip()
                listFromLine = line.split('\t')
                returnMat[index, :] = listFromLine[0:3]
                classLabelVector.append(int(listFromLine[-1]))
                index += 1
            return returnMat, classLabelVector

    # 该方法用于取平均值，减少数值因为取值差距导致对结果的影响，即把矩阵中所有值都转成1以内的小数
    def autoNorm(self, dataSet):
        minVals = dataSet.min(0)
        maxVals = dataSet.max(0)
        ranges = maxVals - minVals
        normDataSet = zeros(shape(dataSet))
        m = dataSet.shape[0]
        normDataSet = dataSet - tile(minVals, (m, 1))
        normDataSet = normDataSet / tile(ranges, (m, 1))  # 除法：此处的计算方法是 （原数-该列最小数）/（该列最大数-该列最小数）
        return normDataSet, ranges, minVals

    def datingClassTest(self):
        hoRatio = 0.10  # 只取10%
        datingDataMat, datingLabels = self.file2matrix('datingTestSet2.txt')  # 读取文件
        normMat, ranges, minVals = self.autoNorm(datingDataMat)
        m = normMat.shape[0]
        numTestVecs = int(m * hoRatio)
        print("numTestVecs:", numTestVecs, "hoRatio:", m)
        errorCount = 0.0
        print(normMat[1, :], "shape:", shape(normMat[numTestVecs:m, :]))
        for i in range(numTestVecs):
            classifierResult = self.classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
            print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i]))
            if (classifierResult != datingLabels[i]): errorCount += 1.0
        #print("the total error rate is: %f"%(errorCount / float(numTestVecs)))
        #print("the total error number is: %d"%errorCount)

    #将文本中的内容转换成一个1，1024的矩阵向量
    def img2vector(self, filename):
        returnVect = zeros((1, 1024))
        fr = open(filename)
        for i in range(32):
            lineStr = fr.readline()
            for j in range(32):
                returnVect[0, 32 * i + j] = int(lineStr[j])
        return returnVect

    def ClassTest(self):
        hwLabels = []
        trainingFileList = listdir('trainingDigits')  #装载训练数据
        print(trainingFileList)

    def handwritingClassTest(self,k):
        hwLabels = []
        errorCount = 0
        trainingFileList = listdir('trainingDigits')  #装载训练数据

        m = len(trainingFileList)
        trainingMat = zeros((m, 1024))
        for i in range(m):
            fileNameStr = trainingFileList[i]
            fileStr = fileNameStr.split('.')[0]       #去掉后缀名
            classNumStr = int(fileStr.split('_')[0])
            hwLabels.append(classNumStr)
            trainingMat[i, :] = self.img2vector('trainingDigits/%s' % fileNameStr)

        testFileList = listdir('testDigits')        #装载测试样本
        errorCount = 0.0
        mTest = len(testFileList)
        for i in range(mTest):
            fileNameStr = testFileList[i]
            fileStr = fileNameStr.split('.')[0]
            classNumStr = int(fileStr.split('_')[0])
            vectorUnderTest = self.img2vector('testDigits/%s' % fileNameStr)
            classifierResult = self.classify0(vectorUnderTest, trainingMat, hwLabels, k)
            # print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr), "test:", fileStr)
            if (classifierResult != classNumStr): errorCount += 1.0
        print("\nthe total number of errors is: %d" % errorCount)
        # print("\nthe total error rate is: %f" % (errorCount / float(mTest)))
        return errorCount

    def testBestKNNValue(self):
        returnValue = []
        Kvalue = 0
        for kk in range(10):
            returnValue.append(k.handwritingClassTest(kk + 1))
            Kvalue = sorted(returnValue, reverse=False)
        print("beseKvalue is: %f" %Kvalue[0])

k = KNN()
# datingDataMat,datingLables = k.file2matrix('datingTestSet2.txt')
# k.datingClassTest()
k.testBestKNNValue()



# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(datingDataMat[:, 0],datingDataMat[:, 1])
# ax.scatter(datingDataMat[:, 0],datingDataMat[:, 1], 40.0*array(datingLables), 1.0*array(datingLables))
# plt.show()
