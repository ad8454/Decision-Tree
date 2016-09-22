import numpy as np

class Tree():
    
    def __init__(self):
        self.name = None
        self.children = []
        self.binMin = []
        self.binMax = []
        self.val = None
    
    def train(self,trainData):
        #Attributes/Last Column is class
        self.createTree(trainData)
    
    def createTree(self,trainData):
        self.treemodel=None
        #create the tree

    def predict(self,testData):
        #testData does not have the class column
        #returns list of the predicted output
        return []

    def Accuracy(self, list, root):
        #Last Column comtains the class
        data = np.asarray(list)
        attributes = data[0]
        data = np.delete(data, 0, 0)
        results = []
        correct = 0


        classes = np.unique(data[:, -1])
        conMatrix = [[0]* (len(classes))]* (len(classes))
        conMatrix = np.asarray(conMatrix)
        for row in data:
            ans = self.dfs(row, attributes, root)
            results.append(ans)
            if ans == row[-1]:
                index = np.where(classes[:] == ans)[0][0]  #classes.index(ans)
                conMatrix[index][index]+=1
                correct+=1
            else:
                i = np.where(classes[:] == ans)[0][0]
                j = np.where(classes[:] == row[-1])[0][0]
                conMatrix[i][j]+=1


        print 'Confusion Matrix:'
        print classes
        np.append(conMatrix, classes.reshape((len(classes), 1)), 1)
        print conMatrix
        acc = correct / float(len(data))
        return 'Accuracy: '+ str(acc)
    
    def ConfusionMatrix(self, list, root):
        #print confusion Matrix 
        #last column has the class value
        pass

    def dfs(self, row, attributes, node):
        if node.name == attributes[-1]:
            return node.val
        field = np.where(attributes[:] == node.name)[0][0] # attributes.index(node.name)
        #print field
        for i in range(len(node.binMax)):
            #print row[field], node.binMax[i], float(row[field]) < node.binMax[i]
            if float(row[field]) < node.binMax[i]:
                node = node.children[i]
                break
        return self.dfs(row, attributes, node)
         
