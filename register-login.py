from sqlmodel import Field, SQLModel, create_engine, Session
from typing import Optional
from flask import Flask, request, jsonify

class UserInformation():
    def _init_(self,name,password):
        self.name = name
        self.password = password


app = Flask(__name__)
database_ur1 = "sqlite:///database.db"#SQLite数据库app = Flask(__name__)的URL
engine = create_engine(database_ur1)#创建SQLite数据库引擎并链接到数据库
SQLModel.metadata.create_all(engine)#创建表格



class User(SQLModel,table = True):#创建表的结构，创建一个类，里面有id,name,password
    id:Optional[int] = Field(default=None,primary_key=True)#定义了一个可选的整数字段id,默认值为none
    name:str
    password:str


@app.route('/register',methods = ['post'])#/register是指定的URL路由。methods=['post']表示这个路由只能通过 HTTP POST 方法访问。
def register():#用户注册
    data = request.get.json()
    name = data['name']
    password = data['password']

    user_info = UserInformation(name=name,password=password)

    with Session(engine) as session:#在会话中执行数据库操作
        user = User(name = user_info.name,password = user_info.password)
        session.add(user)#将其添加到数据库中
        session.commit() #并来提交更改。

    return jsonify({'message': 'Invalid username or password'})


@app.route('/login',methods=['post'])
def login():#用户登录
    data = request.get_json()
    name = data['name']
    password = data['password']
    """从request对象中获取请求的JSON数据,
    并将其存储在data变量中"""

    user_info = UserInformation(name = user_info.name,password = user_info.password)

    with Session(engine) as session:#创建一个会话对象session.会话对象负责管理数据库连接和事务处理
        user = session.exec(User).where(User.name == user_info.name).first()
        """筛选条件，用于指定查询的用户名必须与输入的 name 变量匹配。.first()
          表示只返回查询结果的第一个对象。"""
        if user and user.password == user_info.password:
            return jsonify({'message':'登录成功'})
    return jsonify({'message':'登录失败'})
    """如果用户的名字和密码匹配，返回登录成功。否则返回登录失败"""

@app.route('/forget_password',methods = ['post'])
def forget():
    data = request.get_json()
    name = data['name']
    new_password = data['new_password']
    user_info = UserInformation(name = user_info.name,password = '')

    with Session(engine) as session:
        user =  session.exec(User).where(User.name == user_info.name).first()
        if user:
            user.password = new_password
            session.commit()
            return jsonify({'message':'密码重置成功'})

    


if __name__=='__main__':
    app.run()