"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
import LinRegLearner as lrl
import sys
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
import time

if __name__=="__main__":
    if len(sys.argv) != 2:
        print "Usage: python testlearner.py <filename>"
        sys.exit(1)
    #inf = open(sys.argv[1])
    #data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
    try:
	inf = open(sys.argv[1])
        data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
    except ValueError:
        inf = open(sys.argv[1])
        data = np.array([map(float,s.strip().split(',')[1:]) for s in inf.readlines()[1:]])

    # compute how much of the data is training and testing
    train_rows = int(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]

    #print testX.shape
    #print testY.shape
    #get 1 - 100 leaf size
    file = open('istanbulDT.csv', 'w')
    file.write('Decision Tree Learner Runtime\n')
    file.write('Leaf Size, Time\n')
    overallStart = time.time()
    for i in range(1,10,1)+[i for i in range(10, 101, 10)]:

        learner = dt.DTLearner(verbose = False, leaf_size=i)
        learner.addEvidence(trainX, trainY) # train it


        # evaluate in sample
        startTime = time.time()
        predY = learner.query(trainX) # get the predictions
        endTime = time.time()
        traintime = endTime-startTime
        trainrmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        trainc = np.corrcoef(predY, y=trainY)[0,1]
        # print "corr: ", c[0,1]

        # evaluate out of sample
        startTime = time.time()
        predY = learner.query(testX) # get the predictions
        endTime = time.time()
        testtime = endTime-startTime
        testrmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        testc = np.corrcoef(predY, y=testY)[0,1]
        file.write('{},{},{},{}\n'.format(i, traintime, testtime, learner.tree.shape[0]))

    file.close()
    overallEndTime = time.time()
    print "DT Overall {}".format(overallEndTime - overallStart)

    file = open('istanbulRT.csv', 'w')
    file.write('Random Tree Learner Runtime\n')
    file.write('Leaf Size,Train RMSE, Test RMSE, \n')
    overallStart = time.time()
    for i in range(1,10,1)+[i for i in range(10, 101, 10)]:
        learner = rt.RTLearner(verbose = False, leaf_size=i)
        learner.addEvidence(trainX, trainY) # train it


        # evaluate in sample
        startTime = time.time()
        predY = learner.query(trainX) # get the predictions
        endTime = time.time()
        traintime = endTime-startTime
        trainrmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        trainc = np.corrcoef(predY, y=trainY)[0,1]
        # print "corr: ", c[0,1]

        # evaluate out of sample
        startTime = time.time()
        predY = learner.query(testX) # get the predictions
        endTime = time.time()
        testtime = endTime-startTime
        testrmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        testc = np.corrcoef(predY, y=testY)[0,1]
        totalTime = endTime - startTime
        file.write('{},{},{},{}\n'.format(i, traintime, testtime, learner.tree.shape[0]))

    file.close()
    overallEndTime = time.time()
    print "RT Overall {}".format(overallEndTime - overallStart)

    # create a learner and train it
    #learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner
    #learner = dt.DTLearner(leaf_size =9, verbose = True)
    #learner.addEvidence(trainX, trainY) # train it
    #print learner.author()

    # evaluate in sample
    #predY = learner.query(trainX) # get the predictions
    #rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    #print
    #print "In sample results"
    #print "RMSE: ", rmse
    #c = np.corrcoef(predY, y=trainY)
    #print "corr: ", c[0,1]

    # evaluate out of sample
    #predY = learner.query(testX) # get the predictions
    #rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    #print
    #print "Out of sample results"
    #print "RMSE: ", rmse
    #c = np.corrcoef(predY, y=testY)
    #print "corr: ", c[0,1]
