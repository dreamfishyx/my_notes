> 1. 以下都是基于ubuntu22.04(个人华为云服务器的`linux`发行版本),其他`linux`发行版命令略有差异。
> 2. `chatgpt`用的好,能解决很多问题(gpt可以分析错误日志报告)。之前脑子里很多想法不知到怎么实现,都是`chatgpt`提供实现思路。u例如这次,我在找的参考大部分都是用的`php`,但是我没学过`php`,不过对python的一些框架还是比较熟。



##### 项目结构

```tex
/image-api
|-- Dockerfile (docker镜像构建文件)
|-- app.py (服务)
|-- api_key.txt (初始key)
|-- convert_images.sh (将/images图片转为webp格式,非图片删除,可能会误删,建议图片格式png、jpg、webp)
|-- update_api_key.sh (生成或更新key)
|-- /images (存放用于随机读取的图片)
```





##### convert_images.sh

```bash
#!/bin/bash

# 进入图片目录
cd /app/images || exit

for file in *; do
  # 如果文件是webp格式，直接跳过
  if [[ "$file" == *.webp ]]; then
    echo "$file is already in WEBP format. Skipping..."
    continue
  fi

  # 检查文件是否为图片类型
  if file "$file" | grep -qE 'image|bitmap'; then
  	# 修复sRGB配置文件问题
    mogrify -strip "$file"
    echo "Converting $file to WEBP format..."
    # 其他图片格式转换为WEBP
    cwebp -quiet "$file" -o "${file%.*}.webp"
    # 删除原始文件
    rm "$file"
  else
  	# 删除非图片文件
    echo "$file is not an image. Deleting..."
    rm "$file"
  fi
done
```





##### update_api_key.sh

```bash
#!/bin/bash

# 定义API密钥存储文件路径
API_KEY_FILE="/app/api_key.txt"

# 生成新的API密钥
new_key=$(openssl rand -hex 32)

# 将新密钥覆盖写入文件
echo "$new_key" > "$API_KEY_FILE"

# 打印新生成的API密钥，使用颜色和格式使其更显眼
echo -e "\n\033[1;32m========================================"
echo -e "New API key generated:"
echo -e "\033[1;31m$new_key\033[0m"  # 红色加粗显示API密钥
echo -e "\033[1;32m========================================\033[0m\n"
```







##### 初始key(api_key.txt)

```tex
f52b63814da6efc0d3e5fa5d7ba5790698ee87a34c4fb2c15de9520155ea82cb
```

> 启动容器后手动运行`docker exec -it api /app/update_api_key.sh`(容器名按照自己的来)更新key





##### 编写API服务(app.py)

可以使用Python的Flask框架来快速构建一个简单的`API`服务。

```python
from flask import Flask, request, jsonify, send_file
from functools import wraps
from flask_cors import CORS  # 导入 CORS
import os
import secrets
import random

app = Flask(__name__)
CORS(app) 
"""
启用跨域支持，默认允许所有来源
如果想限制允许访问的域名，在CORS中传入特定参数，如:
CORS(app, origins=['https://example.com'])
"""

# API密钥存储文件路径
API_KEY_FILE = '/app/api_key.txt'

# 从文件中读取API密钥
def read_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as f:
            return f.read().strip()
    return None

# 验证请求中提供的API密钥
def verify_api_key(token):
    stored_key = read_api_key()
    return stored_key and secrets.compare_digest(stored_key, token)

# 装饰器：验证API密钥
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从路径参数中获取API密钥
        token = kwargs.get('key')
        if not token or not verify_api_key(token):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# 提供随机图片的API，要求提供API密钥作为路径参数
@app.route('/random-image/<key>', methods=['GET'])
@require_api_key
def random_image(key):
    # 确保图片目录存在
    image_dir = '/app/images'
    if not os.path.exists(image_dir):
        return jsonify({"error": "Image directory not found"}), 404
    
    # 获取目录下所有的图片文件
    images = [f for f in os.listdir(image_dir) if f.endswith('.webp')]
    if not images:
        return jsonify({"error": "No images found"}), 404
    
    # 随机选择一张图片
    selected_image = os.path.join(image_dir, random.choice(images))
    
    # 发送图片文件作为响应
    return send_file(selected_image, mimetype='image/webp')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    """
    app.run(): 启动 Flask 的内置开发服务器。
	host='0.0.0.0': 将应用绑定到所有可用的网络接口，使得外部设备也能访问该服务。
	port=5000: 将服务器绑定到5000端口，使服务在该端口上监听HTTP请求。
    """
```

