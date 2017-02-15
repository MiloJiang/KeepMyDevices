## 服务端

## 概要
服务使用 Python 的微框架 Flask 进行开发.

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

* Flask-Security(optional)
需要权限控制 https://github.com/flask-admin/Flask-Admin/tree/master/examples/auth

* Flask-Login
和Flask-Security相比, 页面(template)上的工作量更少一点. Admin页面需要权限控制.