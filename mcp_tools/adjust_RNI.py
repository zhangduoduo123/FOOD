from mcp.server.fastmcp import FastMCP
import pymysql
from typing import Dict, Any, Optional, List, Tuple
import logging
# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为 INFO
    format="%(asctime)s - %(levelname)s - %(message)s"  # 日志格式
)
logger = logging.getLogger(__name__)

mcp = FastMCP("adjust_RNI")

SPECIAL_CONDITIONS = ["孕早期", "孕中期", "哺乳期"]

# 不需要按体重调整的列
EXCLUDE_COLUMNS = ['人群', '年龄小值', '年龄大值', '性别', '体重-kg', '活动水平']

PERCENTAGE_OF_EACH_MEAL = {"早饭": 0.3, "午饭": 0.4, "晚饭": 0.3}

def get_nutrient_columns(cursor) -> List[str]:
    """获取数据库中的营养素列名"""
    cursor.execute("SHOW COLUMNS FROM rni_chinese")
    return [column[0] for column in cursor.fetchall()]

def match_nutrient_name(nutrient: str, columns: List[str]) -> Optional[str]:
    """
    匹配营养素名称与数据库列名
    
    参数:
        nutrient: 调整参数中的营养素名称（如"蛋白质"）
        columns: 数据库表的列名列表（如["蛋白质-克", "能量-千卡"]）
    
    返回:
        匹配的完整列名或None
    """
    # 精确匹配
    exact_match = next((col for col in columns if col.startswith(f"{nutrient}-")), None)
    if exact_match:
        return exact_match
    
    # 模糊匹配（处理可能的变体，如"维生素C"匹配"维生素C-毫克"）
    for col in columns:
        if nutrient.lower() in col.lower().split('-')[0]:
            return col
    
    return None

def validate_params(params: Dict[str, Any], param_type: str = "rni", columns: List[str] = None) -> Optional[str]:
    """
    统一的参数验证函数
    
    参数:
        params: 要验证的参数字典
        param_type: 参数类型，可选值为 "rni" 或 "adjustment"
        columns: 数据库表的列名列表（用于验证调整参数）
    """
    if not isinstance(params, dict):
        return "参数必须是字典类型"
    
    if param_type == "rni":
        required_fields = {
            'sex': '性别',
            'age': '年龄',
            'physical_activity': '活动水平',
            'weight': '体重'
        }
        
        # 检查必填字段
        for field, name in required_fields.items():
            if field not in params:
                return f"缺少必填参数: {name}"
        
        # 验证参数类型和值
        if not isinstance(params['age'], (int, float)):
            return "年龄必须是数字"
        if params['age'] < 0:
            return "年龄不能为负数"
        
        # 验证体重
        if not isinstance(params['weight'], (int, float)):
            return "体重必须是数字"
        if params['weight'] <= 0:
            return "体重必须大于0"
        
        # 验证性别
        if params['sex'] not in ['男', '女']:
            return "性别必须是'男'或'女'"
        
        # 验证活动水平
        valid_activities = ['-', '极轻', '轻', '中', '重', '极重']
        if params['physical_activity'] not in valid_activities:
            return f"活动水平必须是以下之一: {', '.join(valid_activities)}"
    
    elif param_type == "adjustment":
        if not columns:
            return "无法验证调整参数：缺少数据库列信息"
            
        invalid_nutrients = []
        for nutrient, value in params.items():
            if not isinstance(value, (int, float)):
                return f"调整值 {nutrient} 必须是数字类型"
            if value <= 0:
                return f"调整值 {nutrient} 必须大于0"
            
            # 验证营养素是否能与数据库列匹配
            if not match_nutrient_name(nutrient, columns):
                invalid_nutrients.append(nutrient)
        
        if invalid_nutrients:
            available_nutrients = [col.split('-')[0] for col in columns if '-' in col and col not in EXCLUDE_COLUMNS]
            return f"找不到以下营养素的匹配项: {', '.join(invalid_nutrients)}\n可用的营养素: {', '.join(available_nutrients)}"
    
    return None

def adjust_value_by_weight(value: Any, weight_ratio: float) -> Any:
    """根据体重比例调整值"""
    if isinstance(value, (int, float)):
        return round(float(value) * weight_ratio, 2)
    elif isinstance(value, str):
        # 处理范围值，例如 "30-100"
        if '-' in value:
            try:
                low, high = map(float, value.split('-'))
                return f"{round(low * weight_ratio, 2)}-{round(high * weight_ratio, 2)}"
            except ValueError:
                return value
    return value

