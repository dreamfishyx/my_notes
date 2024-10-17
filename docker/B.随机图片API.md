> 1. 以下都是基于ubuntu22.04(个人华为云服务器的`linux`发行版本),其他`linux`发行版命令略有差异。
> 2. `chatgpt`用的好,能解决很多问题(gpt可以分析错误日志报告)。之前脑子里很多想法不知到怎么实现,都是`chatgpt`提供实现思路。u例如这次,我在找的参考大部分都是用的`php`,但是我没学过`php`,不过对python的一些框架还是比较熟。



##### 项目结构

```tex
./image-api
├── app
│   ├── api_key.txt(初始api_key)
│   ├── app.py(服务)
│   ├── convert_images.sh(将/images图片转为webp格式,非图片删除,可能会误删,建议图片格式png、jpg、webp)
│   └── update_api_key.sh(生成或更新key)
├── Dockerfile(docker镜像构建文件)
└── README.md
```





##### convert_images.sh

```bash
#!/bin/bash

cd /app/images || exit

for file in *; do
  # 跳过已经是 WEBP 格式的文件
  if [[ "$file" == *.webp ]]; then
    echo "$file is already in WEBP format. Skipping..."
    continue
  fi

  # 检查文件是否为常见图片格式（jpg, png, gif等）
   if file "$file" | grep -qE 'image|bitmap'; then
    # 转换图片为 WEBP 格式
    echo "Converting $file to WEBP format..."
    cwebp -quiet "$file" -o "${file%.*}.webp"

    # 检查转换是否成功
    if [[ -f "${file%.*}.webp" ]]; then
      echo "$file successfully converted. Deleting original..."
      rm "$file"
    else
      echo "Failed to convert $file. Skipping deletion."
    fi
  else
    echo "$file is not a supported image format. Deleting..."
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





##### 编写API服务(app.py)

1. 使用 Python 的 Flask 框架来快速构建一个简单的`API`服务: 这里相较于最初版本，添加更新图片的功能。在最初版本，在每一次请求时都需要获取一次图片列表和 api 秘钥，显然这样是十分低效的。实际上对于图片列表和 api 秘钥，大部分时间都是处于不变状态，因此只需要在更新的时候动态维护即可。
2. 此外靠虑了很久，我仍然不认可由 url 控制 api 秘钥和图片列表的更新，这并不安全，即使这样可以简化操作。故而 url 只负责对数据的更新维护，不具有脚本执行的权利，更新脚本仍然需要用户手动执行。
3. 实际上在最初的时候，我并不太看好 url 控制更新。我采用的是 flask cli，这期间也出现一些问题，在此记录一下:
   1. 使用 flask run 启动应用时，Flask 会自己管理应用的启动，而不会执行 app.py 的 `if __name__ == '__main__':` 中的初始化代码。这是因为 `flask run` 会启动 Flask 服务器，而不是通过 `python app.py` 或其他方式直接启动应用。
   1. 使用 flask cli 需要使用 `CMD ["flask run --host=0.0.0.0"]` 启动(并配置启动环境 `ENV FLASK_APP=app.py` )，但是官方不建议在生产环境中使用 flask 内置服务器(即使用 flask run 启动服务)。
   1. 
4. 具体代码及其部分注释如下：

```python
from flask import Flask, request, jsonify, send_file
from functools import wraps
from flask_cors import CORS
import os
import secrets
import random
# import subprocess
import logging
from logging.handlers import RotatingFileHandler

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
# API密钥
app.config['API_KEY'] = None
# 维护图片列表
app.config['IMAGE_LIST'] = []

# 检查文件是否存在
def check_file_exists(path):
    if not os.path.exists(path):
        logging.error(f'{path} not found. Exiting...')
        return False
    return True

# 装饰器：验证API密钥
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
         # 从url参数中获取API密钥
        token = kwargs.get('key')
        # 若从请求头中获取API密钥:request.args.get('key')
        if not token or not verify_api_key(token):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

    
# 更新API密钥(docker exec -it <container_name> update_api_key.sh)
@app.route('/update-key/<key>', methods=['GET'])
@require_api_key
def update_api_key(key):
    # 维护API密钥
    app.config['API_KEY'] = read_api_key()
    if not app.config['API_KEY']:
        return jsonify({"error": "API key not found or invalid"}), 404
    return jsonify({"message": "API key updated successfully"}), 200

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
    stored_key = app.config['API_KEY']  
    return stored_key and secrets.compare_digest(stored_key, token)


