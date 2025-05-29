import pandas as pd

from process.nutrition_process import generate_food_list, FOOD_INFO_LIST, DIVIDE_BY_WEIGHT, SCALE
from process.topsis_process import compute_nutrition_best_value
from utils.util import SEPARATOR_DIFF_KIND, SEPARATOR_SAME_KIND, SEPARATOR_FORBIDDEN_FOOD, MEAT, VEGETABLE

ADJUST_PERCENT = 0.1


def get_food_info_from_name(food_name_str):
    content_list = food_name_str.split(SEPARATOR_SAME_KIND)
    food_name_list = []
    food_weight_list = []
    for i in range(len(content_list)):
        if (i % 2) == 0:
            food_name_list.append(content_list[i])
        else:
            food_weight_list.append(float(content_list[i]))
    return food_name_list, food_weight_list


def get_total_weight(food_weight_list):
    total_weight = 0.0
    for weight in food_weight_list:
        total_weight += weight
    return total_weight


def get_food_exclude_list(food_info, food_name_list):
    food_exclude_list = []
    for food_name in food_name_list:
        food_exclude_list.append(food_name)
        current_food_forbidden = food_info.loc[food_name, FOOD_INFO_LIST[2]]
        if not pd.isnull(current_food_forbidden):
            food_exclude_list.extend(current_food_forbidden.split(SEPARATOR_FORBIDDEN_FOOD))
    return list(set(food_exclude_list))


def get_food_main_kind(food_name_list, food_weight_list):
    max_food_index = 0
    max_food_weigt = food_weight_list[0]
    for i in range(1, len(food_weight_list)):
        if food_weight_list[i] > max_food_weigt:
            max_food_weigt = food_weight_list[i]
            max_food_index = i
    return food_name_list[max_food_index], max_food_index


def minus_main_kind(nutrition_best_value, food_main_kind, food_adjust_weight, food_nutrition_list):
    nutrition_best_value -= food_nutrition_list.loc[food_main_kind] * food_adjust_weight / DIVIDE_BY_WEIGHT


def get_food_nutrition_adjust_list(food_nutrition_list, food_adjust_weight, food_exclude_list, data, index):
    for i in range(food_nutrition_list.shape[0]):
        food_name = food_nutrition_list.index[i]
        if food_name in food_exclude_list:
            continue
        food_nutrition_value = food_nutrition_list.iloc[i,] * food_adjust_weight / DIVIDE_BY_WEIGHT
        data.append(dict(food_nutrition_value))
        index.append(food_name)


def get_food_name_from_info(food_name_list, food_weight_list):
    food_name_str = food_name_list[0] + SEPARATOR_SAME_KIND + str(round(food_weight_list[0], SCALE))
    for i in range(1, len(food_name_list)):
        food_name_str += SEPARATOR_SAME_KIND + food_name_list[i] + SEPARATOR_SAME_KIND + str(
            round(food_weight_list[i], SCALE))
    return food_name_str


def adjust_single_food_nutrition(food_name_str, food_nutrition_list, food_base_info, nutrition_best_value):
    food_name_list, food_weight_list = get_food_info_from_name(food_name_str)
    food_total_weight = get_total_weight(food_weight_list)
    food_adjust_weight = food_total_weight * ADJUST_PERCENT
    food_exclude_list = get_food_exclude_list(food_base_info, food_name_list)
    food_main_kind_name, food_main_kind_index = get_food_main_kind(food_name_list, food_weight_list)
    food_main_kind_weight = food_weight_list[food_main_kind_index]
    data = []
    columns = food_nutrition_list.columns
    index = []
    if food_main_kind_weight > food_adjust_weight:
        food_weight_list[food_main_kind_index] = food_main_kind_weight - food_adjust_weight
        minus_main_kind(nutrition_best_value, food_main_kind_name, food_adjust_weight, food_nutrition_list)
        get_food_nutrition_adjust_list(food_nutrition_list, food_adjust_weight, food_exclude_list, data, index)
        food_name_str = get_food_name_from_info(food_name_list, food_weight_list)
    food_nutrition_adjust_list = pd.DataFrame(data=data, columns=columns, index=index)
    return food_nutrition_adjust_list, food_name_str, food_adjust_weight


