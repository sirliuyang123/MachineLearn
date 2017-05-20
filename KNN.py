from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt
from os import listdir
class KNN:
    def createDataSet():
        group = array([[1.0, 1.1], [1.0, 1.0], [0.0, 0.0], [0.0, 0.1]])
        labels = ['A', 'A', 'B', 'B']
        return group, labels

    def classify0(self,inX, dataSet, labels, k):
        dataSetSize = dataSet.shape[0]
        diffMat = tile(inX,(dataSetSize, 1)) - dataSet
        sgDiffMat = diffMat**2
        sgDistances = sgDiffMat.sum(axis=1)
        distances = sgDistances**0.5
        sortedDistIndicies = distances.argsort()
        classCount={}
        for i in range(k):

            voteIlabel = labels[sortedDistIndicies[i]]
            classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1

        sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
        return sortedClassCount[0][0]

    def file2matrix(self,filename):
            fr = open(filename)
            numberOfLines = len(fr.readlines())     #获取文件行数
            returnMat = zeros((numberOfLines, 3))   #将文件中的数据放到返回的矩阵中
            classLabelVector = []                   # 初始化一个空的标签对象作为将来的返回对象
            fr = open(filename)
            index = 0
            for line in fr.readlines():
                line = line.strip()
                listFromLine = line.split('\t')
                returnMat[index, :] = listFromLine[0:3]
                classLabelVector.append(int(listFromLine[-1]))
                index += 1
            return returnMat, classLabelVector

    def autoNorm(self,dataSet):
        minVals = dataSet.min(0)
        maxVals = dataSet.max(0)
        ranges = maxVals - minVals
        normDataSet = zeros(shape(dataSet))

        m = dataSet.shape[0]

        normDataSet = dataSet - tile(minVals, (m, 1))
        normDataSet = normDataSet / tile(ranges, (m, 1))  # 除法：此处的计算方法是 （原数-该列最小数）/（该列最大数-该列最小数）
        return normDataSet, ranges, minVals

    def datingClassTest(self):
        hoRatio = 0.10  # hold out 10%
        datingDataMat, datingLabels = self.file2matrix('datingTestSet2.txt')  # 读取文件
        normMat, ranges, minVals = self.autoNorm(datingDataMat)
        print(normMat)
        m = normMat.shape[0]
        print(m)
        numTestVecs = int(m * hoRatio)
        errorCount = 0.0
        for i in range(numTestVecs):
            classifierResult = self.classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
            print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i]))
            if (classifierResult != datingLabels[i]): errorCount += 1.0
        print("the total error rate is: %f" % (errorCount / float(numTestVecs)))
        print("the total error nuber is: %d" % errorCount)

k = KNN()
datingDataMat,datingLables = k.file2matrix('datingTestSet2.txt')
k.datingClassTest()

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.scatter(datingDataMat[:, 0],datingDataMat[:, 1])
#ax.scatter(datingDataMat[:, 0],datingDataMat[:, 1], 40.0*array(datingLables), 1.0*array(datingLables))
#plt.show()