# 解析图片列表
def parse_image_list():
    # 检查目录是否存在，不存在则创建
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    app.config['IMAGE_LIST'] = [f for f in os.listdir(IMAGE_DIR) if f.endswith('.webp')]
    logging.info(f"Initialized with {len(app.config['IMAGE_LIST'])} images.")


# 更新并转换图片(docker exec -it <container_name> convert_images.sh)
@app.route('/update-images/<key>', methods=['GET'])
@require_api_key
def update_images(key):
    # 维护图片列表
    parse_image_list()
    # 判断维护结果并做出回应
    if not app.config['IMAGE_LIST']:
        return jsonify({"error": "No images found"}), 404
    return jsonify({"message": "Images list updated"}), 200


# 随机获取一张图片
@app.route('/random-image/<key>', methods=['GET'])
@require_api_key
def random_image(key):
    if not app.config['IMAGE_LIST']:
        return jsonify({"error": "No images found"}), 404
    selected_image = random.choice(app.config['IMAGE_LIST'])
    return send_file(os.path.join(IMAGE_DIR, selected_image), mimetype='image/webp')


# 初始化日志
handler = RotatingFileHandler('/app/log/app.log', maxBytes=10*1024*1024, backupCount=10)
handler.setLevel(logging.INFO)  # 设置信息级别
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
logging.getLogger().addHandler(logging.StreamHandler()) # 确保标准输出也记录日志
logging.getLogger().setLevel(logging.INFO)

# 初始化图片列表
parse_image_list()

# 初始化API密钥
app.config['API_KEY'] = read_api_key()
logging.info(f"API key init:{app.config['API_KEY']}")
if not app.config['API_KEY']:
    logging.error("API key not found or invalid. Exiting.")
    exit(1)
```

````python
from flask import Flask, request, jsonify, send_file
from functools import wraps
from flask_cors import CORS
import os
import secrets
import random
# import subprocess
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
CORS(app)

API_KEY_FILE = '/app/api_key.txt'
IMAGE_DIR = '/app/images'
app.config['API_KEY'] = None
app.config['IMAGE_LIST'] = []

def check_file_exists(path):
    if not os.path.exists(path):
        logging.error(f'{path} not found. Exiting...')
        return False
    return True

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = kwargs.get('key')
        if not token or not verify_api_key(token):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/update-key/<key>', methods=['GET'])
@require_api_key
def update_api_key(key):
    app.config['API_KEY'] = read_api_key()
    if not app.config['API_KEY']:
        return jsonify({"error": "API key not found or invalid"}), 404
    return jsonify({"message": "API key updated successfully"}), 200

def read_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as f:
            key = f.read().strip()
            if key:
                return key
    logging.error(f'API key file {API_KEY_FILE} not found or empty.Try run "update-api-key" command.')
    return None

def verify_api_key(token):
    stored_key = app.config['API_KEY']  
    return stored_key and secrets.compare_digest(stored_key, token)

def parse_image_list():
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    app.config['IMAGE_LIST'] = [f for f in os.listdir(IMAGE_DIR) if f.endswith('.webp')]
    logging.info(f"Initialized with {len(app.config['IMAGE_LIST'])} images.")

@app.route('/update-images/<key>', methods=['GET'])
@require_api_key
def update_images(key):
    parse_image_list()
    if not app.config['IMAGE_LIST']:
        return jsonify({"error": "No images found"}), 404
    return jsonify({"message": "Images list updated"}), 200

@app.route('/random-image/<key>', methods=['GET'])
@require_api_key
def random_image(key):
    if not app.config['IMAGE_LIST']:
        return jsonify({"error": "No images found"}), 404
    selected_image = random.choice(app.config['IMAGE_LIST'])
    return send_file(os.path.join(IMAGE_DIR, selected_image), mimetype='image/webp')

handler = RotatingFileHandler('/app/log/app.log', maxBytes=10*1024*1024, backupCount=10)
handler.setLevel(logging.INFO)  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
logging.getLogger().addHandler(logging.StreamHandler()) 
logging.getLogger().setLevel(logging.INFO)

parse_image_list()

app.config['API_KEY'] = read_api_key()
logging.info(f"API key init:{app.config['API_KEY']}")
if not app.config['API_KEY']:
    logging.error("API key not found or invalid. Exiting.")
    exit(1)
````

> gpt建议，在启动时判断一些文件或者目录是否存在并处理，后续可以不再判断。未采用，不排除容器运行过程中失手删除某些文件的可能。但在此记录一下，可以作为以后其他项目优化的一个思路。



##### 准备Dockerfile

1. 接下来,需要创建一个`Dockerfile`来定义Docker镜像的构建过程。但是在此过程中，还是遇到了一些问题：
   1. 开始时我打算在容器构建时将图片加入到容器并进行格式转换，但是这样会导致容器构建及其缓慢，并且最重要的是后续将系统目录挂载到该位置时，容器的图片文件夹文件夹会被覆盖，功亏一篑。
   2. 于是我又打算不使用系统目录挂载，而是使用数据卷，虽然通过命令很容易知道数据卷位置，但是后续实际操作发现没有权限，根本进不去。
   3. 于是只能退而求其次，先启动容器挂载系统目录，然后再添加图片和装换格式。

2. Dockerfile 文件及其部分注释内容如下:

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
          imagemagick \   # 图片修复时使用
          libwebp-dev \
          openssl \
          file \
          webp \
       && pip install --upgrade pip \
       && pip install Flask \
     	&& pip install flask-cors \
     	&& pip install gunicorn \
       && apt-get clean \
       && rm -rf /var/lib/apt/lists/*
   
   # 设置工作目录并复制文件
   WORKDIR /app
   COPY ./app /app
   
   # 使脚本可执行并执行
   RUN chmod +x /app/convert_images.sh /app/update_api_key.sh 
   
   # 暴露应用运行的端口
   EXPOSE 5000
   
   # 指定运行应用的命令
   CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "--timeout", "37", "app:app"]
   ```

   > gpt 建议将 /app/convert_images.sh  执行过程放到 CMD 中，即容器执行过程中，以简化容器构建构成。但我觉得会导致容器启动及其缓慢，未采用。但在此记录一下，可以作为以后其他项目优化的一个思路。





