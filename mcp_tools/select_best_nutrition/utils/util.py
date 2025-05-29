import os
SEPARATOR_DIFF_KIND = ';'
SEPARATOR_SAME_KIND = '_'
SEPARATOR_FORBIDDEN_FOOD = '_'

FLOUR = ["面粉"]
MEAT = ["牛肉", "猪肉", "羊肉", "海鲜", "鸡蛋", "鸡肉"]
VEGETABLE = ["蔬菜", "菌菇藻", "豆制品"]


def mkdir(path):
    if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


def find_non_numeric_loc(data):
    data_error_index = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            data_col = data.iloc[i, j]
            try:
                float(data_col)
            except Exception as e:
                data_error_index.append([i, j, str(data_col)])
    return data_error_index
