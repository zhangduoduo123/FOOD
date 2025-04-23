import pandas as pd
from decimal import Decimal

from utils.util import find_non_numeric_loc, SEPARATOR_SAME_KIND, SEPARATOR_DIFF_KIND, SEPARATOR_FORBIDDEN_FOOD

# 食物成分表中的食物重量单位是100g，也就是每一百克食物的成分
DIVIDE_BY_WEIGHT = 100
# 每种食材的比例间隔
FOOD_PERCENT_INTERVAL = Decimal('0.2')
# 食物重量保留的小数点位数
SCALE = 1
# 饺子食材中除了营养成分的其他关键信息
FOOD_INFO_LIST = ['类别', '最大占比', '相似或相克']


def get_nutrition_file_data(nutrition_file_name, select_nutrition):
    nutrition_file = pd.read_csv(nutrition_file_name, encoding="gbk", index_col=0)
    nutrition_data = nutrition_file[select_nutrition]
    nutrition_data = nutrition_data.fillna(0)
    error_loc = find_non_numeric_loc(nutrition_data)
    if len(error_loc) > 0:
        print(error_loc)
        raise Exception
    nutrition_data[FOOD_INFO_LIST] = nutrition_file[FOOD_INFO_LIST]
    # print("饺子食材营养表：" + str(nutrition_data))
    return nutrition_data


def compute_nutrition_by_food_weight(nutrition_file_data, food_name, food_weight):
    nutrition = nutrition_file_data.loc[[food_name]]
    nutrition[nutrition.select_dtypes(include=['number']).columns] *= food_weight / DIVIDE_BY_WEIGHT
    nutrition = nutrition.loc[food_name]
    # print("食材：" + food_name + "，重量：" + str(food_weight) + "g，营养值：" + str(nutrition.to_dict()))
    return nutrition.to_dict()


def generate_food_list(nutrition_file_data, classifications):
    food_nutrition_list = nutrition_file_data.loc[nutrition_file_data['类别'].isin(classifications)]
    food_info = food_nutrition_list[FOOD_INFO_LIST]
    food_nutrition_list = food_nutrition_list.drop(FOOD_INFO_LIST, axis=1)
    # print(food_list)
    return food_nutrition_list, food_info


def generate_food_nutrition_data(data, index, food_list, food_info, total_weight_of_food, remain_num_of_food,
                                 current_food_index, food_remain_percent, single_food_min_percent, food_forbidden_list=[],
                                 current_food_name='', current_food_nutrition=0):
    for i in range(current_food_index, food_list.shape[0]):
        if food_list.index[i] in food_forbidden_list:
            continue
        food_max_percent = Decimal(str(food_info.iloc[i, 1]))
        if remain_num_of_food == 1:
            current_food_percent = food_remain_percent
            if current_food_percent > food_max_percent:
                continue
            final_food_name = current_food_name + food_list.index[i] + SEPARATOR_SAME_KIND + str(
                round(float(current_food_percent) * total_weight_of_food, SCALE))
            final_food_nutrition = current_food_nutrition + food_list.iloc[i,] * total_weight_of_food * float(
                current_food_percent) / DIVIDE_BY_WEIGHT
            data.append(dict(final_food_nutrition))
            index.append(final_food_name)
            continue
        for food_percent_num in \
                range(int((food_remain_percent - single_food_min_percent * (remain_num_of_food - 1)) / FOOD_PERCENT_INTERVAL)):
            current_food_percent = single_food_min_percent + food_percent_num * FOOD_PERCENT_INTERVAL
            if current_food_percent > food_max_percent:
                break
            current_food_forbidden = food_info.iloc[i, 2]
            next_forbidden_list = food_forbidden_list.copy()
            if not pd.isnull(current_food_forbidden):
                next_forbidden_list.extend(current_food_forbidden.split(SEPARATOR_FORBIDDEN_FOOD))
            next_food_name = current_food_name + food_list.index[i] + SEPARATOR_SAME_KIND + str(
                round(float(current_food_percent) * total_weight_of_food, SCALE)) + SEPARATOR_SAME_KIND
            next_food_nutrition = current_food_nutrition + food_list.iloc[i,] * total_weight_of_food * float(
                current_food_percent) / DIVIDE_BY_WEIGHT
            generate_food_nutrition_data(data, index, food_list, food_info, total_weight_of_food,
                                         remain_num_of_food - 1,
                                         i + 1, food_remain_percent - current_food_percent,
                                         single_food_min_percent,
                                         next_forbidden_list, next_food_name, next_food_nutrition)


def generate_food_nutrition_list(classifications, food_list, kind_num_of_food, weight_of_food, single_food_min_percent,
                                 output_file_path, food_info):
    data = []
    columns = food_list.columns
    index = []
    for i in range(kind_num_of_food):
        generate_food_nutrition_data(data, index, food_list, food_info, weight_of_food, i+1, 0, Decimal('1.0'), single_food_min_percent)
    food_nutrition_list = pd.DataFrame(data=data, columns=columns, index=index)
    output_file_name = output_file_path + "{}_营养成分.csv".format(str(classifications))
    food_nutrition_list.to_csv(output_file_name)
    return food_nutrition_list


def compute_nutrition_list(nutrition_file_data, classifications, kind_num_of_food, weight_of_food,
                           single_food_min_percent, output_file_path):
    food_list, food_info = generate_food_list(nutrition_file_data, classifications)
    food_nutrition_list = generate_food_nutrition_list(classifications, food_list, kind_num_of_food, weight_of_food,
                                                       single_food_min_percent, output_file_path, food_info)
    return food_nutrition_list


def compute_combine_nutrition_list(nutrition_list_flour, nutrition_list_meat, nutrition_list_vegetable,
                                   output_file_path):
    data = []
    columns = nutrition_list_flour.columns
    index = []
    for i in range(nutrition_list_flour.shape[0]):
        for j in range(nutrition_list_meat.shape[0]):
            for k in range(nutrition_list_vegetable.shape[0]):
                food_new_name = nutrition_list_flour.index[i] + SEPARATOR_DIFF_KIND + nutrition_list_meat.index[j] + SEPARATOR_DIFF_KIND + \
                                nutrition_list_vegetable.index[k]
                food_nutrition = nutrition_list_flour.iloc[i,] + nutrition_list_meat.iloc[j,] + \
                                 nutrition_list_vegetable.iloc[k,]
                data.append(dict(food_nutrition))
                index.append(food_new_name)
    food_nutrition_list = pd.DataFrame(data=data, columns=columns, index=index)
    output_file_name = output_file_path + "['综合']_营养成分.csv"
    food_nutrition_list.to_csv(output_file_name)
    return food_nutrition_list

