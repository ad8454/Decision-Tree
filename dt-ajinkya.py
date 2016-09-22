import sys
import math
import pickle
import csv
import numpy as np
from Tree_Model import Tree
from test import test

def isNum(val):
  try:
    float(val)
    return True
  except ValueError:
    return False

def rec(data, attributes, depth=0, outcome=None):
    if len(attributes) == 1 or len(data) < 1:
        print '\t'*depth + outcome
        myNode = Tree()
        myNode.name = attributes[-1]
        myNode.val = outcome
        return myNode

    binEdges, binFreq, allBinIndices = getDataInfo(data, attributes)
    if len(allBinIndices)+1 < len(attributes):
        print '\t'*depth + binEdges[-1][np.argmax(binFreq[-1])]
        myNode = Tree()
        myNode.name = attributes[-1]
        myNode.val = binEdges[-1][np.argmax(binFreq[-1])]
        return myNode
    iGain = getInfoGain(data, binEdges, binFreq, allBinIndices, attributes)
    nodeIndex = iGain.index(max(iGain))

    myNode = Tree()
    myNode.name = attributes[nodeIndex]

    print '\t'*depth + attributes[nodeIndex]
    data = np.delete(data, nodeIndex, 1)
    attributes = np.delete(attributes, nodeIndex)
    for j in range(len(binEdges[nodeIndex]) - 1):
        print '\t'*depth + str(binEdges[nodeIndex][j]) +' - '+ str(binEdges[nodeIndex][j+1]) + ':'
        child = rec(np.asarray([data[idx] for idx in np.where(allBinIndices[nodeIndex] == j+1)[0]]),
            attributes, depth + 1, binEdges[-1][np.argmax(binFreq[-1])])
        myNode.children.append(child)
        myNode.binMin.append(binEdges[nodeIndex][j])
        myNode.binMax.append(binEdges[nodeIndex][j+1])
        #print myNode.binMax
    return myNode

def getDataInfo(data, attributes):
    binEdges = []
    binFreq = []
    allBinIndices = []
    thresh = 5
    #print '--->' + str(data.shape) + str(len(data))
    for i in range(len(attributes)):
        col = data[:, i]
        colUnique = np.unique(col, return_counts=True)
        if colUnique[0].size > thresh and isNum(colUnique[0][0]):
            float_col = [float(i) for i in col]
            ret = np.asarray(np.histogram(float_col, thresh))
            colUnique = ret[1], ret[0]
            ret[1][-1] += 0.1
            allBinIndices.append(np.digitize(float_col, ret[1]))

        binEdges.append(colUnique[0])
        binFreq.append(colUnique[1])

    return binEdges, binFreq, allBinIndices

def getInfoGain(data, binEdges, binFreq, allBinIndices, attributes):
    total = float(len(data))

    entropy = 0.
    lastAttr = binFreq[-1]
    for j in range(len(lastAttr)):
        p = lastAttr[j] / total
        entropy += - (p * math.log(p, 2))


    iGain = []
    for i in range(len(attributes)-1):
        sum = 0
        for j in range(len(binEdges)-1):
            if binFreq[i][j] == 0:
                continue
            prod = binFreq[i][j]/total
            diff = 0
            for k in binEdges[-1]:      #because last element is to be predicted
                l1 = np.where(allBinIndices[i] == j+1)
                l2 = np.where(data[:, -1] == k)
                p = len(np.intersect1d(l1, l2)) / float(binFreq[i][j])
                if p > 0:
                    diff += - (p * math.log(p, 2))

            sum += (prod*diff)
        iGain.append(entropy - sum)
    return iGain

def main():

    job = sys.argv[1]
    fn = sys.argv[2]
    if job == '-test':
        with open('ET-ajinkya.pickle','rb') as h:
            root = pickle.load(h)
        list = []
        with open(fn, 'rb') as csvfile:
            inputData = csv.reader(csvfile, delimiter=',')
            for row in inputData:
                list.append(row)
        print (root.Accuracy(list, root))
        #root.ConfusionMatrix(list)

    elif job == '-train':
        print 'here'
        list = []
        with open(fn, 'rb') as csvfile:
            inputData = csv.reader(csvfile, delimiter=',')
            for row in inputData:
                list.append(row)

        data = np.asarray(list)
        attributes = data[0]
        data = np.delete(list, 0, 0)

        print 'Decision Tree:'
        root = rec(data, attributes)


        with open('ET-ajinkya.pickle','wb') as h:
            pickle.dump(root,h)




if __name__ == '__main__':
   main()