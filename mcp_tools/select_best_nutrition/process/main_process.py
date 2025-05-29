from process.RNI_process import get_RNI_range
from process.adjust_process import adjust_nutrition_list
from process.nutrition_process import get_nutrition_file_data, compute_nutrition_by_food_weight, compute_nutrition_list, \
    compute_combine_nutrition_list
from process.topsis_process import compute_nutrition_best_value
from utils.util import mkdir, FLOUR, MEAT, VEGETABLE
from decimal import Decimal

# 调整营养值的循环次数
ADJUST_ITER_NUM = 0

def main_process(RNI_range, num_of_dumpling, meat_percent, output_file_path, input_file_path, dumpling_skin_percent, select_nutrition):
    """
    饺子营养优化的主处理函数
    
    Args:
        RNI_range: 营养素推荐摄入量范围
        num_of_dumpling: 饺子数量
        meat_percent: 肉馅比例
        output_file_path: 输出文件路径
        dumpling_skin_percent: 饺子皮占比
        select_nutrition: 需要优化的营养素列表
    
    Returns:
        优化后的营养值列表
    """
    print("饺子个数：" + str(num_of_dumpling))
    print("肉类占比：" + str(meat_percent))
    mkdir(output_file_path)
    # 1、定义输入数据
    # 人体所需营养-文件名
    RNI_file_name = input_file_path + "RNI.csv"
    # 饺子食材的营养含量-文件名
    nutrition_file_name = input_file_path + "饺子食材食物成分表1.csv"
    nutrition_file_name2 = input_file_path + "饺子食材食物成分表2.csv"
    # 营养成分重要性
    weight = [0.175, 0.175, 0.175, 0.175, 0.05, 0.01, 0.01, 0.05, 0.05, 0.04, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
              0.01, 0.01]
    # weight = None
    # 单个饺子=25g；面皮占比=12/25；面粉占比面皮=1/1.4
    weight_of_per_dumpling = 25
    # dumpling_skin_percent = 12 / 25
    flour_percent = 1 / 1.4
    # 饺子皮重
    weight_of_dumpling_skin = weight_of_per_dumpling * num_of_dumpling * dumpling_skin_percent
    # 饺子馅重
    weight_of_dumpling_stuffing = weight_of_per_dumpling * num_of_dumpling * (1 - dumpling_skin_percent)
    # 面粉重
    weight_of_flour = weight_of_dumpling_skin * flour_percent
    # 花生油占比馅=50/1800；姜占比馅=15/1800；盐占比馅=7/1800；酱油占比馅=45/1800；味精占比馅=5/1800；胡椒粉占比馅=5/1800
    weight_of_peanut_oil = weight_of_dumpling_stuffing * (50 / 1800)
    weight_of_ginger = weight_of_dumpling_stuffing * (15 / 1800)
    weight_of_salt = weight_of_dumpling_stuffing * (7 / 1800)
    weight_of_soy_sauce = weight_of_dumpling_stuffing * (45 / 1800)
    weight_of_MSG = weight_of_dumpling_stuffing * (5 / 1800)
    weight_of_pepper = weight_of_dumpling_stuffing * (5 / 1800)
    # 肉+菜占比馅=1600/1800
    meat_and_vegetable_percent = 1600 / 1800
    # 肉+菜重
    meat_and_vegetable_weight = weight_of_dumpling_stuffing * meat_and_vegetable_percent

    # 2、获取所需营养范围和饺子食材营养成分表
    RNI_range = get_RNI_range(RNI_range, select_nutrition)
    nutrition_file_data = get_nutrition_file_data(nutrition_file_name, select_nutrition)
    nutrition_file_data2 = get_nutrition_file_data(nutrition_file_name2, select_nutrition)

    # 3、减去固定成分的营养
    weight_of_fixed_component = {"花生油": weight_of_peanut_oil, "姜": weight_of_ginger, "盐": weight_of_salt,
                                 "酱油": weight_of_soy_sauce, "味精": weight_of_MSG, "胡椒粉": weight_of_pepper}
    for key in weight_of_fixed_component:
        RNI_fixed_food_value = compute_nutrition_by_food_weight(nutrition_file_data, key,
                                                                weight_of_fixed_component[key])
        for nutrition in select_nutrition:
            RNI_range[nutrition] = [item - RNI_fixed_food_value[nutrition] for item in RNI_range[nutrition]]
    print("添加调料后，剩余所需营养范围：" + str(RNI_range))

    # 4、计算面粉搭配
    classifications = FLOUR
    # 面粉种类个数
    kind_num_of_flour = 1
    # 每种面粉最低占比
    single_flour_min_percent = Decimal('0.2')
    # 计算不同搭配的面粉营养值
    nutrition_list_flour = compute_nutrition_list(nutrition_file_data, classifications, kind_num_of_flour,
                                                  weight_of_flour,
                                                  single_flour_min_percent, output_file_path)

    # 5、计算肉馅搭配
    # 定义肉馅包含哪些类别
    classifications = MEAT
    # 肉馅重量
    weight_of_meat = meat_and_vegetable_weight * meat_percent
    # 肉馅种类个数
    kind_num_of_meat = 1
    # 每种肉馅最低占比
    single_meat_min_percent = Decimal('0.2')
    # 计算不同搭配的肉馅营养值
    nutrition_list_meat = compute_nutrition_list(nutrition_file_data, classifications, kind_num_of_meat, weight_of_meat,
                                                 single_meat_min_percent, output_file_path)

    # 6、计算蔬菜搭配
    # 定义蔬菜包含哪些类别
    classifications = VEGETABLE
    # 定义蔬菜占比
    vegetable_percent = 1 - meat_percent
    # 蔬菜重量
    weight_of_vegetable = meat_and_vegetable_weight * vegetable_percent
    # 蔬菜种类个数
    kind_num_of_vegetable = 1
    # 每种蔬菜最低占比
    single_vegetable_min_percent = Decimal('0.2')
    # 计算不同搭配的蔬菜营养值
    nutrition_list_vegetable = compute_nutrition_list(nutrition_file_data, classifications, kind_num_of_vegetable,
                                                      weight_of_vegetable, single_vegetable_min_percent,
                                                      output_file_path)
    # 7、根据topsis算法，计算总体搭配的最优营养值
    nutrition_list = compute_combine_nutrition_list(nutrition_list_flour, nutrition_list_meat, nutrition_list_vegetable,
                                                    output_file_path)
    # 设置筛选条件，需要满足对应营养值为1
    nutrition_filter = ["能量-千卡", "蛋白质-克", "脂肪-克", "碳水化合物-克"]
    nutrition_best_value_list = compute_nutrition_best_value(["综合"], nutrition_list, RNI_range, output_file_path,
                                                             weight, nutrition_filter, 30, 0.9)
    for i in range(ADJUST_ITER_NUM):
        nutrition_best_value_list = adjust_nutrition_list(nutrition_best_value_list, RNI_range, nutrition_file_data2,
                                                          output_file_path, weight, nutrition_filter, 30, 0.95, i + 1)
    return nutrition_best_value_list
    # 从当前所需剩余营养中减去总体搭配的最优营养值
    # for nutrition in SELECT_NUTRITION:
    #     RNI_range[nutrition] = [item - nutrition_best_value_list[nutrition] for item in RNI_range[nutrition]]
    # print("添加面粉肉馅蔬菜后，剩余所需营养范围：" + str(RNI_range))
    # print('------------------------------------------------------------------------------')
