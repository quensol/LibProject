from flask import session, request, redirect, render_template, make_response

from app import app
from app.models import Admin, Readers, Books


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
    return redirect('/elogin')


@app.route('/index')
def index():
    if 'admin_name' in session:
        inject_global_params()
        response = make_response(render_template('index.html'))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
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


# 通过上下文处理器来注入参数
@app.context_processor
def inject_global_params():
    # 在这个示例中，我们假设有一个用户名参数
    username = session.get('admin_name', None)
    # 获取当前请求中的参数，例如 GET 或 POST 请求
    job = session.get('job', None)
    # 返回一个字典，包含所有要注入到模板中的参数
    return dict(username=username, job=job)


@app.route('/index/return')
def toreturnpage():
    return render_template('returnpage.html', pagename='图书归还')


@app.route('/index/books')
def tobookspage():
    books = Books.query.all()
    return render_template('books.html', pagename='图书信息维护', books=books)


@app.route('/index/searchbook')
def tosearchbookpage():
    return render_template('searchbook.html', pagename='图书信息维护')
