from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import datas_get_operate as Db


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'



@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login_type = request.form.get('loginType')
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'

        # 验证用户/商家
        if login_type == 'user':
            if Db.login_user(username, password):
                return redirect(url_for('userboard'))
            else:
                error = "用户名或密码错误"
        elif login_type == 'business':
            if Db.login_business(username, password):
                return redirect(url_for('userboard'))
            else:
                error = "商家账号或密码错误"

    return render_template('login.html', error=error)


@app.route('/userboard')
def userboard():
    return  render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))












if __name__ == '__main__':
    app.run(debug=True, port=5000)




