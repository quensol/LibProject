from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/user/<username>')
def show_user_profile(username):
    if username == '赵中华' or username == '蒋杜飞':
        existed = 1;
    else:
        existed = 0;
    return render_template('user.html', user=username, existed=existed)


if __name__ == '__main__':
    app.run(debug=True)
