# NinjaXia测试平台

基于 [django-ninja](https://github.com/vitalik/django-ninja)
快速开发的一个简单入门级自动化测试平台后端

**仓库说明**:

&nbsp;&nbsp;&nbsp;
此项目目的是个人练习, 非商业用途, 不提供任何担保, 不提供任何技术支持.

如果你想熟悉此项目的构成, 你应该已经了解或使用过
[fastapi](https://fastapi.tiangolo.com/zh/),

因为此项目也是为后期更好的使用 `fastapi` 做的实验品.

&nbsp;&nbsp;&nbsp;
由于依赖 django, 所以目前此项目设计为全局同步, 如果你想熟悉此项目,

你也应该会浅使用 django-orm, 还接触过一些 django 基础知识, 最后

你阅读过 `django-ninja` 文档, 虽然与 `fastapi` 相近, 但仍别有洞天

🔈: 提示, 此框架与 `django-rest-framework` 没有任何关系

### 基础开发环境

- Django 3.2
- Django-Ninja 0.17.0
- Python 3.8
- MySQL
- HTTPX
- Redis
- Apscheduler
- ......

### 下载

```shell
git clone https://gitee.com/wu_cl/NinjaXia.git
```

## 使用

> ⚠️: 此过程请格外注意端口占用情况, 特别是 8000, 3306, 6379...

### 1. 传统

1. 安装所有依赖
    ```shell
    pip install -r requirements.txt
    ```
2. 创建数据库 ninja_xia，选择 utf8mb4 编码
3. 检查并修改 ninja_xia/settings.py mysql 数据库配置
4. 数据库迁移
   ```shell
   #  生成迁移文件
   python manage.py makemigrations
   
   # 执行迁移
   python manage.py migrate
   ```
5. 百度安装redis客户端, 安装完启动服务
6. 检查并修改 ninja_xia/settings.py redis 数据库配置
7. 执行 `python manage.py runserver` 文件启动服务
8. 浏览器访问: http://127.0.0.1:8000/v1/docs

### 2. docker

1. 在 docker-compose.yml 文件所在目录下执行一键启动命令
   ```shell
   docker-compose up -d --build
   ```
2. 等待命令自动执行完成
3. 浏览器访问: http://127.0.0.1:8000/v1/docs

### 创建管理员用户

`python manage.py createsuperuser`
