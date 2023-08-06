# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import numpy as np
import matplotlib.pyplot as plt
from .functions import *


def plotTSE(h, dim=10, nTriples=10, nThetas=100, R=1, onSimplex=True, 
            randseed=-1):
    """
    Plot estimated triangle scaling exponents of Bregman distance.
    """
    
    if randseed >= 0:
        np.random.seed(randseed)
    
    plt.figure()
    
    for k in range(nTriples):
        x = R * np.random.rand(dim)
        y = R * np.random.rand(dim)
        z = R * np.random.rand(dim)
        if onSimplex:
            x = x / x.sum()
            y = y / y.sum()
            z = z / z.sum()
            
        theta = np.arange(1.0/nThetas, 1, 1.0/nThetas)
        expnt = np.zeros(theta.shape)
        dyz = h.divergence(y, z)

        for i in range(theta.size):
            c = theta[i]
            dtheta = h.divergence((1-c)*x+c*y, (1-c)*x+c*z)
            expnt[i] = np.log(dtheta / dyz) / np.log(c)
            #expnt[i] = (np.log(dtheta) - np.log(dyz)) / np.log(c)
        plt.plot(theta, expnt)

    plt.xlim([0,1])
    #plt.ylim([0,5])
    #plt.xlabel(r'$\theta$')
    #plt.ylabel(r'$\hat{\gamma}(\theta)$')
    plt.tight_layout()

    
def plotTSE0(h, dim=10, xscale=1, yscale=1, zscale=2, nThetas=1000, maxTheta=1):
    """
    Plot estimated triangle scaling exponents of Bregman distance.
    """
    
    plt.figure()
    
    # test for extreme cases
    #x = np.zeros(dim)
    x = xscale*np.ones(dim)
    #x = np.random.rand(dim)
    y = yscale*np.ones(dim)
    z = zscale*np.ones(dim)
    #y = yscale*np.random.rand(dim)
    #z = zscale*np.random.rand(dim)

    theta = np.arange(1.0/nThetas, maxTheta, 1.0/nThetas)
    expnt = np.zeros(theta.shape)
    dyz = h.divergence(y, z)

    for i in range(theta.size):
        c = theta[i]
        dtheta = h.divergence((1-c)*x+c*y, (1-c)*x+c*z)
        expnt[i] = np.log(dtheta / dyz) / np.log(c)
        #expnt[i] = (np.log(dtheta) - np.log(dyz)) / np.log(c)
    plt.plot(theta, expnt)

    plt.xlim([0,maxTheta])
    #plt.ylim([0,5])
    #plt.xlabel(r'$\theta$')
    #plt.ylabel(r'$\hat{\gamma}(\theta)$')
    plt.tight_layout()
    

if __name__ == "__main__":

    #h = ShannonEntropy()
    #h = BurgEntropy()
    h = PowerNeg1()
    #h = SquaredL2Norm()
    #h = SumOf2nd4thPowers(1)

    plotTSE(h, nThetas=1000)
    #plotTSE0(h, xscale=1e-8, yscale=10, zscale=20, nThetas=10000, maxTheta=1e-2)
