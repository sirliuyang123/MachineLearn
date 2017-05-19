from numpy import *
import  operator

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0.0,0.0],[0.0,0.1]])
    labels =['A','A','B','B']
    return  group,labels

def classify0(inX,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1)) - dataSet

    sgDiffMat = diffMat**2

    sgDistances = sgDiffMat.sum(axis=1)

    distances = sgDistances**0.5
    #print diffMat,sgDiffMat,sgDistances,distances
    sorteDistIndicies = distances.argsort()
    print distances,sorteDistIndicies
    classCount = {}
    for i in range(k):
        voteIlable =  labels[sorteDistIndicies[i]]
        print voteIlable
        classCount [voteIlable] = classCount.get(voteIlable,0)+1
        print classCount
    sortedClassCount = sorted(classCount.iteritems(),key = operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

group,labels = createDataSet()
print(classify0([2,1],group,labels,4))