```python
from flask import Flask, request, jsonify, send_file
from functools import wraps
from flask_cors import CORS
import os
import secrets
import random
import subprocess
import logging

app = Flask(__name__)
CORS(app)
"""
启用跨域支持，默认允许所有来源
如果想限制允许访问的域名，在CORS中传入特定参数，如:
CORS(app, origins=['https://example.com'])
"""

# api秘钥文件
API_KEY_FILE = '/app/api_key.txt'
# 图片目录
IMAGE_DIR = '/app/images'
# 脚本
SHELL_UPDATE_API_KEY = '/app/update_api_key.sh'
SHELL_CONVERT_IMAGES = '/app/convert_images.sh'
# API密钥
app.config['API_KEY'] = None
# 维护图片列表
app.config['IMAGE_LIST'] = []

# 检查文件是否存在(仅支持flask cli函数调用,因为没有后续处理逻辑)
def check_file_exists(path):
    if not os.path.exists(path):
        logging.error(f'{path} not found. Exiting...')
        return False
    return True

# 更新API密钥
@app.cli.command("update-api-key")
def update_api_key():
    # 检查文件是否存在
    if not check_file_exists(SHELL_UPDATE_API_KEY):
        return
    
    try:
        # 更新API密钥文件
        subprocess.run([SHELL_UPDATE_API_KEY], check=True)
        # 重新读取API密钥
        app.config['API_KEY'] = read_api_key()
        logging.info(f'{SHELL_UPDATE_API_KEY} executed successfully.')
    except Exception as e:
        logging.error(f'Error executing {SHELL_UPDATE_API_KEY}: {e}')

# 从文件中读取API密钥
def read_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as f:
            key = f.read().strip()
            if key:
                return key
    logging.error(f'API key file {API_KEY_FILE} not found or empty.Try run "update-api-key" command.')
    return None

# 验证请求中提供的API密钥
def verify_api_key(token):
    stored_key = app.config['API_KEY']  # 直接使用全局变量API_KEY
    return stored_key and secrets.compare_digest(stored_key, token)

# 装饰器：验证API密钥
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从url参数或请求头中获取API密钥
        token = kwargs.get('key') or request.args.get('key')
        if not token or not verify_api_key(token):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# 解析图片列表
def parse_image_list():
    # 检查目录是否存在，不存在则创建
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    app.config['IMAGE_LIST'] = [f for f in os.listdir(IMAGE_DIR) if f.endswith('.webp')]
    logging.info(f"Initialized with {len(app.config['IMAGE_LIST'])} images.")

# 更新并转换图片
def convert_and_update_images():
    try:
        # 检查文件是否存在
        if not check_file_exists(SHELL_CONVERT_IMAGES):
            return
        # 执行转换脚本
        subprocess.run([SHELL_CONVERT_IMAGES], check=True)
        # 更新图片列表
        parse_image_list()
        logging.info(f'{SHELL_CONVERT_IMAGES} executed successfully.')
    except Exception as e:
        logging.error(f'Error executing {SHELL_CONVERT_IMAGES}: {e}')

# 随机获取一张图片
@app.route('/random-image/<key>', methods=['GET'])
@require_api_key
def random_image(key):
    if not app.config['IMAGE_LIST']:
        return jsonify({"error": "No images found"}), 404

    selected_image = random.choice(app.config['IMAGE_LIST'])
    return send_file(os.path.join(IMAGE_DIR, selected_image), mimetype='image/webp')

# 更新图片列表和转换图片格式
@app.cli.command("update-images")
def update_images():
    convert_and_update_images()
    logging.info("Images converted and list updated.")

if __name__ == '__main__':
    # 初始化图片列表
    parse_image_list()
    # 初始化API密钥
    app.config['API_KEY'] = read_api_key()
    if not app.config['API_KEY']:
        logging.error("API key not found or invalid. Exiting.")
        exit(1)
    # 设置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # 启动应用
    app.run(host='0.0.0.0', port=5000)
    """
    app.run(): 启动 Flask 的内置开发服务器。
	host='0.0.0.0': 将应用绑定到所有可用的网络接口，使得外部设备也能访问该服务。
	port=5000: 将服务器绑定到5000端口，使服务在该端口上监听HTTP请求。
    """
```

