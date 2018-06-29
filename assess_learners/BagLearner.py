"""
A simple wrapper for Bag Learner
"""

import numpy as np
import RTLearner as rt

class BagLearner(object):

    def __init__(self, learner=rt.RTLearner, kwargs = {"leaf_size":1}, bags = 20, boost = False, verbose = False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.learnerTrees = []
        self.verbose = verbose
        for i in range(0, bags):
            self.learnerTrees.append(learner(**kwargs))
    def author(self):
        return 'jpyneni3' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        if self.verbose == True:
            print "Bag Learner"
        for i in self.learnerTrees:
            sampledInds = np.random.randint(0, dataX.shape[0], size = dataX.shape[0] )
            #sampledInds = np.random.choice(a=dataX.shape[0], size = dataX.shape[0], replace = True)
            i.addEvidence(dataX[sampledInds], dataY[sampledInds])

    def query(self, points):
        queries = []
        for i in self.learnerTrees:
            queries.append(i.query(points))

        return np.mean(queries, axis = 0)
