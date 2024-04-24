from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
# 设置应用上下文
with app.app_context():
    # 创建数据库表
    db.create_all()

from app import views, models