##### 构建

1. 方式一:使用 docker hub拉取(待补)

2. 方式二:使用阿里云镜像仓库拉取(待补)

3. 方式三:手动构建

   ```bash
   # 克隆
   git clone --depth 1 https://github.com/dreamfishyx/random_image_api.git
   
   # 进入目录
   cd ./random_image_api
   
   # 构建镜像
   docker build -t random-image-api .
   ```


> 若是构建过程中拉取镜像超时,可以尝试使用镜像加速。但是目前很多镜像加速都用不了,额...可以试着自己利用开源项目搭建一个自己的私人镜像加速。

##### 运行

1. 创建并启动容器：

   1. 创建数据卷: `docker volume create random-image-api`。
   2. 创建并运行容器: `docker run -v ~/random-image:/app/images -v ~/flask/log:/app/log -dp 5000:5000 --name image_api random-image-api`。

2. 访问图片：

   1. 查看初始 api-key: `docker exec -it image_api cat /app/api_key.txt`，实际上其默认值为`f52b63814da6efc0d3e5fa5d7ba5790698ee87a34c4fb2c15de9520155ea82cb`。
   2. 访问格式为:`http://localhost:5000/random-image/<your_api_key>`(初始状态没有图片，无法访问，参考下面方式添加图片)。

3. 更新api-key(初始时建议更新):

   1. 首先手动更新 api-key文件:`docker exec -it image_api  /app/update_api_key.sh`(此时应用未更新，api-key未改变)。
   2. 访问`http://localhost:5000/update-key/<your_api_key>`更新应用api-key改变((api-key更新)。

4. 添加或者修改图片:

   1. 向系统目录 `~/random-image` 中添加或者删除图片(非图片格式在构建镜像时会被删除)。

   2. 执行脚本对容器图片进行格式转换:`docker exec -it image_api /app/convert_images.sh`。
   
   3. 访问`http://localhost:5000/update-images/<your_api_key>`更新应用图片列表，需要等待一段时间。
   
5. 目前这个镜像的优化应该会告一段落。



