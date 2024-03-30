from extension import db


# 构建模型类  类->表  类属性->字段  实例对象->记录
class Readers(db.Model):
    __tablename__ = 'readers'  # 设置表名, 表名默认为类名小写
    reader_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reader_name = db.Column(db.String(50), unique=True, nullable=False)
    reader_password = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.Date, nullable=False)
    reader_type = db.Column(db.Enum('teacher', 'student'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=True)
    account_balance = db.Column(db.Numeric(10, 2), default=0.00, nullable=True)
