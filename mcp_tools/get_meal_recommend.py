from mcp.server.fastmcp import FastMCP
import logging
from typing import Dict, Any
from get_user_info import get_user_info
from adjust_RNI import adjust_RNI
from pyprojroot import here
import pandas as pd
import pymysql
from select_best_nutrition.client import optimize_dumpling_nutrition
import os
import sys
from datetime import datetime
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
mcp = FastMCP("get_meal_recommend")
    
 
@mcp.tool()
def get_meal_recommend(username: str, adjustments: Dict[str, Any] = None) -> dict:
    """
    根据用户名和调整参数获取餐食推荐
    
    参数:
        username: 用户名
        adjustments: 营养调整参数
        
    返回:
        # 返回信息说明:
        # - food_recommend: 推荐的食材及其具体重量，格式为字典，例如 {"猪肉": 50, "白菜": 100}，表示猪肉50克、白菜100克
        # - nutrition_value: 推荐食材组合所包含的各项营养元素值，格式为字典，如 {"能量-千卡": xxx, "蛋白质-克": xxx, ...}
        # - adjustments: 营养元素的调整信息，若无调整则为 None 或空
        # 例如:
        # {
        #   "food_recommend": {
        #       "猪肉": 50,
        #       "白菜": 100
        #   },
        #   "nutrition_value": {
        #       "能量-千卡": 500,
        #       "蛋白质-克": 20,
        #       ...
        #   },
        #   "adjustments": {
        #       "能量": 1.2,
        #       "维生素C": 1.5
        #   }
        # }
    """
    user_info = get_user_info(username)
    uid = user_info.get('uid')

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
    # INSERT_YOUR_CODE
    if adjustments is None:
        conn = get_mysql_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # 先查找last_use_timestamp为null的记录
                sql_null = """
                    SELECT * FROM meal_recommend
                    WHERE uid = %s AND meal = %s AND last_use_timestamp IS NULL
                    ORDER BY id ASC
                    LIMIT 1
                """
                cursor.execute(sql_null, (uid, current_meal))
                record = cursor.fetchone()
                if not record:
                    # 如果没有last_use_timestamp为null的，查找last_use_timestamp最早的
                    sql_earliest = """
                        SELECT * FROM meal_recommend
                        WHERE uid = %s AND meal = %s
                        ORDER BY last_use_timestamp ASC
                        LIMIT 1
                    """
                    cursor.execute(sql_earliest, (uid, current_meal))
                    record = cursor.fetchone()
                if record:
                    # 更新last_use_timestamp为当前时间
                    update_sql = """
                        UPDATE meal_recommend
                        SET last_use_timestamp = %s
                        WHERE id = %s
                    """
                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute(update_sql, (now_str, record['id']))
                    conn.commit()
                    food_recommend = record['food_recommend']
                    # INSERT_YOUR_CODE
                    # 重新解析food_recommend字符串，支持多组用分号分隔，每组用下划线分隔食材和重量（假设不会出现同名食材）
                    food_recommend_dict = {}
                    if isinstance(food_recommend, str):
                        groups = food_recommend.split(';')
                        for group in groups:
                            if not group.strip():
                                continue
                            items = group.split('_')
                            # items应为: 名称1, 重量1, 名称2, 重量2, ...
                            i = 0
                            while i < len(items) - 1:
                                name = items[i].strip()
                                weight_str = items[i+1].strip()
                                try:
                                    weight = float(weight_str)
                                except ValueError:
                                    weight = weight_str  # fallback: keep as string if not float
                                food_recommend_dict[name] = weight
                                i += 2
                        items = food_recommend.split(';')
                    else:
                        food_recommend_dict = food_recommend  # fallback: already dict or other type
                    # INSERT_YOUR_CODE
                    # 设置nutrition_value为仅包含record中有值的营养元素字段的字典
                    nutrition_fields = [
                        '能量-千卡', '蛋白质-克', '脂肪-克', '碳水化合物-克', '钙-毫克', '磷-毫克', '钾-毫克', '钠-毫克', '镁-毫克',
                        '铁-毫克', '锌-毫克', '硒-微克', '碘-微克', '铜-毫克', '氟-毫克', '铬-微克', '锰-毫克', '钼-微克',
                        '维生素A-微克', '维生素C-毫克', '维生素D-微克', '维生素E-毫克', '维生素K-微克', '维生素B1-毫克',
                        '维生素B2-毫克', '维生素B6-毫克', '维生素B12-微克', '泛酸-毫克', '叶酸-微克', '烟酸-毫克', '生物素-微克'
                    ]
                    nutrition_value = {}
                    for field in nutrition_fields:
                        value = record.get(field)
                        if value is not None and value != '':
                            # INSERT_YOUR_CODE
                            try:
                                value = float(value)
                                value = round(value, 2)
                            except Exception:
                                pass
                            nutrition_value[field] = value
                    return {"status": "success", "food_recommend": food_recommend_dict, "nutrition_value": nutrition_value}
        except Exception as e:
            return {"status": "fail", "msg": f"数据库操作异常: {e}"}
        finally:
            try:
                conn.close()
            except Exception as close_e:
                pass
    adjust_info = str(adjustments) if adjustments is not None else None
    adjustments_original = adjustments.copy()
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

    # # 需要插入的字段
    # nutrition_fields = [
    #     '能量-千卡', '蛋白质-克', '脂肪-克', '碳水化合物-克', '钙-毫克', '磷-毫克', '钾-毫克', '钠-毫克', '镁-毫克',
    #     '铁-毫克', '锌-毫克', '硒-微克', '碘-微克', '铜-毫克', '氟-毫克', '铬-微克', '锰-毫克', '钼-微克',
    #     '维生素A-微克', '维生素C-毫克', '维生素D-微克', '维生素E-毫克', '维生素K-微克', '维生素B1-毫克',
    #     '维生素B2-毫克', '维生素B6-毫克', '维生素B12-微克', '泛酸-毫克', '叶酸-微克', '烟酸-毫克', '生物素-微克'
    # ]

    # # 遍历DataFrame的每一行，插入到meal_recommend表
    # # 调整：每插入一行后立即提交，并在每次插入时捕获并打印异常，确保数据能被保存且异常能被发现
    # try:
    #     conn = get_mysql_connection()
    #     conn.autocommit(True)  # 强制开启自动提交
    #     with conn.cursor() as cursor:
    #         for food_name, row in result['final_result'].iterrows():
    #             columns = ['uid', 'meal', 'adjust_info', 'food_recommend'] + nutrition_fields + ['last_use_timestamp']
    #             columns_sql = ','.join([f'`{col}`' for col in columns])  # 用反引号包裹
    #             values = [
    #                 uid,
    #                 current_meal,
    #                 adjust_info,
    #                 food_name
    #             ]
    #             for field in nutrition_fields:
    #                 values.append(row[field] if field in row else None)
    #             values.append(None)
    #             placeholders = ','.join(['%s'] * len(columns))
    #             sql = f"INSERT INTO meal_recommend ({columns_sql}) VALUES ({placeholders})"
    #             print(f"即将执行SQL: {sql}")
    #             print(f"参数: {values}")
    #             cursor.execute(sql, values)
    #     conn.commit()
    # except Exception as e:
    #     print(f"数据库操作异常: {e}")
    # finally:
    #     try:
    #         conn.close()
    #     except Exception as close_e:
    #         print(f"关闭数据库连接时出错: {close_e}")
    food_recommend = result['final_result'].index[0]
    nutrition_value = result['final_result'].iloc[0].to_dict()
    # INSERT_YOUR_CODE
    # 将food_recommend字符串转换为字典格式
    food_recommend_dict = {}
    if isinstance(food_recommend, str):
        groups = food_recommend.split(';')
        for group in groups:
            if not group.strip():
                continue
            items = group.split('_')
            # items应为: 名称1, 重量1, 名称2, 重量2, ...
            i = 0
            while i < len(items) - 1:
                name = items[i].strip()
                weight_str = items[i+1].strip()
                try:
                    weight = float(weight_str)
                except ValueError:
                    weight = weight_str  # fallback: keep as string if not float
                food_recommend_dict[name] = weight
                i += 2
        items = food_recommend.split(';')
    else:
        food_recommend_dict = food_recommend  # fallback: already dict or other type
    result['food_recommend'] = food_recommend_dict
    # nutrition_value中的值，最多保留两位小数
    for k, v in nutrition_value.items():
        if isinstance(v, float):
            nutrition_value[k] = round(v, 2)
    result['nutrition_value'] = nutrition_value
    if adjustments is not None:
        result['adjustments'] = adjustments_original
    
    return result
    
 
 
if __name__ == "__main__":
    logger.info("Start get_meal_recommend server through MCP")  # 记录服务启动日志
    mcp.run(transport="stdio")  # 启动服务并使用标准输入输出通信
    # print(get_meal_recommend("zhangyulong", {"能量": 1.2, "维生素C": 1.5}))
    # print(get_meal_recommend("zhangyulong"))