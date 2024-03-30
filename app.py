import datetime

from flask import Flask, url_for, request, redirect, render_template, session
from flask.views import MethodView
from extension import db
from models import Readers

app = Flask(__name__)
# 设置一个用于加密 session 数据的密钥
app.config['SECRET_KEY'] = 'WZ7+fw,=AQ0Cx?sis_>rz1W3'
# 设置数据库连接地址
DB_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/akashi'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
# 是否追踪数据库修改，一般不开启, 会影响性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 是否显示底层执行的SQL语句
app.config['SQLALCHEMY_ECHO'] = True

# 初始化db,关联flask 项目
db.init_app(app)


class ReaderApi(MethodView):
    def get(self, reader_id):
        if not reader_id:
            # Readers是数据库表名，readerslist是查出的列表
            readerslist: [Readers] = Readers.query.all()
            results = [
                {
                    'id': readers.reader_id,
                    'name': readers.reader_name,
                    'password': readers.reader_password,
                    'registration_date': readers.registration_date,
                    'reader_type': readers.reader_type,
                    'is_active': readers.is_active,
                    'account_balance': readers.account_balance
                } for readers in readerslist
            ]
            return {
                'status': 'success',
                'message': '读者数据查询成功',
                'results': results
            }
        single: Readers = Readers.query.get(reader_id)
        return {
            'status': 'success',
            'message': '读者数据查询成功',
            'results': {
                'id': single.reader_id,
                'name': single.reader_name,
                'password': single.reader_password,
                'registration_date': single.registration_date,
                'reader_type': single.reader_type,
                'is_active': single.is_active,
                'account_balance': single.account_balance
            }
        }

    def post(self):
        form = request.json
        newreader = Readers()
        newreader.reader_name = form.get('reader_name')
        newreader.reader_password = form.get('reader_password')
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        newreader.registration_date = now_time
        newreader.reader_type = form.get('reader_type')
        db.session.add(newreader)
        db.session.commit()

        return {
            'status': 'success',
            'message': '数据添加成功'
        }


class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(20), unique=True, nullable=False)
    admin_password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Admin {self.admin_name}>'


# 设置应用上下文
with app.app_context():
    # 创建数据库表
    db.create_all()


# 路由：主页
@app.route('/')
def showlogininfo():
    if 'reader_name' in session:
        return f'已登录，用户名：{session["reader_name"]}'
    if 'admin_name' in session:
        return f'已登录，admin用户，用户名：{session["admin_name"]}'
    return '未登录'


@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    if request.method == 'POST':
        readername = request.form['username']
        password = request.form['password']
        user = Readers.query.filter_by(reader_name=readername, reader_password=password).first()
        if user:
            session['reader_name'] = readername
            return redirect('/')
        else:
            return '登录失败'
    return render_template('login.html')


# 路由：注销
@app.route('/logout')
def logout():
    session.pop('reader_name', None)
    session.pop('admin_name', None)
    session.pop('job', None)
    return redirect('/')


@app.route('/index')
def index():
    if 'admin_name' in session:
        username = session['admin_name']
        job = session['job']
        return render_template('index.html', username=username, job=job)
    return '未登录'


@app.route('/elogin', methods=['GET', 'POST'])
def elogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Admin.query.filter_by(admin_name=username, admin_password=password).first()
        if user:
            session['admin_name'] = username
            session['job'] = 'admin'
            return redirect('/index')
        else:
            return '登录失败'
    return render_template('elogin.html')


reader_view = ReaderApi.as_view('reader_api')
app.add_url_rule('/readers/', defaults={'reader_id': None}, view_func=reader_view, methods=['GET'])
app.add_url_rule('/readers/', view_func=reader_view, methods=['POST'])
app.add_url_rule('/readers/<int:reader_id>', view_func=reader_view, methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
