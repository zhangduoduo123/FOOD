import pandas as pd
import numpy as np

from topsis.ahpWeight import ahp_weight
from topsis.entropyWeight import entropy_weight


def topsis(data, weight=None, weight_method='entropy_weight'):
    # 归一化
    data = data / np.sqrt((data ** 2).sum())

    # 最优最劣方案
    Z = pd.DataFrame([data.min(), data.max()], index=['负理想解', '正理想解'])

    # 距离
    if weight is None:
        if weight_method == 'entropy_weight':
            weight = entropy_weight(data)
        else:
            weight = ahp_weight(data)
    else:
        weight = np.array(weight)

    Result = data.copy()
    Result['正理想解'] = np.sqrt(((data - Z.loc['正理想解']) ** 2 * weight).sum(axis=1))
    Result['负理想解'] = np.sqrt(((data - Z.loc['负理想解']) ** 2 * weight).sum(axis=1))

    # 综合得分指数
    Result['综合得分指数'] = Result['负理想解'] / (Result['负理想解'] + Result['正理想解'])
    Result['排序'] = Result.rank(ascending=False)['综合得分指数']

    return Result, Z, weight
