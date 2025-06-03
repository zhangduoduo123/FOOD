from typing import Dict, Optional, List
from neo4j import GraphDatabase
from langchain_community.chat_models import ChatOllama
import traceback
import io
import logging
from mcp.server.fastmcp import FastMCP

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建 FastMCP 实例
mcp = FastMCP("Neo4jLLM")

# Neo4j配置
NEO4J_CONFIG = {
    'uri': 'bolt://localhost:7687',
    'user': 'neo4j',
    'password': 'root'
}

@mcp.tool()
def get_neo4j_connection():
    """创建并返回Neo4j连接"""
    logger.info("Creating Neo4j connection")
    return GraphDatabase.driver(
        NEO4J_CONFIG['uri'],
        auth=(NEO4J_CONFIG['user'], NEO4J_CONFIG['password'])
    )

@mcp.tool()
def get_graph_schema() -> Dict:
    """获取图数据库结构信息"""
    logger.info("Getting graph schema")
    try:
        driver = get_neo4j_connection()
        with driver.session() as session:
            # 获取所有节点标签
            labels = session.run("CALL db.labels()").data()
            
            # 获取所有关系类型
            relationships = session.run("CALL db.relationshipTypes()").data()
            
            # 获取节点属性
            properties = {}
            for label in labels:
                label_name = label['label']
                props = session.run(
                    f"MATCH (n:{label_name}) RETURN keys(n) LIMIT 1"
                ).data()
                if props:
                    properties[label_name] = props[0]['keys(n)']
            
            schema = {
                'labels': [label['label'] for label in labels],
                'relationships': [rel['relationshipType'] for rel in relationships],
                'properties': properties
            }
            
            return schema
    except Exception as e:
        logger.error(f"Error getting graph schema: {e}")
        return None
    finally:
        driver.close()

def map_relationship_type(question: str, available_relationships: List[str]) -> Dict[str, str]:
    """根据问题语义映射到最合适的关系类型"""
    # 定义关系类型的语义映射
    relationship_mappings = {
        'recommend_eat': ['推荐吃', '可以吃', '适合吃', '建议吃', '能吃'],
        'not_recommend_eat': ['不推荐吃', '不可以吃', '不适合吃', '禁止吃', '不能吃'],
        'prevent': ['预防', '防止', '避免'],
        'cause': ['导致', '引起', '造成'],
        'contain': ['含有', '包含', '富含'],
        'typical_symptom': ['症状', '表现', '特征'],
        'treat': ['治疗', '缓解', '改善']
    }
    
    # 根据问题内容选择最合适的关系类型
    matched_relationships = {}
    
    # 首先检查实际存在的关系类型
    for rel_type in available_relationships:
        if rel_type in relationship_mappings:
            keywords = relationship_mappings[rel_type]
            for keyword in keywords:
                if keyword in question:
                    # 验证这个关系类型是否实际存在于数据库中
                    if rel_type in available_relationships:
                        matched_relationships[keyword] = rel_type
                        logging.info(f"Found matching relationship: {rel_type} for keyword: {keyword}")
    
    if not matched_relationships:
        logging.warning(f"No matching relationships found in available relationships: {available_relationships}")
    
    return matched_relationships

def validate_relationship_connection(driver, query: str) -> bool:
    """验证查询中的关系连接是否实际存在"""
    try:
        # 提取查询中的关系类型和节点标签
        import re
        pattern = r'\(([^)]+)\)-\[r:(\w+)\]->\(([^)]+)\)'
        match = re.search(pattern, query)
        if not match:
            return False
            
        start_node = match.group(1)  # 例如: "f:Food"
        rel_type = match.group(2)    # 例如: "SUITABLE_FOR"
        end_node = match.group(3)    # 例如: "d:Disease"
        
        # 提取节点标签
        start_label = start_node.split(':')[1] if ':' in start_node else start_node
        end_label = end_node.split(':')[1] if ':' in end_node else end_node
        
        # 验证关系是否存在
        verify_query = f"""
        MATCH (n:{start_label})-[r:{rel_type}]->(m:{end_label})
        RETURN count(*) as count
        LIMIT 1
        """
        
        with driver.session() as session:
            result = session.run(verify_query).single()
            return result and result['count'] > 0
            
    except Exception as e:
        logging.error(f"Error validating relationship connection: {e}")
        return False

def validate_query(query: str, schema: Dict) -> Optional[str]:
    """验证Cypher查询"""
    try:
        # 验证查询格式
        if not query.lower().startswith(('match', 'create', 'merge', 'call')):
            return None
            
        if 'where' not in query.lower():
            return None
            
        if 'return' not in query.lower():
            return None
            
        # 验证关系类型
        available_relationships = set(schema['relationships'])
        # 使用正则表达式提取查询中的关系类型
        import re
        rel_pattern = r'\[r:(\w+)\]'
        used_relationships = set(re.findall(rel_pattern, query))
        
        invalid_relationships = used_relationships - available_relationships
        if invalid_relationships:
            logging.warning(f"Invalid relationships found: {invalid_relationships}")
            return None
            
        # 验证节点标签
        available_labels = set(schema['labels'])
        label_pattern = r'(?<!\[r):(\w+)'  # 使用否定向后查找，确保冒号前面不是[r
        used_labels = set(re.findall(label_pattern, query))
        
        invalid_labels = used_labels - available_labels
        if invalid_labels:
            logging.warning(f"Invalid labels found: {invalid_labels}")
            return None
            
        # 验证关系连接是否实际存在
        driver = get_neo4j_connection()
        try:
            if not validate_relationship_connection(driver, query):
                logging.warning("Query contains non-existent relationship connections")
                return None
        finally:
            driver.close()
            
        # 确保以分号结尾
        query = query.strip()
        if not query.endswith(';'):
            query += ';'
            
        return query
        
    except Exception as e:
        logging.error(f"Error validating query: {e}")
        return None

