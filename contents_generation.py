import os 

# 定义常量
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
CONTENT_FILE_NAME = 'readme.md'
CONTENT_HEAD = """
# 目录\n
>  - (本目录文件由脚本自动生成, 不一定准确)该仓库为个人知识库，主要包含了一些学习笔记，技术文档等内容。
>  - 个人博客地址：[Dream sea](https://dreamfish.cc)
>  - leetcode刷题：[力扣刷题日记](./leetcode刷题日记.md)
\n\n
"""

CONTENT_TITLE_LEVEL = 2
# 排除的文件夹
EXCLUDE_DIRS = ['.git', 'assets', '.trash',".obsidian","选择",'temp']

class MdDir:
    def __init__(self, dir_name, level, md_list=None):
        self.dir_name = dir_name
        self.level = level
        self.md_list = md_list if md_list is not None else []

def parse_dir(dir_path: str, content: list, level: int = 0): 
    for dir_path, dir_names, file_names in os.walk(dir_path):
        relative_path = os.path.relpath(dir_path, ROOT_PATH)
        # 将相对路径分割成部分
        path_parts = relative_path.split(os.sep)[0]
        # 排除不需要的文件夹
        if path_parts in EXCLUDE_DIRS:
            continue
        if path_parts == '.':
            continue

        md_list = []
        
        for file_name in file_names:
            if file_name.endswith('.md'):
                file_path = os.path.relpath(os.path.join(dir_path, file_name), ROOT_PATH)
                file_path = file_path.replace('\\', '/')  # 将路径中的反斜杠替换为正斜杠
                file_content = f"- [{file_name[:-3]}](./{file_path})\n"
                md_list.append(file_content)

        if md_list:
            # 排序
            # md_list.sort()
            dir_name = os.path.basename(dir_path)
            dir_level = dir_path.count(os.sep) - ROOT_PATH.count(os.sep)
            new_dir = MdDir(dir_name, dir_level, md_list)
            content.append(new_dir)

# 生成目录文件
def generate_content_file(content: list):
    with open(os.path.join(ROOT_PATH, CONTENT_FILE_NAME), 'w', encoding='utf-8') as f:
        f.write(CONTENT_HEAD)
        for item in content:
            f.write(f"{'#' * (CONTENT_TITLE_LEVEL)} {item.dir_name}\n")
            for md in item.md_list:
                f.write(md)
            f.write('\n\n\n')  # 添加额外换行

if __name__ == '__main__':
    content = []
    parse_dir(ROOT_PATH, content)
    generate_content_file(content)  # 传入content
    print("生成目录文件成功！")
