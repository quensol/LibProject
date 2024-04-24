# 设置一个用于加密 session 数据的密钥
SECRET_KEY = 'WZ7+fw,=AQ0Cx?sis_>rz1W3'
# 设置数据库连接地址
DB_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/akashi'
SQLALCHEMY_DATABASE_URI = DB_URI
# 是否追踪数据库修改，一般不开启, 会影响性能
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 是否显示底层执行的SQL语句
SQLALCHEMY_ECHO = True