def get_base_RNI(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取基础RNI值"""
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="root",
            database="mcp"
        )
        cursor = conn.cursor()
        
        # 获取表的列名
        columns = get_nutrient_columns(cursor)
        
        # 参数验证
        error = validate_params(params, "rni")
        if error:
            return {"error": error}
        
        # 构建查询
        sex = params['sex']
        age = params['age']
        physical_activity = params['physical_activity']
        category = params['category']
        if category in SPECIAL_CONDITIONS:
            cursor.execute(f"SELECT * FROM rni_chinese where 人群 = '{category}'")
        else:
            cursor.execute(f"SELECT * FROM rni_chinese where 性别 = '{sex}' and 年龄小值 <= {age} and 年龄大值 > {age} and 活动水平 = '{physical_activity}'")
        
        result = cursor.fetchone()
        
        if not result:
            return {"error": "未找到匹配的数据"}
        
        # 将结果转换为字典
        base_rni = dict(zip(columns, result))
        
        # 获取数据库中的参考体重和实际体重的比例
        try:
            db_weight = float(base_rni.get('体重-kg', 0))
            if db_weight <= 0:
                return {"error": "数据库中的参考体重无效"}
            
            actual_weight = float(params['weight'])
            weight_ratio = actual_weight / db_weight
            
            # 根据体重比例调整营养素值
            for column, value in base_rni.items():
                if column not in EXCLUDE_COLUMNS and value is not None:
                    base_rni[column] = adjust_value_by_weight(value, weight_ratio)
            
        except (ValueError, TypeError) as e:
            return {"error": f"体重计算错误: {str(e)}"}
        
        return base_rni
        
    except pymysql.Error as e:
        return {"error": f"数据库错误: {str(e)}"}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@mcp.tool()
def adjust_RNI(base_params: Dict[str, Any], adjustments: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    根据调整参数计算调整后的RNI值，并按三餐分配
    
    参数:
        base_params (Dict[str, Any]): 基础RNI查询参数，包含:
            - category (str): 人群类别
            - sex (str): 性别
            - age (int/float): 年龄
            - physical_activity (str): 活动水平
            - weight (float): 体重(kg)
        adjustments (Dict[str, Any]): RNI调整参数，键为营养素名称，值为调整系数
            例如: {"蛋白质": 1.2, "维生素C": 1.5}
    
    返回:
        List[Dict[str, Any]]: 包含三个字典的列表，分别代表早餐、午餐、晚餐的营养需求
    
    示例:
        >>> base_params = {"category": "成人", "sex": "男", "age": 30, "physical_activity": "中", "weight": 70}
        >>> adjustments = {"蛋白质": 1.2, "维生素C": 1.5}
        >>> adjust_RNI(base_params, adjustments)
        [
            {"meal": "早饭", "蛋白质-克": "25.2", "维生素C-毫克": "45-47.25", ...},
            {"meal": "午饭", "蛋白质-克": "33.6", "维生素C-毫克": "60-63", ...},
            {"meal": "晚饭", "蛋白质-克": "25.2", "维生素C-毫克": "45-47.25", ...}
        ]
    """
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="root",
            database="mcp"
        )
        cursor = conn.cursor()
        
        # 获取数据库列名
        columns = get_nutrient_columns(cursor)
        
        # 验证调整参数
        error = validate_params(adjustments, "adjustment", columns)
        if error:
            return {"error": error}
        
        # 获取基础RNI值
        base_rni = get_base_RNI(base_params)
        if "error" in base_rni:
            return [{"error": base_rni["error"]}]
        
        # 创建结果字典，初始值与基础RNI相同
        result = base_rni.copy()
        
        # 应用调整系数
        for nutrient, factor in adjustments.items():
            # 查找匹配的数据库列名
            column_name = match_nutrient_name(nutrient, columns)
            if column_name and column_name in result:
                value = result[column_name]
                if isinstance(value, str) and '-' in value:
                    # 处理范围值
                    try:
                        low, high = map(float, value.split('-'))
                        result[column_name] = f"{round(low * factor, 2)}-{round(high * factor, 2)}"
                    except ValueError:
                        continue
                else:
                    # 处理普通数值
                    try:
                        original_value = float(value)
                        result[column_name] = round(original_value * factor, 2)
                    except (ValueError, TypeError):
                        continue
        
        # 按三餐分配营养素
        meal_results = []
        for meal, percentage in PERCENTAGE_OF_EACH_MEAL.items():
            meal_dict = {"meal": meal}
            for column, value in result.items():
                if column not in EXCLUDE_COLUMNS and value is not None:
                    if isinstance(value, str) and '-' in value:
                        try:
                            low, high = map(float, value.split('-'))
                            meal_dict[column] = f"{round(low * percentage, 2)}-{round(high * percentage, 2)}"
                        except ValueError:
                            meal_dict[column] = value
                    else:
                        try:
                            numeric_value = float(value)
                            meal_dict[column] = round(numeric_value * percentage, 2)
                        except (ValueError, TypeError):
                            meal_dict[column] = value
            meal_results.append(meal_dict)
        
        return meal_results
        
    except pymysql.Error as e:
        return [{"error": f"数据库错误: {str(e)}"}]
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    logger.info("Start adjust_RNI server through MCP")  # 记录服务启动日志
    mcp.run(transport="stdio")  
