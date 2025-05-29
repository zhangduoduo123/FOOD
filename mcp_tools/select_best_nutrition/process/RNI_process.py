import pandas as pd

SPECIAL_CONDITIONS = ["孕早期", "孕中期", "孕晚期", "哺乳期"]
RNI_MIN = 1
RNI_MAX = 1.05
PERCENTAGE_OF_EACH_MEAL = {"早饭": 0.3, "午饭": 0.4, "晚饭": 0.3}


# 获取符合条件的RNI数据
def get_RNI_data(RNI_file_data, age, sex, activity, special_condition):
    if special_condition in SPECIAL_CONDITIONS:
        return RNI_file_data.loc[RNI_file_data['人群'] == special_condition]
    else:
        return RNI_file_data.loc[(~RNI_file_data['人群'].isin(SPECIAL_CONDITIONS))
                                 & (RNI_file_data['年龄小值'] <= age)
                                 & (age < RNI_file_data['年龄大值'])
                                 & (RNI_file_data['性别'] == sex)
                                 & (RNI_file_data['活动水平'] == activity)]


# 获取RNI的范围
def get_RNI_range(RNI_file_name, age, sex, activity, special_condition, weight, meal, select_nutrition):
    RNI_file_data = pd.read_csv(RNI_file_name, encoding="gbk")
    RNI_data = get_RNI_data(RNI_file_data, age, sex, activity, special_condition)
    RNI_range = {}
    for nutrition in select_nutrition:
        nutrition_value = RNI_data[nutrition].values[0]
        weight_reference = RNI_data['体重/kg'].values[0]
        nutrition_value_adjust = weight / weight_reference * PERCENTAGE_OF_EACH_MEAL[meal]
        nutrition_range = []
        if "-" in str(nutrition_value):
            nutrition_range.append(int(nutrition_value.split('-')[0]) * nutrition_value_adjust)
            nutrition_range.append(int(nutrition_value.split('-')[1]) * nutrition_value_adjust)
        else:
            nutrition_range.append(nutrition_value * RNI_MIN * nutrition_value_adjust)
            nutrition_range.append(nutrition_value * RNI_MAX * nutrition_value_adjust)
        RNI_range[nutrition] = nutrition_range
    print("所需营养范围：" + str(RNI_range))
    return RNI_range

# 获取RNI的范围
def get_RNI_range(RNI_range_in, select_nutrition):
    RNI_range_out = {}
    for nutrition in select_nutrition:
        nutrition_value = RNI_range_in[nutrition]
        nutrition_range = []
        if "-" in str(nutrition_value):
            nutrition_range.append(float(nutrition_value.split('-')[0]))
            nutrition_range.append(float(nutrition_value.split('-')[1]))
        else:
            nutrition_range.append(float(nutrition_value) * RNI_MIN)
            nutrition_range.append(float(nutrition_value) * RNI_MAX)
        RNI_range_out[nutrition] = nutrition_range
    print("所需营养范围：" + str(RNI_range_out))
    return RNI_range_out