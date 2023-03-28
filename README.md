# FileTrans

## 部署和使用

- Server端先配置好mysql环境，根据`document.md`中的内容建立好数据库和数据表
- 

- Server端根据情况修改MysqlHandler.py文件中的数据库连接信息

- Server端根据情况修改Server.py文件中的监听端口号
- 
- Client端根据情况修改Main.py文件中的`SERVER_IP`和`SERVER_PORT`
- 
- Server和Client运行前安装所需第三方包`pip install -r requirements.txt`
- 
- Server命令`python Server.py`

- Client命令`python Main.py`

## 注意

测试过程中发现，linux和windows环境下对于Crypto第三方包有不兼容现象。

windows环境下修改`Server.py#13`为如下内容

```python
from Crypto.Hash import SHA256
```

linux环境下修改`Server.py#13`为如下内容

```python
from Cryptodome.Hash import SHA256
```

## 演示视频

https://www.bilibili.com/video/BV19T411z7ZN/