> ### 1. **使用 `os.system()` 执行脚本**
>
> 这是最简单的方式，可以直接调用操作系统的命令来执行脚本。适用于简单的命令执行。
>
> ```
> python复制代码import os
> 
> # 执行脚本文件
> os.system('bash script.sh')  # 如果是 Bash 脚本
> os.system('python script.py')  # 如果是 Python 脚本
> ```
>
> ### 2. **使用 `subprocess` 模块**
>
> `subprocess` 模块提供了更强大、更灵活的方式来调用外部程序，它能够更好地处理输出、错误和返回值。
>
> ```
> python复制代码import subprocess
> 
> # 执行 Bash 脚本
> subprocess.run(['bash', 'script.sh'])
> 
> # 执行 Python 脚本
> subprocess.run(['python', 'script.py'])
> ```
>
> 你还可以捕获输出和错误信息：
>
> ```
> python复制代码result = subprocess.run(['python', 'script.py'], capture_output=True, text=True)
> print(result.stdout)  # 打印输出
> print(result.stderr)  # 打印错误
> ```

在 `parse_image_list` 和 `convert_and_update_images` 中使用了 `os.path.exists()` 和 `os.makedirs()` 来确保图片目录存在，这样很好。不过可以考虑在 Flask 应用启动时就检查这些关键文件和目录是否存在，避免每次调用时都做检查。





在你给出的 `require_api_key` 装饰器中，使用 `kwargs.get('key')` 来获取 API 密钥，假设它会通过 URL 路由参数传递，例如 `/random-image/your_api_key`。

不过，如果你希望从 URL 查询参数获取 API 密钥（即 `/random-image?key=your_api_key`），那么需要修改为从 `request.args` 中提取 API 密钥。下面是两种不同的实现方式，分别对应这两种 API 设计：

### 1. **从 URL 路由参数获取密钥（保持现有方式）**：

如果你的 API 路由是 `/random-image/<key>` 这种格式，`kwargs.get('key')` 的用法是正确的。这时 `key` 是路由的一部分：

```
python复制代码# 装饰器：验证API密钥
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = kwargs.get('key')  # 从URL路由参数获取密钥
        if not token or not verify_api_key(token):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function
```

这个情况下，API 调用方式会是这样的：

```
arduino


复制代码
/random-image/your_api_key
```

### 2. **从 URL 查询参数获取密钥**：

如果你希望通过查询参数来传递 API 密钥，例如 `/random-image?key=your_api_key`，则可以改为使用 `request.args.get('key')`：

```
python复制代码# 装饰器：验证API密钥
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('key')  # 从查询参数获取密钥
        if not token or not verify_api_key(token):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function
```

这个情况下，API 调用方式会是：

```
arduino


复制代码
/random-image?key=your_api_key
```

> gpt建议，在启动时判断一些文件或者目录是否存在并处理，后续可以不再判断。未采用，不排除容器运行过程中失手删除某些文件的可能。但在此记录一下，可以作为以后其他项目优化的一个思路。









##### 准备Dockerfile

接下来,需要创建一个`Dockerfile`来定义Docker镜像的构建过程：

