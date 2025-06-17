from mcp.server.fastmcp import FastMCP
import logging
from typing import Dict, Any
from .get_user_info import get_user_info
from .adjust_RNI import adjust_RNI
from pyprojroot import here
import pandas as pd
from .select_best_nutrition.client import optimize_dumpling_nutrition
import os
import sys
# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from utils.mysql_util import get_mysql_connection
 
# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为 INFO
    format="%(asctime)s - %(levelname)s - %(message)s"  # 日志格式
)
logger = logging.getLogger(__name__)
 
# 创建 FastMCP 实例
mcp = FastMCP("save_meal_recommend")
    
 
@mcp.tool()
def save_meal_recommend(username: str, adjustments: Dict[str, Any] = None) -> dict:
    """
    根据用户名和调整参数保存餐食推荐
    
    参数:
        username: 用户名
        adjustments: 营养调整参数
        
    返回:
        是否保存成功
    """
    user_info = get_user_info(username)
    adjust_info = str(adjustments) if adjustments is not None else None
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

    current_dir = str(here()).replace('\\', '/')+'/mcp_tools/select_best_nutrition/'
    EXCLUDED_FOODS = []
    # 根据用户信息设置排除的食物
    if user_info.get('Ethnicity') == '回族':
        EXCLUDED_FOODS.append('猪肉')
    if user_info.get('Vegetarian') == '是':
        EXCLUDED_FOODS.extend(['猪肉', '鸡肉', '牛肉', '羊肉'])
    uid = user_info.get('uid')
    # 需要插入的字段
    nutrition_fields = [
        '能量-千卡', '蛋白质-克', '脂肪-克', '碳水化合物-克', '钙-毫克', '磷-毫克', '钾-毫克', '钠-毫克', '镁-毫克',
        '铁-毫克', '锌-毫克', '硒-微克', '碘-微克', '铜-毫克', '氟-毫克', '铬-微克', '锰-毫克', '钼-微克',
        '维生素A-微克', '维生素C-毫克', '维生素D-微克', '维生素E-毫克', '维生素K-微克', '维生素B1-毫克',
        '维生素B2-毫克', '维生素B6-毫克', '维生素B12-微克', '泛酸-毫克', '叶酸-微克', '烟酸-毫克', '生物素-微克'
    ]

    for meal_rni in RNI:
        meal = meal_rni["meal"]
        result = optimize_dumpling_nutrition(
            meal_rni, current_dir=current_dir, EXCLUDED_FOODS=EXCLUDED_FOODS, ADJUST_ITER_NUM=2)
        # 遍历DataFrame的每一行，插入到meal_recommend表
        # 调整：每插入一行后立即提交，并在每次插入时捕获并打印异常，确保数据能被保存且异常能被发现
        try:
            conn = get_mysql_connection()
            conn.autocommit(True)  # 强制开启自动提交
            with conn.cursor() as cursor:
                for food_name, row in result['final_result'].iterrows():
                    columns = ['uid', 'meal', 'adjust_info', 'food_recommend'] + nutrition_fields + ['last_use_timestamp']
                    columns_sql = ','.join([f'`{col}`' for col in columns])  # 用反引号包裹
                    values = [
                        uid,
                        meal,
                        adjust_info,
                        food_name
                    ]
                    for field in nutrition_fields:
                        values.append(row[field] if field in row else None)
                    values.append(None)
                    placeholders = ','.join(['%s'] * len(columns))
                    sql = f"INSERT INTO meal_recommend ({columns_sql}) VALUES ({placeholders})"
                    print(f"即将执行SQL: {sql}")
                    print(f"参数: {values}")
                    cursor.execute(sql, values)
            conn.commit()
        except Exception as e:
            print(f"数据库操作异常: {e}")
        finally:
            try:
                conn.close()
            except Exception as close_e:
                print(f"关闭数据库连接时出错: {close_e}")
    return {"status": "success"}
    
 
 
if __name__ == "__main__":
    # logger.info("Start save_meal_recommend server through MCP")  # 记录服务启动日志
    # mcp.run(transport="stdio")  # 启动服务并使用标准输入输出通信
    print(save_meal_recommend("zhangyulong"))