from app import db


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


class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(20), unique=True, nullable=False)
    admin_password = db.Column(db.String(50), nullable=False)


class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    ISBN = db.Column(db.String(13), nullable=False, unique=True)
    total_quantity = db.Column(db.Integer, nullable=False)
    remaining_quantity = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'book_title': self.book_title,
            'author': self.author,
            'publisher': self.publisher,
            'ISBN': self.ISBN,
            'total_quantity': self.total_quantity,
            'remaining_quantity': self.remaining_quantity
        }