```dockerfile
# 使用python基础镜像
FROM python:3.11-slim

# 换源并安装必要的软件包和工具(apt-utils略)
RUN echo "deb http://mirrors.aliyun.com/debian/ bookworm main non-free contrib" > /etc/apt/sources.list \
    && echo "deb-src http://mirrors.aliyun.com/debian/ bookworm main non-free contrib" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian-security bookworm-security main" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.aliyun.com/debian-security bookworm-security main" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian/ bookworm-updates main" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.aliyun.com/debian/ bookworm-updates main" >> /etc/apt/sources.list \
    && pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && apt-get update \
    && apt-get install -y \
       imagemagick \
       libwebp-dev \
       openssl \
       file \
       webp \
    && pip install --upgrade pip \
    && pip install Flask \
  	&& pip install flask-cors \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录并复制文件
WORKDIR /app
COPY . /app

# 使脚本可执行并执行
RUN chmod +x /app/convert_images.sh /app/update_api_key.sh \
    && /app/convert_images.sh 
    
# 设置 FLASK_APP 环境变量
ENV FLASK_APP=app.py   
    
# 暴露应用运行的端口
EXPOSE 5000

# 指定运行应用的命令
CMD ["flask", "run", "--host=0.0.0.0"]
```

```dockerfile
# 使用python基础镜像
FROM python:3.11-slim

# 换源并安装必要的软件包和工具(apt-utils略)
RUN echo "deb http://mirrors.aliyun.com/debian/ bookworm main non-free contrib" > /etc/apt/sources.list \
    && echo "deb-src http://mirrors.aliyun.com/debian/ bookworm main non-free contrib" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian-security bookworm-security main" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.aliyun.com/debian-security bookworm-security main" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian/ bookworm-updates main" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.aliyun.com/debian/ bookworm-updates main" >> /etc/apt/sources.list \
    && pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && apt-get update \
    && apt-get install -y \
       imagemagick \
       libwebp-dev \
       openssl \
       file \
       webp \
    && pip install --upgrade pip \
    && pip install Flask \
  	&& pip install flask-cors \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录并复制文件
WORKDIR /app
COPY . /app

# 使脚本可执行并执行
RUN chmod +x /app/convert_images.sh /app/update_api_key.sh \
    && /app/convert_images.sh 
    
# 设置 FLASK_APP 环境变量
ENV FLASK_APP=app.py   
    
# 暴露应用运行的端口
EXPOSE 5000

# 指定运行应用的命令
CMD ["flask", "run", "--host=0.0.0.0"]
```



> gpt建议将 /app/convert_images.sh  执行过程放到cmd中，即容器执行过程中，以简化容器构建构成。但我觉得会导致容器启动及其缓慢，未采用。但在此记录一下，可以作为以后其他项目优化的一个思路。

##### 构建和运行

1. 在`images`中准备好图片文件。

2. 在包含`Dockerfile`和`app.py`的目录中运行`docker build -t random-image-api .`构建Docker镜像。构建完成后，可以使用命令`docker run -dp 5000:5000 --name api random-image-api`运行容器。

   ```bash
   docker run -v ~/image_api:/app/images -dp 5000:5000 --name image_api random-image-api
   ```

3. 启动容器后手动运行`docker exec -it api /app/update_api_key.sh`(容器名按照自己的来)更新key

4. 通过访问`http://localhost:5000/random-image?key=xxxxxxxxxxxx`来测试`API`，它会随机返回一张图片。

> 若是构建过程中拉取镜像超时,可以尝试使用镜像加速。但是目前很多镜像加速都用不了,额...可以试着自己利用开源项目搭建一个自己的私人镜像加速。



```bash
docker exec -it image_api flask update-api-key

docker exec -it image_api flask update-images
```









http://60.204.217.126/:5000/random-image?ffbcbcec6b50136ad59d306c3c7ac1dbc3ab32e24c499ba3f8ebbe7dd85ecd39



##### 部署私人dockerhub



