## 服务端

## 概要
服务使用 Python 的微框架 Flask 进行开发.

## 快速上手

#### 前提
需要确保已经安装
* Nginx
* Python2.7
* gunicorn
* 其他python组件(可用通过pip install -r requirement.txt安装)

#### 初始化
```
python migrate.py db init
python migrate.py db migrate
python migrate.py db upgrade
```


#### 运行
* 调试

```
python run.py
```


* 部署

gunicorn <AppFileName>:app
AppFileName指的是flask启动文件的名字. 本项目是"run"
所以
```
gunicorn run:app
```


## 开发记录

* 使用flask

* 使用模板

* 加入SQLAlchemy

* 加入Flask-SQLAlchemy


* 接入[Flask-Admin](http://flask-admin.readthedocs.io/en/latest/index.html)

* Create database

```
python db_init.py
```

* 设置flask 的 Security Key
生成
```
import os
os.urandom(24)
>>>'\xb7\x7f\xa6\xdf\xf3\x0f3\xefO\xe7\x9a\xd8?{\x82\xb8\x12R\xda\xee\xd3\xd3\xcb\x9e'
```
配置
```
app.config['SECRET_KEY'] = '\xb7\x7f\xa6\xdf\xf3\x0f3\xefO\xe7\x9a\xd8?{\x82\xb8\x12R\xda\xee\xd3\xd3\xcb\x9e'
```

* Flask-migrate

首次需要生成DB
````
python migrate.py db init
python migrate.py db migrate
python migrate.py db upgrade
````
引入 Migrate 脚本便于我们今后更容易的修改数据的结构.这里需要注意的是, 生成的DB的文件(如果有)的位置最好是绝对路径. 相对路径的话, 容易造成运行脚本时的路径和服务运行的路径不一致.


* 接入Flask-Restless

提供可以API供应用访问

* Flask-Admin

管理页面

* Flask-Security(optional)

需要权限控制 https://github.com/flask-admin/Flask-Admin/tree/master/examples/auth

* Flask-Login

和Flask-Security相比, 页面(template)上的工作量更少一点. 但是两者都需要重写Admin页面来实现针对管理页面的权限管理.


* Flask-JWT
API同样也需要保护
设置完成后, 请求需要第一次访问 "/auth" 获得token, 然后根据这个token加入请求的头部进行访问:
```
Authorization: JWT <token> 
```

* 增加自定义命令支持建立Admin账号

* 实现API