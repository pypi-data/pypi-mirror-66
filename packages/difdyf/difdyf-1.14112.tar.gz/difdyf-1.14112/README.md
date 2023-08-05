# difdyf


calculate differential geometry content


`difdyf` 是一个计算不同度规场，坐标系下各种张量的库

更多功能正在添加中


### 使用方式

```
import difdyf as df
g,symb=df.sphereMetric()## 生成球坐标度规场g，symb=【'r','theta','phi'】
T=df.getChristSymb(g,symb)## 生成球坐标下克氏算符
R=df.getRiemannCurvature(T,symb)## 生成球坐标表示的R3空间黎曼曲率张量，和正交坐标表示的R3曲率一样，为0
##输入度规场g可任意指定，需要是一个2维字符串值的字典，例如g['r']['r']='1'
```
### 内部函数
```
df.sphereMetric()## 生成球坐标度规场g，symb=【'r','theta','phi'】
df.orthMetric(n)## 生成n维正交度规场g，symb=【'x0','x1',... ,'xn'】
df.getChristSymb(g,symb)## 生成度规场下的克氏算符
df.getRiemannCurvature(T,symb)## 生成黎曼曲率
df.getRici(T,symb)##里奇张量
df.coord2MetricFromOrth(n,coordList,varlist)## 生成不同坐标系的度规场
                                               n为空间维度（整数）
                                               coordList为坐标表示式 i.e.['r*cos(theta)*cos(phi)','r*cos(theta)*sin(phi)','r*sin(theta)']
                                                    需要是一个n维列表，列表每一个字符串依次代表x0，x1,..., xn在新坐标系中的表示式
                                               varlist为新坐标名字 i.e. ['r','theta','phi']
df.plotFromCoord(coord,symb,ranges)# 生成指定坐标系（3维）在正交坐标下的象
                                    coord=['r*cos(theta)*cos(phi)','r*cos(theta)*sin(phi)','r*sin(theta)']
                                    var=['r','theta','phi']
                                    ranges：坐标范围
                       i.e. df.plotFromCoord(coord,var,[[1],np.linspace(-1.57,1.57,40),np.linspace(0,6.28,40)])




```

### 安装

```
$ pip install difdyf
```