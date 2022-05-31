# NinjaXia测试平台

基于 [django-ninja](https://github.com/vitalik/django-ninja)
快速开发的一个简单入门级自动化测试平台后端

萌芽版本迭代接近尾声, 在这里浅浅的做下介绍:

此项目目的是个人练习, 非商业用途, 不提供任何担保, 不提供任何技术支持.

如果你想熟悉此项目的构成, 首先你应该已经了解或使用过
[fastapi](https://fastapi.tiangolo.com/zh/), 这是前提

此项目也是为后期更好的使用 `fastapi` 做的实验品

但是它和 `fastapi` 不同, 由于依赖django, 所以目前此项目为`全局同步`

然后你也应该会浅使用 django-orm, 还接触过一些django基础知识,

最后你阅读过 [django-ninja]() 文档, 虽然大程度上与 `fastapi` 相近, 但还是别有洞天

🔈: 提前告知, 此框架与 `django-rest-framework` 没有任何关系

### 基础开发环境

- Django 3.2.13
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

### 安装使用

```shell
1. 安装依赖
    pip install -r requirements.txt
    
2. 创建数据库
    python manage.py makemigrations
    python manage.py migrate
    
3. 创建超级管理员
    python manage.py createsuperuser
    
4. 启动服务
    python manage.py runserver
    
5. 访问浏览器
    http://127.0.0.1:8000/v1/docs
```
