"""
饺子营养优化的MCP客户端工具

此模块提供了一个基于MCP协议的工具，用于优化饺子的营养配比并生成结果报告。
主要功能：
1. 接收RNI营养需求范围
2. 计算最优饺子配方
3. 生成营养分析报告
"""

import datetime
import warnings
import pandas as pd
from typing import Dict, Union, List
from process.main_process import main_process

# 禁用警告信息
warnings.filterwarnings('ignore')

# 需要研究的营养成分
SELECT_NUTRITION = [
    "能量-千卡", "蛋白质-克", "脂肪-克", "碳水化合物-克", "维生素A-微克", "维生素B1-毫克",
    "维生素B2-毫克", "维生素C-毫克", "维生素E-毫克", "钙-毫克", "磷-毫克", "钾-毫克",
    "钠-毫克", "镁-毫克", "铁-毫克", "锌-毫克", "硒-微克", "铜-毫克", "锰-毫克"
]

def optimize_dumpling_nutrition(RNI_range: Dict[str, Union[str, float, int]]) -> Dict[str, Union[pd.DataFrame, Dict]]:
    """
    基于给定的RNI范围优化饺子配方并生成分析报告

    Args:
        RNI_range (Dict[str, Union[str, float, int]]): 营养素推荐摄入量范围
            格式示例:
            {
                "meal": "午饭",
                "能量-千卡": 1200,
                "蛋白质-克": 43.2,
                ...
            }

    Returns:
        Dict[str, Union[pd.DataFrame, Dict]]: 包含以下键的字典：
            - result_data: 优化后的营养值DataFrame
            - parameters: 使用的参数信息
            - metadata: 计算元数据
    """
    # 获取当前的绝对路径
    import os
    current_dir = 'D:/program/VsCodeProjects/python/FOOD/mcp_tools/select_best_nutrition/'
    
    # 生成输出路径
    output_file_path = os.path.join(current_dir, f'output_file/{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}/')
    
    # 生成输入文件路径
    input_file_path = os.path.join(current_dir, f'input_file/')

    # 计算参数
    num_of_dumpling = int(RNI_range["能量-千卡"] / 60)  # 根据能量需求计算饺子数量
    dumpling_skin_percent = 0.5  # 饺子皮占比
    meat_percent = 0.5  # 肉馅占比
    
    # 获取优化结果
    best_nutrition_list = main_process(
        RNI_range=RNI_range,
        num_of_dumpling=num_of_dumpling,
        meat_percent=meat_percent,
        output_file_path=output_file_path,
        input_file_path=input_file_path,
        dumpling_skin_percent=dumpling_skin_percent,
        select_nutrition=SELECT_NUTRITION
    )
    
    # 转换为DataFrame
    final_result = pd.DataFrame(columns=SELECT_NUTRITION)
    final_result = pd.concat([final_result, best_nutrition_list])
    
    # 保存结果
    result_file_path = f'{output_file_path}final_result.csv'
    final_result.to_csv(result_file_path)
    
    # 构造返回结果
    return {
        "status": "success",
        "result_data": final_result,
        "parameters": {
            "num_of_dumpling": num_of_dumpling,
            "dumpling_skin_percent": dumpling_skin_percent,
            "meat_percent": meat_percent
        },
        "metadata": {
            "calculation_time": datetime.datetime.now().isoformat(),
            "result_file_path": result_file_path,
            "selected_nutrition": SELECT_NUTRITION
        }
    }

if __name__ == "__main__":
    # 示例用法
    example_RNI_range = {
    "meal": "晚饭",
    "能量-千卡": 1000,
    "蛋白质-克": 36,
    "脂肪-克": "22.33-27.67",
    "碳水化合物-克": "158.33-163.0",
    "钙-毫克": 266.67,
    "磷-毫克": 233.33,
    "钾-毫克": 666.67,
    "钠-毫克": 733.33,
    "镁-毫克": 116.67,
    "铁-毫克": 5,
    "锌-毫克": 5.17,
    "硒-微克": 16.67,
    "碘-微克": 50,
    "铜-毫克": 0.67,
    "氟-毫克": 0.5,
    "铬-微克": 16.67,
    "锰-毫克": 1.17,
    "钼-微克": 20,
    "维生素A-微克": 266.67,
    "维生素C-毫克": 50,
    "维生素D-微克": 1.67,
    "维生素E-毫克": 4.67,
    "维生素K-微克": 40,
    "维生素B1-毫克": 0.47,
    "维生素B2-毫克": 0.47,
    "维生素B6-毫克": 0.4,
    "维生素B12-微克": 0.8,
    "泛酸-毫克": 1.67,
    "叶酸-微克": 133.33,
    "烟酸-毫克": 4.67,
    "生物素-微克": 10
    }
    result = optimize_dumpling_nutrition(example_RNI_range)
    print(f"优化完成，结果保存在: {result['metadata']['result_file_path']}")

