# -*- coding: utf-8 -*-
from math import log
import operator
from treePlotter import treePlotter

class trees:
    def createDataSet(self):
        dataSet = [[1, 1, 'yes'], [1, 1, 'yes'], [1, 0, 'no'], [0, 1, 'no'], [0, 1, 'no']]
        labels = ['no surfacing', 'flippers']
        return dataSet, labels

    # 计算香农熵
    def calcShannonEnt(self, dataSet):
        numEntries = len(dataSet)
        labelCounts = {}
        for featVec in dataSet:
            currentLabel = featVec[-1]
            if currentLabel not in labelCounts.keys():
                labelCounts[currentLabel] = 0
            labelCounts[currentLabel] += 1
        shannonEnt = 0.0
        for key in labelCounts:
            prob = float(labelCounts[key])/numEntries  #prob为选择这个分类的概率
                                                       #计算香农熵,这里shannonEnt需要根据P(xi)来计算，P(xi)表示选择这个类型所发生的概率，
            shannonEnt -= prob * log(prob, 2)          # 然后将所有类型进行叠加
        return shannonEnt

    #用于将数据集根据目标（即：axis）的值要求（即：value），返回与这个目标相同的数据集
    def splitDataSet(self, dataSet, axis, value):
        retDataSet = []
        for featVec in dataSet:
            if featVec[axis] == value:
                reducedFeatVec = featVec[:axis]          #把目标值前面的数据取出来
                reducedFeatVec.extend(featVec[axis+1:])  #把目标值后面的数据取出来，并extend到reducedFeatVec
                retDataSet.append(reducedFeatVec)        #把reducedFeatVec列表append到retDataSet并进行返回
        return retDataSet

    #取熵最大的并返回序号
    def chooseBestFeatureToSplit(self, dataSet):
        numFeatures = len(dataSet[0]) - 1               #将最后一个元素作为类别标签
        baseEntropy = self.calcShannonEnt(dataSet)      #原始香农熵
        bestInfoGain = 0.0
        bestFeature = -1
        for i in range(numFeatures):
            featList = [example[i] for example in dataSet]  # 用第i列的特征值新建一个数组
            uniqueVals = set(featList)  # 用set获取一个不重复的特征值set
            newEntropy = 0.0
            for value in uniqueVals:
                subDataSet = self.splitDataSet(dataSet, i, value)
                prob = len(subDataSet) / float(len(dataSet))
                newEntropy += prob * self.calcShannonEnt(subDataSet)
            infoGain = baseEntropy - newEntropy  # infoGain为信息增益 ，即老香农熵 - 新的香农熵
            if (infoGain > bestInfoGain):  #
                bestInfoGain = infoGain  # 取信息增益最大的值，并返回这个列序号
                bestFeature = i
        return bestFeature

    #把最多标签返回
    def majorityCnt(self, classList):
        classCount = {}
        for vote in classList:
            if vote not in classCount.keys(): classCount[vote] = 0
            classCount[vote] += 1
        sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sortedClassCount[0][0]

    def createTree(self, dataSet, labels):
        classList = [example[-1] for example in dataSet]
        if classList.count(classList[0]) == len(classList):
            return classList[0]  # 如果所有的标签都相同的话，则返回
        if len(dataSet[0]) == 1:  # 遍历完，返回出现次数最多的元素
            return self.majorityCnt(classList)
        bestFeat = self.chooseBestFeatureToSplit(dataSet)     #将dataSet中，熵值最大的标签序号返回
        print bestFeat
        bestFeatLabel = labels[bestFeat]
        myTree = {bestFeatLabel: {}}
        del (labels[bestFeat])
        featValues = [example[bestFeat] for example in dataSet]
        uniqueVals = set(featValues)
        for value in uniqueVals:    #获取该组标签里面不重复的值（也就是分支），然后递归循环分支
            subLabels = labels[:]
            myTree[bestFeatLabel][value] = self.createTree(self.splitDataSet(dataSet, bestFeat, value), subLabels)
        return myTree

    def classify(self, inputTree, featLabels, testVec):
        firstStr = inputTree.keys()[0]

        secondDict = inputTree[firstStr]
        print featLabels.index(firstStr)
        featIndex = featLabels.index(firstStr)
        key = testVec[featIndex]
        valueOfFeat = secondDict[key]
        if isinstance(valueOfFeat, dict):
            classLabel = self.classify(valueOfFeat, featLabels, testVec)
        else:
            classLabel = valueOfFeat
        return classLabel

t = trees()
tp = treePlotter()
dataSet, labels = t.createDataSet()
# myTree = t.createTree(dataSet, labels)