def get_actual_relationships(driver) -> Dict[str, List[str]]:
    """获取数据库中实际存在的关系类型和节点标签"""
    try:
        with driver.session() as session:
            # 获取所有节点标签
            labels = session.run("CALL db.labels()").data()
            
            # 获取所有关系类型
            relationships = session.run("CALL db.relationshipTypes()").data()
            
            # 获取每个关系类型对应的起始和终止节点标签
            relationship_info = {}
            for rel in relationships:
                rel_type = rel['relationshipType']
                # 查询该关系类型连接的节点标签对
                query = f"""
                MATCH (n)-[r:{rel_type}]->(m)
                RETURN DISTINCT labels(n) as start_labels, labels(m) as end_labels
                LIMIT 10
                """
                result = session.run(query).data()
                if result:
                    relationship_info[rel_type] = {
                        'start_labels': list(set([label for r in result for label in r['start_labels']])),
                        'end_labels': list(set([label for r in result for label in r['end_labels']]))
                    }
            
            return {
                'labels': [label['label'] for label in labels],
                'relationships': [rel['relationshipType'] for rel in relationships],
                'relationship_info': relationship_info
            }
    except Exception as e:
        logging.error(f"Error getting actual relationships: {e}")
        return None

def generate_cypher_query(question: str, schema: Dict) -> str:
    """使用LLM根据自然语言问题生成Cypher查询，只使用实际存在的关系"""
    try:
        # 获取数据库连接
        driver = get_neo4j_connection()
        actual_relationships = get_actual_relationships(driver)
        driver.close()
        
        if not actual_relationships:
            logging.error("无法获取实际关系信息")
            return None
            
        print(f"可用的关系类型: {actual_relationships['relationships']}")
        
        # 使用 map_relationship_type 获取正确的关系类型映射
        matched_relationships = map_relationship_type(question, actual_relationships['relationships'])
        if not matched_relationships:
            logging.warning(f"未找到匹配的关系类型。问题: {question}")
            return None
            
        print(f"匹配到的关系: {matched_relationships}")
        
        # 获取第一个匹配的关系类型
        rel_type = list(matched_relationships.values())[0]
        print(f"选择使用的关系类型: {rel_type}")
        
        # 获取该关系类型的实际连接信息
        rel_info = actual_relationships['relationship_info'].get(rel_type)
        if not rel_info:
            logging.warning(f"未找到关系 {rel_type} 的连接信息")
            return None
            
        print(f"关系 {rel_type} 的连接信息: {rel_info}")
        
        # 构建查询模板
        query_template = f"""
        MATCH (n:{rel_info['start_labels'][0]})-[r:{rel_type}]->(m:{rel_info['end_labels'][0]})
        WHERE n.name = $disease_name
        RETURN m.name as name, r.reason as reason
        """
        
        print("\n=== LLM生成的Cypher查询 ===")
        print(query_template)
        print("===========================\n")
        
        # 根据问题提取疾病名称
        disease_name = None
        if "糖尿病" in question:
            disease_name = "糖尿病"
        elif "高血压" in question:
            disease_name = "高血压"
        # 可以添加更多疾病名称的匹配
        
        if not disease_name:
            logging.warning("未能在问题中找到疾病名称")
            return None
            
        # 替换查询中的疾病名称
        query = query_template.replace("$disease_name", f"'{disease_name}'")
        print(f"生成的查询: {query}")
        
        # 验证查询
        validated_query = validate_query(query, schema)
        if not validated_query:
            logging.warning("查询验证失败")
            return None
            
        print(f"验证后的查询: {validated_query}")
        return validated_query
        
    except Exception as e:
        logging.error(f"生成Cypher查询时出错: {e}")
        import traceback
        logging.error(f"错误堆栈: {traceback.format_exc()}")
        return None

@mcp.tool()
def process_question(question: str) -> Dict:
    """处理用户问题并返回结果"""
    logger.info(f"Processing question: {question}")
    try:
        # 获取图数据库结构
        schema = get_graph_schema()
        if not schema:
            return {"error": "无法获取图数据库结构"}
            
        # 生成Cypher查询
        query = generate_cypher_query(question, schema)
        if not query:
            return {"error": "无法生成有效的查询"}
            
        # 执行查询
        driver = get_neo4j_connection()
        try:
            with driver.session() as session:
                results = session.run(query).data()
                return {"results": results}
        finally:
            driver.close()
            
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    logger.info("Starting Neo4j LLM server through MCP")
    mcp.run(transport="stdio") 