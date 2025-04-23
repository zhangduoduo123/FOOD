# 极小型指标：期望指标值越小越好（如患病率、死亡率等）
from topsis.topsis import topsis

FILTER_MIN_NUM = 20
FILTER_STEP = 0.01


def data_direction_1(datas, offset=0):
    def normalization(data):
        return 1 / (data + offset)

    return list(map(normalization, datas))


# 中间型指标：期望指标值既不要太大也不要太小，适当取中间值最好（如水质量评估 PH 值），其中x_max为指标x的可能取值的最大值，x_min为指标x的可能取值的最小值
def data_direction_2(datas, x_min, x_max):
    def normalization(data):
        if data <= x_min or data >= x_max:
            return 0
        elif x_min < data < (x_min + x_max) / 2:
            return 2 * (data - x_min) / (x_max - x_min)
        elif x_max > data >= (x_min + x_max) / 2:
            return 2 * (x_max - data) / (x_max - x_min)

    return list(map(normalization, datas))


# 区间型指标：期望指标的取值最好落在某一个确定的区间最好（如体温），其中[x_min, x_max]为指标x的最佳稳定区间，[x_minimum, x_maximum]为最大容忍区间
def data_direction_3(datas, x_min, x_max, x_minimum, x_maximum):
    def normalization(data):
        if x_min <= data <= x_max:
            return 1
        elif data <= x_minimum or data >= x_maximum:
            return 0
        elif x_max < data < x_maximum:
            return 1 - (data - x_max) / (x_maximum - x_max)
        elif x_min > data > x_minimum:
            return 1 - (x_min - data) / (x_min - x_minimum)

    return list(map(normalization, datas))


def do_filter(nutrition_list, nutrition_filters, min_score=0.9):
    FILTER_MIN_SCORE = min_score / 2
    while True:
        nutrition_list_clone = nutrition_list.copy()
        for nutrition_filter in nutrition_filters:
            nutrition_list_clone = nutrition_list_clone.loc[(nutrition_list_clone[nutrition_filter] >= min_score)]
        if nutrition_list_clone.shape[0] < FILTER_MIN_NUM and min_score > FILTER_MIN_SCORE:
            min_score -= FILTER_STEP
        else:
            return nutrition_list_clone


def compute_nutrition_best_value(classifications, nutrition_list, RNI_range, output_file_path, weight,
                                 nutrition_filter=None, best_value_num=1, min_score=0.9):
    nutrition_list_clone = nutrition_list.copy()
    for key in RNI_range:
        RNI_maximum = RNI_range[key][1] + 20 * (RNI_range[key][1] - RNI_range[key][0])
        RNI_minimum = RNI_range[key][0] - 20 * (RNI_range[key][1] - RNI_range[key][0])
        nutrition_list_clone[key] = data_direction_3(nutrition_list_clone[key], RNI_range[key][0], RNI_range[key][1],
                                                     RNI_minimum, RNI_maximum)
    output_file_name = output_file_path + "{}_营养打分.csv".format(str(classifications))
    nutrition_list_clone.to_csv(output_file_name)
    if nutrition_filter is not None:
        nutrition_list_clone = do_filter(nutrition_list_clone, nutrition_filter, min_score)
        output_file_name = output_file_path + "{}_筛选后营养打分.csv".format(str(classifications))
        nutrition_list_clone.to_csv(output_file_name)
    Result, Z, weight = topsis(nutrition_list_clone, weight)
    print(str(classifications) + '营养权值为：' + str(weight))
    Result = Result.fillna(value=0)
    output_file_name = output_file_path + "{}_topsis排名.csv".format(str(classifications))
    Result.to_csv(output_file_name)
    best_result = Result.loc[Result['排序'] <= best_value_num]
    if best_result.empty:
        raise Exception("没有找到符合条件的营养组合")
    if best_value_num > 1:
        nutrition_best_food = best_result.index.values
        nutrition_best_value = nutrition_list.loc[nutrition_best_food]
        print('{}营养最优搭配前{}名为：'.format(str(classifications), str(best_value_num)))
        print(nutrition_best_food)
        print('营养值为：')
        print(nutrition_best_value)
        return nutrition_best_value
    nutrition_best_food = best_result.index.values[0]
    nutrition_best_value = nutrition_list.loc[nutrition_best_food]
    print(str(classifications) + '营养最优搭配为：' + nutrition_best_food)
    # print('营养值为：' + str(nutrition_best_value))
    return nutrition_best_value.to_dict()
