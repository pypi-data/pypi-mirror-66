# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# plt.show()
####################################################### curve
# from mpl_toolkits.mplot3d import Axes3D
# import numpy as np
# import matplotlib.pyplot as plt
#
# fig = plt.figure()
# ax = fig.gca(projection='3d')
#
# # Prepare arrays x, y, z
# theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
# z = np.linspace(-2, 2, 100)
# r = z**2 + 1
# x = r * np.sin(theta)
# y = r * np.cos(theta)
#
# ax.plot(x, y, z, label='parametric curve')  #这里传入x, y, z的值
# ax.legend()
#
# plt.show()
############################################################### discreate points
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)


def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 100

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
# 迭代两次，分别绘制两种不同的散点，一种是（红色，小圆圈，z坐标取值范围(-50, -25)），另一种是（蓝色，小三角，z坐标取值范围(-30, -5)）。
for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zlow, zhigh)
    ax.scatter(xs, ys, zs, c=c, marker=m)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()

# x=np.array([[1,0,0],[0,0.5,0],[0,0,1]])
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1, projection='3d')
# for i in range(x.shape[0]):
#     ax.text(x[i, 0], x[i, 1], x[i, 2], str(1),
#             color='r',
#             fontdict={'weight': 'bold', 'size': 9})
# ax.view_init(20, 0)  # 只有这一行改变了
# plt.show()
# # 关键就是函数ax.view_init()函数的调用
# # 该函数接受两个参数，第一个参数是竖直旋转，第二个参数是水平旋转，旋转单位是度°
# # 默认的初始角度是ax.view_init(30, -60)