def compute_stuffing_adjust_nutrition(meat_nutrition_adjust_list, vegetable_nutrition_adjust_list, nutrition_best_value,
                                      flour_name_str, meat_new_name, vegetable_new_name, meat_adjust_weight,
                                      vegetable_adjust_weight):
    data = []
    columns = meat_nutrition_adjust_list.columns
    index = []
    for i in range(meat_nutrition_adjust_list.shape[0]):
        for j in range(vegetable_nutrition_adjust_list.shape[0]):
            meat_name_str = meat_new_name + SEPARATOR_SAME_KIND + meat_nutrition_adjust_list.index[
                i] + SEPARATOR_SAME_KIND + str(
                round(meat_adjust_weight, SCALE))
            vegetable_name_str = vegetable_new_name + SEPARATOR_SAME_KIND + vegetable_nutrition_adjust_list.index[
                j] + SEPARATOR_SAME_KIND + str(round(vegetable_adjust_weight, SCALE))
            food_new_name = flour_name_str + SEPARATOR_DIFF_KIND + meat_name_str + SEPARATOR_DIFF_KIND + vegetable_name_str
            nutrition_new_value = nutrition_best_value + meat_nutrition_adjust_list.iloc[i,] + \
                                  vegetable_nutrition_adjust_list.iloc[j,]
            index.append(food_new_name)
            data.append(nutrition_new_value.to_dict())
    stuffing_adjust_nutrition = pd.DataFrame(data=data, columns=columns, index=index)
    return stuffing_adjust_nutrition


def adjust_stuffing_nutrition(food_name_str, nutrition_best_value, RNI_range, nutrition_file_data):
    flour_name_str = food_name_str.split(SEPARATOR_DIFF_KIND)[0]

    meat_nutrition_list, meat_base_info = generate_food_list(nutrition_file_data, MEAT)
    meat_name_str = food_name_str.split(SEPARATOR_DIFF_KIND)[1]
    meat_nutrition_adjust_list, meat_new_name, meat_adjust_weight = adjust_single_food_nutrition(meat_name_str,
                                                                                                 meat_nutrition_list,
                                                                                                 meat_base_info,
                                                                                                 nutrition_best_value)

    vegetable_nutrition_list, vegetable_base_info = generate_food_list(nutrition_file_data, VEGETABLE)
    vegetable_name_str = food_name_str.split(SEPARATOR_DIFF_KIND)[2]
    vegetable_nutrition_adjust_list, vegetable_new_name, vegetable_adjust_weight = adjust_single_food_nutrition(
        vegetable_name_str, vegetable_nutrition_list,
        vegetable_base_info,
        nutrition_best_value)
    return compute_stuffing_adjust_nutrition(meat_nutrition_adjust_list,
                                             vegetable_nutrition_adjust_list, nutrition_best_value,
                                             flour_name_str, meat_new_name, vegetable_new_name,
                                             meat_adjust_weight, vegetable_adjust_weight)


def adjust_nutrition_list(nutrition_best_value_list, RNI_range, nutrition_file_data, output_file_path, weight,
                          nutrition_filter=None, best_value_num=1, min_score=0.9, iter_num=1):
    adjust_result = nutrition_best_value_list.copy()
    for i in range(nutrition_best_value_list.shape[0]):
        nutrition_best_value = nutrition_best_value_list.iloc[i,].copy()
        food_name_str = nutrition_best_value_list.index[i]
        stuffing_adjust_nutrition = adjust_stuffing_nutrition(food_name_str, nutrition_best_value, RNI_range,
                                                              nutrition_file_data)
        adjust_result = pd.concat([adjust_result, stuffing_adjust_nutrition])
    classification = ["综合_调整" + str(iter_num)]
    output_file_name = output_file_path + "{}_营养成分.csv".format(str(classification))
    adjust_result.to_csv(output_file_name)
    adjust_best_value_list = compute_nutrition_best_value(classification, adjust_result, RNI_range, output_file_path,
                                                          weight, nutrition_filter, best_value_num, min_score)
    return adjust_best_value_list
