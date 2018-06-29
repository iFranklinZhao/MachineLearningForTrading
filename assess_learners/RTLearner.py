"""
A simple wrapper for Random Decision Tree
"""

import numpy as np

class RTLearner(object):

    def __init__(self, leaf_size=1, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = np.ndarray(shape=(0,4))
        self.treesize = 0

    def author(self):
        return 'jpyneni3' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        # slap on 1s column so linear regression finds a constant term
        #newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1])
        #newdataX[:,0:dataX.shape[1]]=dataX

        # build and save the model
        #self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY)
        if self.verbose == True:
            print "RT Learner"
        self.buildTree(dataX, dataY)

    def buildTree(self, xdata, ydata):
        if (xdata.shape[0]<self.leaf_size or ydata.shape[0]<self.leaf_size):
            rowVals = [np.NaN, np.mean(ydata), -1, -1]
            self.tree = np.vstack((self.tree,rowVals))
            self.treesize += 1
            return
        if(np.all(ydata[0] == ydata[:], axis=0)):
            rowVals = [np.NaN, ydata[0], -1, -1]
            self.tree = np.vstack((self.tree,rowVals))
            self.treesize += 1
            return
        correlationList = []
        splitIndex = np.random.randint(0, xdata.shape[1])
        if(np.all(xdata[0,splitIndex] == xdata[:,splitIndex], axis=0)):
            rowVals = [np.NaN,np.mean(ydata), -1, -1]
            self.tree = np.vstack((self.tree,rowVals))
            self.treesize += 1
            return
        splitVal = np.median(xdata[:,splitIndex])
        leftInd = xdata[:,splitIndex] <= splitVal
        rightInd= xdata[:,splitIndex] > splitVal
        xdleft = xdata[leftInd,:]
        ydleft = ydata[leftInd]
        xdright = xdata[rightInd,:]
        ydright = ydata[rightInd]
        if (xdleft.shape[0]<self.leaf_size or ydright.shape[0]<self.leaf_size):
            rowVals = [np.NaN, np.mean(ydata), -1, -1]
            self.tree = np.vstack((self.tree,rowVals))
            self.treesize += 1
            return
        rowVals = [splitIndex, splitVal, 1, -1]
        self.tree = np.vstack((self.tree,rowVals))
        self.treesize += 1
        currTreesize = self.treesize
        self.buildTree(xdleft,ydleft)
        newTreesize = self.treesize
        self.tree[currTreesize-1, 3] = (newTreesize - currTreesize) + 1
        self.buildTree(xdright,ydright)

    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        retList = []
        #print self.tree
        for j in range(len(points)):
            i = 0
            while(not np.isnan(self.tree[int(i),0])):
                if (points[j, int(self.tree[int(i),0])]) <= self.tree[int(i),1]:
                    i += 1
                else:
                    i += int(self.tree[i,3])
            retList.append(self.tree[i,1])
        return retList

#        return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
