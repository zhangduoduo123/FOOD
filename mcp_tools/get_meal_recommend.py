from mcp.server.fastmcp import FastMCP
import logging
from typing import Dict, Any
from get_user_info import get_user_info
from adjust_RNI import adjust_RNI
from pyprojroot import here
import pandas as pd
from select_best_nutrition.client import optimize_dumpling_nutrition
 
# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为 INFO
    format="%(asctime)s - %(levelname)s - %(message)s"  # 日志格式
)
logger = logging.getLogger(__name__)
 
# 创建 FastMCP 实例
mcp = FastMCP("get_meal_recommend")
    
 
@mcp.tool()
def get_meal_recommend(username: str, adjustments: Dict[str, Any] = None) -> dict:
    """
    根据用户名和调整参数获取餐食推荐
    
    参数:
        username: 用户名
        adjustments: 营养调整参数
        
    返回:
        包含推荐餐食信息的字典，包括营养优化结果
    """
    user_info = get_user_info(username)
    # 计算BMI值
    weight = float(user_info.get('weight', 0))
    print(weight)
    height = float(user_info.get('height', 0))
    print(height)
    
    if weight > 0 and height > 0:
        # 将身高从厘米转换为米
        height_m = height / 100
        bmi = weight / (height_m * height_m)
        
        # 如果BMI超过24，调整能量、脂肪和碳水化合物的摄入
        if bmi > 24:
            if adjustments is None:
                adjustments = {}
            adjust_value = 0.95
            # 对能量、脂肪、碳水化合物进行调整
            for nutrient in ['能量', '脂肪', '碳水化合物']:
                if nutrient in adjustments:
                    adjustments[nutrient] = round(adjustments[nutrient] * adjust_value, 2)
                else:
                    adjustments[nutrient] = adjust_value
    RNI = adjust_RNI(user_info, adjustments)
    from datetime import datetime
    
    # 获取当前时间
    current_time = datetime.now().time()
    
    # 定义用餐时间范围
    breakfast_start = datetime.strptime("00:00", "%H:%M").time()
    breakfast_end = datetime.strptime("09:59", "%H:%M").time()
    lunch_start = datetime.strptime("10:00", "%H:%M").time()
    lunch_end = datetime.strptime("13:59", "%H:%M").time()
    dinner_start = datetime.strptime("14:00", "%H:%M").time()
    dinner_end = datetime.strptime("23:59", "%H:%M").time()
    
    # 根据当前时间判断用餐类型
    current_meal = None
    if breakfast_start <= current_time <= breakfast_end:
        current_meal = "早饭"
    elif lunch_start <= current_time <= lunch_end:
        current_meal = "午饭"
    elif dinner_start <= current_time <= dinner_end:
        current_meal = "晚饭"
    # 从RNI列表中筛选出当前餐次的推荐
    current_meal_recommend = next((meal for meal in RNI if meal["meal"] == current_meal), None)
    # return current_meal_recommend
    
    current_dir = str(here()).replace('\\', '/')+'/mcp_tools/select_best_nutrition/'
    EXCLUDED_FOODS = []
    
    # 根据用户信息设置排除的食物
    if user_info.get('Ethnicity') == '回族':
        EXCLUDED_FOODS.append('猪肉')
    if user_info.get('Vegetarian') == '是':
        EXCLUDED_FOODS.extend(['猪肉', '鸡肉', '牛肉', '羊肉'])
    
    result = optimize_dumpling_nutrition(current_meal_recommend, current_dir=current_dir, EXCLUDED_FOODS=EXCLUDED_FOODS)
    if adjustments is not None:
        result['adjustments'] = adjustments
    
    # 转换DataFrame为字典
    # if isinstance(result["result_data"], pd.DataFrame):
    #     result["result_data"] = result["result_data"].to_dict(orient="list")
    
    return result
    
 
 
if __name__ == "__main__":
    logger.info("Start get_meal_recommend server through MCP")  # 记录服务启动日志
    mcp.run(transport="stdio")  # 启动服务并使用标准输入输出通信
    # print(get_meal_recommend("zhangyulong", {"能量": 1.2, "维生素C": 1.5}))