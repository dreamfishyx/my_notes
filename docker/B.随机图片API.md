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
    
    
# 暴露应用运行的端口
EXPOSE 5000

# 指定运行应用的命令
CMD ["python", "app.py"]
```



##### 构建和运行

1. 在`images`中准备好图片文件。
2. 在包含`Dockerfile`和`app.py`的目录中运行`docker build -t random-image-api .`构建Docker镜像。构建完成后，可以使用命令`docker run -dp 5000:5000 --name api random-image-api`运行容器。
3. 启动容器后手动运行`docker exec -it api /app/update_api_key.sh`(容器名按照自己的来)更新key
4. 通过访问`http://localhost:5000/random-image?key=xxxxxxxxxxxx`来测试`API`，它会随机返回一张图片。

> 若是构建过程中拉取镜像超时,可以尝试使用镜像加速。但是目前很多镜像加速都用不了,额...可以试着自己利用开源项目搭建一个自己的私人镜像加速。



http://60.204.217.126/:5000/random-image?ffbcbcec6b50136ad59d306c3c7ac1dbc3ab32e24c499ba3f8ebbe7dd85ecd39



##### 部署私人dockerhub

1. 配置私人Docker Hub(Docker Registry)可以让你在自己的服务器上托管Docker镜像，而不依赖于Docker官方的Hub。

2. 确保已经安装docker并且docker服务已经启动：

   ```bash
   # 安装docker(略)
   
   sudo systemctl start docker
   sudo systemctl enable docker
   docker --version
   ```

3. Docker官方提供了一个`registry`镜像，可以直接使用来运行私有Registry,使用以下命令在服务器上启动一个私有Registry,这会在后台启动一个私有的Docker Registry,并将其端口映射到服务器的5000端口:

   ```bash
   docker run -d -p 5000:5000 --name registry registry:2
   ```

4. 假设你已经构建了一个Docker镜像并命名为`random-image-api`，你可以将其推送到你的私有Registry。

   1. 首先，需要给镜像打标签，以便推送到私有Registry中。假设你的私有Registry运行在`<your-server-ip>`上：

      ```bash
      docker tag random-image-api <your-server-ip>:5000/random-image-api
      ```

   2. 然后，将镜像推送到私有Registry：

      ```bash
      docker push <your-server-ip>:5000/random-image-api
      ```

   3. 在其他机器上，你可以使用以下命令从私有Registry中拉取镜像：

      ```bash
      docker pull <your-server-ip>:5000/random-image-api
      ```

5. (可选)默认情况下，Docker会要求Registry使用HTTPS。如果你的私有Registry没有配置HTTPS，你可以在客户端上配置Docker以允许使用HTTP。在Docker客户端的`/etc/docker/daemon.json`文件中添加以下内容：

   ```json
   {
     "insecure-registries": ["<your-server-ip>:5000"]
   }
   ```

6. 保存文件后,重启Docker服务`sudo systemctl restart docker`

7. (可选)默认情况下，Registry会将镜像存储在容器内部。为了实现持久化存储，可以将数据挂载到宿主机上的某个目录。

   ```bash
   docker run -d -p 5000:5000 --name registry \
     -v /path/to/your/data:/var/lib/registry \
     registry:2
   ```

8. 为了保护你的私有Registry，你可以配置身份验证(Basic Authentication)和TLS证书。这需要额外的设置,比如使用`htpasswd`生成用户认证文件，并配置Docker Registry使用自签名或正式的TLS证书。可以通过以下文档获取更多详细信息：[官方文档](https://distribution.github.io/distribution/)。



##### 部署API

将Docker镜像推送到个人docker hub上,并在服务器上拉取并运行它。这样，你就可以在服务器上通过访问`http://<server-ip>:5000/random-image`来获取随机图片了。

```bash
# 推送
docker tag random-image-api your-dockerhub-username/random-image-api
docker push your-dockerhub-username/random-image-api


# 拉取
docker pull your-dockerhub-username/random-image-api
docker run -d -p 5000:5000 your-dockerhub-username/random-image-api
```





