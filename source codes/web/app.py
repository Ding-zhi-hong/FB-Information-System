from flask import Flask, render_template, request, redirect, url_for, session, jsonify,flash
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
            if Db.login_user(username, password) >= 1:
                session['user_id'] = Db.login_user(username, password)   #存储用户
                session['user_type'] = 'user'
                if remember:
                    session.permanent = True

                return redirect(url_for('userboard'))
            else:
                error = "用户账号或密码错误"
        elif login_type == 'business':
            if Db.login_business(username, password) >= 1:
                session['business_id'] = Db.login_business(username, password)   #存储商家
                session['user_type'] = 'business'
                if remember:
                    session.permanent = True

                return redirect(url_for('businessboard'))
            else:
                error = "商家名称或密码错误"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'username' in request.form:  # 用户注册
            username = request.form.get('username')
            password = request.form.get('password')
            phone = request.form.get('phone')
            Db.register_user(username, password,phone)
            return redirect(url_for('login'))

        elif 'merchant_name' in request.form:  # 商家注册
            merchant_name = request.form.get('merchant_name')
            password = request.form.get('password')
            phone = request.form.get('phone')
            Db.register_business(phone,merchant_name, password)
            return redirect(url_for('login'))

    return render_template('register.html')


#用户界面
@app.route('/userboard')
def userboard():
    return  render_template('user.html')


#商家界面
@app.route('/businessboard')
def businessboard():
    return  render_template('business.html')






























if __name__ == '__main__':
    app.run(debug=True, port=5000)




