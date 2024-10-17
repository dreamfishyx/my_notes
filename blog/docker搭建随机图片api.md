> 注意：若要为随机图片api配置域名并设置反向代理时，不要开启反向代理的缓存设置(会导致一直拿到同一张图)！！！

##### 起因

1. 在搭建个人博客时，希望文章封面可以不用每次手动设计，而是随机获取。而恰好butterfly主题提供了对应设置，于是就想自己部署一个自己的api。
2. 将想法提供个chatgpt，它提出采用flask框架搭建。为了防止被其他人直接访问，又配置了api key的验证方式(虽然很简陋)。由于最近在学习docker，且本博客也是采用1panel面板搭建，于是将api配置成dockerfile，从而实现在docker中部署。
3. 项目地址：[random_image_api](https://github.com/dreamfishyx/random_image_api)（目前，发现一些不合理的地方，不应该每次访问都扫描获取图片列表，实际上只需要在修改图片名称等操作后更新图片列表。此外，docker的一些细节上，也有带改进，例如使用数据卷实现添加图片，后续学完docker知识后有时间会更正。）





##### 项目结构

```markdown
/image-api
|-- Dockerfile (docker镜像构建文件)
|-- app.py (服务)
|-- api_key.txt (初始key)
|-- convert_images.sh (将/images图片转为webp格式,非图片删除,可能会误删,建议图片格式png、jpg、webp)
|-- update_api_key.sh (生成或更新key)
|-- /images (存放用于随机读取的图片)
```





##### 使用

1. 使用前提：正确安装`docker`,并可以正常拉取镜像。

2. 克隆仓库：(图片内存有点的,可能有些慢,可以尝试直接复制文件内容)

   ```bash
   git clone https://github.com/dreamfishyx/random_image_api.git
   
   cd ./random_image_api
   ```

3. 在`images`中准备好你所需要的图片文件(非图片格式在构建镜像时会被删除)。`images`中内置一些我自己收藏的壁纸(图片来源于网络,不可商用),不喜欢的可以自行筛选删除,但请确保构建镜像前`images`文件夹不为空。

4. 构建并启动镜像后重置key(镜像名、容器名可自定义)：

   ```bash
   # 构建镜像
   docker build -t random-image-api .
   
   # 运行容器
   docker run -dp 5000:5000 --name api random-image-api
   
   # 更新key
   docker exec -it api /app/update_api_key.sh
   ```

5. 初始key在`api_key.txt`中,但是不建议使用。请按照上述命令更新key,更新后原来的key失效(含初始key)。

6. 通过访问`http://localhost:5000/random-image/xxxxxx you key xxxxxx`来测试`API`，它会随机返回一张图片。



##### app.py介绍

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





##### **update_api_key.sh**

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





##### **Dockerfile**

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
    
    
# 暴露应用运行的端口
EXPOSE 5000

# 指定运行应用的命令
CMD ["python", "app.py"]
```