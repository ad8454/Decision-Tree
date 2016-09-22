import pickle
import csv

def test(fn):
    with open('ET-ajinkya.pickle','rb') as h:
        root = pickle.load(h)


    with open(fn, 'rb') as csvfile:
        testData = csv.reader(csvfile, delimiter=',')
        for row in testData:
            list.append(row)
    print(root.accuracy(list, root))
    root.ConfusionMatrix(list)
