import numpy as np

RI = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49, 11: 1.51}


# 层次分析法(AHP)定权重
def ahp_weight(data):
    data = np.array(data)
    m = len(data)

    # 计算特征向量
    weight = (data / data.sum(axis=0)).sum(axis=1) / m

    # 计算特征值
    Lambda = sum((weight * data).sum(axis=1) / (m * weight))

    # 判断一致性
    CI = (Lambda - m) / (m - 1)
    CR = CI / RI[m]

    if CR < 0.1:
        print(f'最大特征值：lambda = {Lambda}')
        print(f'特征向量：weight = {weight}')
        print(f'\nCI = {round(CI, 2)}, RI = {RI[m]} \nCR = CI/RI = {round(CR, 2)} < 0.1，通过一致性检验')
        return weight
    else:
        print(f'\nCI = {round(CI, 2)}, RI = {RI[m]} \nCR = CI/RI = {round(CR, 2)} >= 0.1，不满足一致性')
