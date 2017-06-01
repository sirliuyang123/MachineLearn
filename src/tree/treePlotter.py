import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

class treePlotter:

    def getNumLeafs(self, myTree):
        numLeafs = 0
        firstStr = myTree.keys()[0]
        secondDict = myTree[firstStr]
        for key in secondDict.keys():
            if type(secondDict[key]).__name__ == 'dict':  # test to see if the nodes are dictonaires, if not they are leaf nodes
                numLeafs += treePlotter.getNumLeafs(secondDict[key])
            else:
                numLeafs += 1
        return numLeafs


    def getTreeDepth(self, myTree):
        maxDepth = 0
        firstStr = myTree.keys()[0]
        secondDict = myTree[firstStr]
        for key in secondDict.keys():
            if type(secondDict[key]).__name__ == 'dict':  # test to see if the nodes are dictonaires, if not they are leaf nodes
                thisDepth = 1 + treePlotter.getTreeDepth(secondDict[key])
            else:
                thisDepth = 1
            if thisDepth > maxDepth: maxDepth = thisDepth
        return maxDepth


    def plotNode(self, nodeTxt, centerPt, parentPt, nodeType):
        treePlotter.createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                                xytext=centerPt, textcoords='axes fraction',
                                va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)


    def plotMidText(self, cntrPt, parentPt, txtString):
        xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
        yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
        treePlotter.createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)


    def plotTree(self, myTree, parentPt, nodeTxt):  # if the first key tells you what feat was split on
        numLeafs = treePlotter.getNumLeafs(myTree)  # this determines the x width of this tree
        depth = treePlotter.getTreeDepth(myTree)
        firstStr = myTree.keys()[0]  # the text label for this node should be this
        cntrPt = (treePlotter.plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / treePlotter.plotTree.totalW, treePlotter.plotTree.yOff)
        treePlotter.plotMidText(cntrPt, parentPt, nodeTxt)
        treePlotter.plotNode(firstStr, cntrPt, parentPt, decisionNode)
        secondDict = myTree[firstStr]
        treePlotter.plotTree.yOff = treePlotter.plotTree.yOff - 1.0 / treePlotter.plotTree.totalD
        for key in secondDict.keys():
            if type(secondDict[
                        key]).__name__ == 'dict':  # test to see if the nodes are dictonaires, if not they are leaf nodes
                treePlotter.plotTree(secondDict[key], cntrPt, str(key))  # recursion
            else:  # it's a leaf node print the leaf node
                treePlotter.plotTree.xOff = treePlotter.plotTree.xOff + 1.0 / treePlotter.plotTree.totalW
                treePlotter.plotNode(secondDict[key], (treePlotter.plotTree.xOff, treePlotter.plotTree.yOff), cntrPt, leafNode)
                treePlotter.plotMidText((treePlotter.plotTree.xOff, treePlotter.plotTree.yOff), cntrPt, str(key))
                treePlotter.plotTree.yOff = treePlotter.plotTree.yOff + 1.0 / treePlotter.plotTree.totalD


    # if you do get a dictonary you know it's a tree, and the first element will be another dict

    def createPlot(inTree):
        fig = plt.figure(1, facecolor='white')
        fig.clf()
        axprops = dict(xticks=[], yticks=[])
        treePlotter.createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)  # no ticks
        # createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
        treePlotter.plotTree.totalW = float(treePlotter.getNumLeafs(inTree))
        treePlotter.plotTree.totalD = float(treePlotter.getTreeDepth(inTree))
        treePlotter.plotTree.xOff = -0.5 / treePlotter.plotTree.totalW;
        treePlotter.plotTree.yOff = 1.0;
        treePlotter.plotTree(inTree, (0.5, 1.0), '')
        plt.show()


    # def createPlot():
    #    fig = plt.figure(1, facecolor='white')
    #    fig.clf()
    #    createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
    #    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
    #    plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
    #    plt.show()

    def retrieveTree(i):
        listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                       {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                       ]
        return listOfTrees[i]

        # createPlot(thisTree)