from pyprojroot import here
import os
print('--------------------------------')
print(os.path.abspath(os.path.dirname(__file__)).replace('\\', '/'))
print('--------------------------------')
print(here())
print('--------------------------------')
current_file_path = os.path.abspath(__file__)
    # 获取当前文件所在目录
current_dir = os.path.dirname(current_file_path)
current_dir = current_dir.replace('\\', '/')
print(current_dir)
print('--------------------------------')
