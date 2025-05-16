from typing import Union, List, Dict
import mysql.connector
from langchain_community.chat_models import ChatOllama

# MySQL配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'health'
}

def get_mysql_connection():
    """创建并返回MySQL连接"""
    return mysql.connector.connect(**MYSQL_CONFIG)

def get_database_schema() -> Dict:
    """获取数据库结构信息，包括表、列、主键和外键关系"""
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 获取表信息
        cursor.execute("""
            SELECT 
                t.TABLE_NAME,
                c.COLUMN_NAME,
                c.DATA_TYPE,
                c.COLUMN_COMMENT,
                c.IS_NULLABLE,
                c.COLUMN_KEY
            FROM INFORMATION_SCHEMA.TABLES t
            JOIN INFORMATION_SCHEMA.COLUMNS c ON t.TABLE_NAME = c.TABLE_NAME
            WHERE t.TABLE_SCHEMA = %s
            ORDER BY t.TABLE_NAME, c.ORDINAL_POSITION
        """, (MYSQL_CONFIG['database'],))
        table_rows = cursor.fetchall()

        # 获取外键关系
        cursor.execute("""
            SELECT 
                TABLE_NAME,
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = %s
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """, (MYSQL_CONFIG['database'],))
        foreign_keys = cursor.fetchall()
        
        schema = {}
        for row in table_rows:
            table_name = row['TABLE_NAME']
            if table_name not in schema:
                schema[table_name] = {
                    'columns': [],
                    'foreign_keys': [],
                    'description': ''
                }
            schema[table_name]['columns'].append({
                'name': row['COLUMN_NAME'],
                'type': row['DATA_TYPE'],
                'comment': row['COLUMN_COMMENT'],
                'nullable': row['IS_NULLABLE'],
                'key': row['COLUMN_KEY']
            })
        
        # 添加外键关系
        for fk in foreign_keys:
            table_name = fk['TABLE_NAME']
            if table_name in schema:
                schema[table_name]['foreign_keys'].append({
                    'column': fk['COLUMN_NAME'],
                    'references': fk['REFERENCED_TABLE_NAME'],
                    'ref_column': fk['REFERENCED_COLUMN_NAME']
                })
        
        cursor.close()
        conn.close()
        return schema
    except Exception as e:
        print(f"获取数据库结构出错: {str(e)}")
        return None
    
def format_schema_for_prompt(schema: Dict) -> str:
    """将数据库结构格式化为提示文本"""
    schema_text = []
    for table_name, table_info in schema.items():
        # 表信息
        table_desc = f"表名: {table_name}\n"
        
        # 列信息
        columns = []
        for col in table_info['columns']:
            col_desc = f"  - {col['name']} ({col['type']})"
            if col['comment']:
                col_desc += f" - {col['comment']}"
            if col['key'] == 'PRI':
                col_desc += " [主键]"
            elif col['key'] == 'MUL':
                col_desc += " [外键]"
            columns.append(col_desc)
        
        # 外键关系
        fk_relations = []
        for fk in table_info['foreign_keys']:
            fk_relations.append(
                f"  - {fk['column']} 关联到 {fk['references']}.{fk['ref_column']}"
            )
        
        # 组合表描述
        table_desc += "列:\n" + "\n".join(columns)
        if fk_relations:
            table_desc += "\n外键关系:\n" + "\n".join(fk_relations)
        
        schema_text.append(table_desc)
    
    return "\n\n".join(schema_text)

def clean_sql_query(sql_query: str) -> str:
    """清理SQL查询，移除前缀和注释"""
    # 移除可能的前缀
    prefixes = ['sql', 'SQL', 'sql:', 'SQL:', 'sql ', 'SQL ']
    for prefix in prefixes:
        if sql_query.lower().startswith(prefix):
            sql_query = sql_query[len(prefix):].strip()
    
    # 移除注释
    if '--' in sql_query:
        sql_query = sql_query.split('--')[0].strip()
    if '/*' in sql_query:
        sql_query = sql_query.split('/*')[0].strip()
    
    return sql_query

def generate_sql_query(question: str, schema: Dict) -> str:
    """使用LLM根据自然语言问题生成SQL查询"""
    llm = ChatOllama(model="qwen2.5:7b", temperature=0.7)
    
    schema_text = format_schema_for_prompt(schema)
    
    prompt = f"""你是一个SQL专家，需要根据用户的问题生成SQL查询。

    数据库结构:
    {schema_text}
    
    用户问题: {question}
    
    请生成一个SQL查询来回答这个问题。考虑：
    1. 需要使用哪些表和列
    2. 表之间的关联关系
    3. 适当的WHERE条件
    4. 必要的GROUP BY和ORDER BY
    5. 是否需要子查询或JOIN
    
    重要规则：
    1. 只返回纯SQL查询语句，不要包含任何前缀（如'sql'、'SQL'等）
    2. 不要包含任何解释或注释
    3. 查询语句必须直接以SELECT、INSERT、UPDATE或DELETE开头
    4. 不要添加任何额外的文本或格式
    
    正确示例：
    输入：查询所有用户信息
    输出：SELECT * FROM users
    
    错误示例：
    输入：查询所有用户信息
    输出：sql SELECT * FROM users
    输出：SQL查询：SELECT * FROM users
    输出：SELECT * FROM users; -- 查询所有用户
    
    只返回SQL查询语句，不要包含其他内容"""
    
    try:
        response = llm.invoke(prompt)
        # 清理SQL查询
        sql_query = clean_sql_query(response.content.strip())
        return sql_query
    except Exception as e:
        print(f"生成SQL查询出错: {str(e)}")
        return None
    
def interpret_results(question: str, results: list, schema: Dict) -> str:
    """使用LLM解释查询结果"""
    llm = ChatOllama(model="qwen2.5:7b", temperature=0.7)
    
    # 获取相关表的结构信息
    relevant_tables = set()
    for result in results:
        for key in result.keys():
            for table_name, table_info in schema.items():
                if any(col['name'] == key for col in table_info['columns']):
                    relevant_tables.add(table_name)
    
    # 格式化相关表的结构
    relevant_schema = {k: v for k, v in schema.items() if k in relevant_tables}
    schema_text = format_schema_for_prompt(relevant_schema)
    
    prompt = f"""你是一个数据分析专家，需要解释数据库查询结果。
    
    相关表结构:
    {schema_text}
    
    用户问题: {question}
    查询结果: {results}
    
    请根据查询结果提供清晰的分析和解释：
    1. 总结主要发现
    2. 解释数据之间的关系
    3. 如果有异常值或特殊模式，请指出
    4. 如果结果不能完全回答问题，请说明原因
    
    用自然语言回答，保持专业性和准确性。"""
    
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        print(f"解释结果出错: {str(e)}")
        return None

def query_database(question: str) -> str:
    """使用自然语言查询数据库的主函数"""
    try:
        # 获取数据库结构
        schema = get_database_schema()
        if not schema:
            return "无法获取数据库结构信息"
        
        # 生成SQL查询
        sql_query = generate_sql_query(question, schema)
        if not sql_query:
            return "无法生成SQL查询"
        
        print(f"生成的SQL查询: {sql_query}")  # 调试输出
        
        # 执行查询
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not results:
            return "未找到相关数据"
        
        # 解释结果
        answer = interpret_results(question, results, schema)
        return answer if answer else "无法解释查询结果"
        
    except Exception as e:
        return f"查询过程中出错: {str(e)}"