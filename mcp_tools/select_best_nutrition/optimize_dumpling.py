"""
FastMCP implementation for dumpling nutrition optimization
"""
from mcp.server.fastmcp import FastMCP
from typing import Dict, Union, List
import pandas as pd
from client import optimize_dumpling_nutrition
import logging
# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为 INFO
    format="%(asctime)s - %(levelname)s - %(message)s"  # 日志格式
)
logger = logging.getLogger(__name__)

mcp = FastMCP("optimize_dumpling")

@mcp.tool()
def optimize_dumpling(params: Dict[str, Union[str, float]]) -> Dict[str, Union[str, List[float], Dict]]:
    """
    优化饺子营养配比的FastMCP端点
    
    Args:
        params: 营养素推荐摄入量范围字典
        
    Returns:
        优化结果，包含营养值、参数信息和元数据
    """
    # 调用优化函数
    result = optimize_dumpling_nutrition(params)
    
    # 转换DataFrame为字典
    if isinstance(result["result_data"], pd.DataFrame):
        result["result_data"] = result["result_data"].to_dict(orient="list")
    
    return result

if __name__ == "__main__":
    logger.info("Start optimize_dumpling server through MCP")  # 记录服务启动日志
    mcp.run(transport="stdio")  