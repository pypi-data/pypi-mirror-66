from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sympy import *
from math import *
from difdyf.util_func import *
import numpy as np

def plotFromCoord(coord,var,ranges,c='r',m='o'):# ranges: [range(l,h,step),range(l,h,step)...]
    assert(len(coord)==len(var) and len(var)==len(ranges))
    ndim=len(var)


    if ndim>3:
        print('dim should be lower than 4')
        return-1
    x = [0] * ndim
    sym = {}
    for i in range(ndim):
        sym[var[i]] = i
        x[i] = Symbol(var[i])
    for i in range(ndim):
        coord[i] = eval(changeVarName(coord[i], var, x))
    if ndim==3:
        x0=np.array([coord[0].subs([(x[0],y0),(x[1],y1),(x[2],y2)]) for y0 in ranges[0] for y1 in ranges[1] for y2 in ranges[2]],dtype=float)
        x1 = np.array([coord[1].subs([(x[0], y0), (x[1], y1), (x[2], y2)]) for y0 in ranges[0] for y1 in ranges[1] for y2 in
              ranges[2]],dtype=float)
        x2 = np.array([coord[2].subs([(x[0], y0), (x[1], y1), (x[2], y2)]) for y0 in ranges[0] for y1 in ranges[1] for y2 in
              ranges[2]],dtype=float)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x0, x1, x2,c=c,marker=m)
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.show()

        # for y1 in ranges[0]:
        #     for y2 in ranges[1]:
        #         for y3 in ranges[3]:




    return 0
# g,v=coord2MetricFromOrth(3,['r*cos(theta)*cos(phi)','r*cos(theta)*sin(phi)','r*sin(theta)'],['r','theta','phi'])














