from numpy import *
import  operator

class KNN():
    def createDataSet(self):
        group = array([[1.0,1.1],[1.0,1.0],[0.0,0.0],[0.0,0.1]])
        labels =['A','A','B','B']
        return  group,labels

    def classify0(self,inX,dataSet,labels,k):
        dataSetSize = dataSet.shape[0]
        diffMat = tile(inX,(dataSetSize,1)) - dataSet
        sgDiffMat = diffMat**2
        sgDistances = sgDiffMat.sum(axis=1)
        distances = sgDistances**0.5
        sorteDistIndicies = distances.argsort()
        classCount = {}
        for i in range(k):
            voteIlable =  labels[sorteDistIndicies[i]]
            print voteIlable
            classCount [voteIlable] = classCount.get(voteIlable,0)+1
            print classCount
        sortedClassCount = sorted(classCount.iteritems(),key = operator.itemgetter(1),reverse=True)
        return sortedClassCount[0][0]

    def file2matrix(selft,filename):
        fr = open(filename)
        numberOfLines = len(fr.readlines())  # get the number of lines in the file
        returnMat = zeros((numberOfLines, 3))  # prepare matrix to return
        classLabelVector = []  # prepare labels return
        fr = open(filename)
        index = 0
        for line in fr.readlines():
            line = line.strip()
            listFromLine = line.split('\t')
            returnMat[index, :] = listFromLine[0:3]
            classLabelVector.append(int(listFromLine[-1]))
            index += 1
        return returnMat, classLabelVector

    def autoNorm(dataSet):
        minVals = dataSet.min(0)
        maxVals = dataSet.max(0)
        ranges = maxVals - minVals
        normDataSet = zeros(shape(dataSet))
        m = dataSet.shape[0]
        normDataSet = dataSet - tile(minVals, (m, 1))
        normDataSet = normDataSet / tile(ranges, (m, 1))  # element wise divide
        return normDataSet, ranges, minVals
kk = KNN()



group,labels = kk.createDataSet()
print(kk.classify0([2,1],group,labels,4))
