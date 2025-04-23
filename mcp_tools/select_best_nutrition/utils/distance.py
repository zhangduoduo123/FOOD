import numpy as np
import pandas as pd


# 欧氏距离
def euclidean_distance(x, y):
    return np.linalg.norm(x - y)


# 余弦距离
def cosine_distance(x, y):
    return x.dot(y) / (np.linalg.norm(x) * np.linalg.norm(y))


datas = pd.DataFrame(data=[[1,2,3],[4,4,4],[2,4,6],[-1,-2,-4]], columns=['a', 'b', 'c'], index=[1, 2, 3, 4])
print(cosine_distance(datas.iloc[0,], datas.iloc[3,]))
