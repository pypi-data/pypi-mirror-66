from sympy import *
from difdyf.util_func import *
from difdyf.plotfig import *
import numpy as np

########### r theta phi      3-d sphere axis
n=3
[ginput, inputsym]=sphereMetric()
####################################################### init the metric field  ginput

T=getChristSymb(ginput,inputsym)
print(T)          #############################################get the christ symbol
T_dict=list2Dict(T,inputsym,listDepth(T))
R=getRiemannCurvature(T,inputsym) #####################################get the riemann curvature tensor
R_dict=list2Dict(R,inputsym,listDepth(R))
print(R_dict)
rici=getRici(T,inputsym)
print(rici)
T2=(np.array(T)[1:3,1:3,1:3]).tolist()
print(getRiemannCurvature(T2,inputsym[1:3]))



coord=['r*cos(theta)*cos(phi)','r*cos(theta)*sin(phi)','r*sin(theta)']
var=['r','theta','phi']
plotFromCoord(coord,var,[[1],np.linspace(-1.57,1.57,40),np.linspace(0,6.28,40)])
