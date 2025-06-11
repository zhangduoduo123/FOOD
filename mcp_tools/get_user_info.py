from mcp.server.fastmcp import FastMCP
import logging
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
mcp = FastMCP("get_user_info")
 
@mcp.tool()
def get_user_info(username: str) -> dict:
    """
    根据用户名获取用户信息
    
    参数:
        username: 用户名
        
    返回:
        包含用户信息的字典，如果发生错误则返回错误信息
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        # 首先根据用户名查找uid
        cursor.execute("SELECT uid FROM user_info WHERE username = %s", (username,))
        result = cursor.fetchone()
        
        if not result:
            return {"error": f"未找到用户: {username}"}
            
        uid = result[0]
        
        # 根据uid获取用户基本信息
        cursor.execute("SELECT * FROM user_basic_info WHERE uid = %s", (uid,))
        user_info = cursor.fetchone()
        
        if not user_info:
            return {"error": f"未找到用户ID {uid} 的基本信息"}
            
        # 获取列名
        columns = [desc[0] for desc in cursor.description]
       
        # 将结果转换为字典
        user_data = dict(zip(columns, user_info))
         # 转换性别和活动水平
        if 'gender' in user_data:
            user_data['gender'] = '男' if user_data['gender'] == 'M' else '女'
        if 'physical_activity' in user_data:
            activity_map = {
                0: '-',
                1: '极轻',
                2: '轻',
                3: '中',
                4: '重',
                5: '极重'
            }
            user_data['physical_activity'] = activity_map.get(user_data['physical_activity'], user_data['physical_activity'])
        
        return user_data
        
    except Exception as e:
        logger.error(f"获取用户信息时发生错误: {str(e)}")
        return {"error": f"数据库错误: {str(e)}"}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    
 
 
if __name__ == "__main__":
    logger.info("Start get_user_info server through MCP")  # 记录服务启动日志
    mcp.run(transport="stdio")  # 启动服务并使用标准输入输出通信