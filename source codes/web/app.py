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
        if login_type == 'user':
            if Db.login_user(username, password) >= 1:
                session['user_id'] = Db.login_user(username, password)
                session['username']=username#存储用户
                session['user_type'] = 'user'
                session['user'] = Db.get_user(session['user_id'])
                if remember:
                    session.permanent = True
                return redirect(url_for('userboard'))
            else:
                error = "用户账号或密码错误"
        elif login_type == 'business':
            if Db.login_business(username, password) >= 1:
                session['business_id'] = Db.login_business(username, password)
                session['businessname'] =username
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
    session['username']=session['user'][0][1]
    return  render_template('users.html')


@app.route('/restrants')
def restaurants():
    restrants = Db.get_restrant()
    return render_template('restrants.html', restrantdata=restrants)

@app.route('/dishes')
def dishes():
    restrantid = int(request.args.get('restrantid'))
    dishes = Db.get_dishs(restrantid)
    return render_template('dishes.html',dishes=dishes)

@app.route('/myorders', methods=['GET', 'POST'])
def myorders():
    myorder=Db.get_orders_with_userid(session['user_id'])
    return render_template('myorder.html', orders=myorder)


# 修改后的Flask路由
@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    order_id = request.args.get('order_id')
    evaluate = Db.get_orders_with_orderid(order_id)
    if request.method == 'POST':
        rating=request.form.get('rating')
        comment=request.form.get('comment')
        print(rating,comment)
        return redirect(url_for('myorders'))
    return render_template('evaluate.html',
                           evaluate=evaluate)


@app.route('/recommend')
def recommend():
    restrant1=(1, '美食广场', '东区活动中心', '中', '900', '8:00-19:00', '晚')
    restrant2=(2, '小高米线', '东区活动中心', '科', '2900', '8:00-19:00','晚餐')
    restrant3=(3, '小马烧烤', '东区活动中心', '大', '2090', '8:00-19:00','晚餐')
    restrant9=(3, '小马烧烤', '东区活动中心', '大', '2090', '8:00-19:00','晚餐')
    hotrestrants =[restrant1, restrant2, restrant3, restrant9]
    restrant4 = (1, '美食广场', '东区活动中心', '中', '900', '8:00-19:00', '晚','3')
    restrant5 = (2, '小高米线', '东区活动中心', '科', '2900', '8:00-19:00', '晚餐','5')
    restrant6 = (3, '小马烧烤', '东区活动中心', '大', '2090', '8:00-19:00', '晚餐','6')
    highscore_restrants=[restrant4, restrant5, restrant6]
    cuisine_restrant=[restrant1, restrant2, restrant3]
    history_restrant=[restrant1, restrant2, restrant3]

    return render_template('recommend.html', hotrestrants=hotrestrants,
                           highscore_restrants=highscore_restrants,
                           cuisine_restrant=cuisine_restrant,history_restrant=history_restrant)






@app.route('/usercenter')
def usercenter():

    session['user'] = Db.get_user(session['user_id'])
    username=session['user'][0][1]
    userid=session['user'][0][0]
    userpassword=session['user'][0][2]
    userphone=session['user'][0][3]
    return render_template('SelfCenter.html',
                           username=username,
                           userid=userid,
                           userpassword=userpassword,
                           userphone=userphone)



@app.route('/update_user', methods=['POST'])
def update_user():
    if request.method == 'POST':
       new_username = request.form['username']
       new_password = request.form['password']
       new_phone = request.form['phone']
       Db.update_user(session['user_id'], new_username, new_password, new_phone)
       session['user'] = Db.get_user(session['user_id'])
       return redirect(url_for('userboard'))











#商家界面
@app.route('/businessboard')
def businessboard():
    return  render_template('business.html')

@app.route('/bosscenter')
def bosscenter():

    session['business'] = Db.get_business(session['business_id'])
    username=session['business'][0][2]
    userid=session['business'][0][0]
    userpassword=session['business'][0][3]
    userphone=session['business'][0][1]
    return render_template('BossSelfCenter.html',
                           username=username,
                           userid=userid,
                           userpassword=userpassword,
                           userphone=userphone)



@app.route('/update_boss', methods=['POST'])
def update_boss():
    if request.method == 'POST':
       new_username = request.form['username']
       new_password = request.form['password']
       new_phone = request.form['phone']
       Db.update_business(session['business_id'], new_username, new_password, new_phone)
       session['business'] = Db.get_business(session['business_id'])
       return redirect(url_for('businessboard'))


@app.route('/staff')
def staff():
    business_id = session['business_id']
    staffs = Db.get_employees_with_restrantid(business_id)
    return render_template('staff.html', staffs=list(staffs))

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.form.get('name')
    position = request.form.get('position')
    contact = request.form.get('contact')
    business_id = session['business_id']
    pno = request.form.get('pno')
    if not all([name, position, contact]):
        return jsonify({"success": False, "message": "缺少必要参数"})
    Db.add_employee(pno,name, position, contact, business_id)
    return redirect(url_for('staff'))

@app.route('/update_employee', methods=['POST'])
def update_employee():
    pno = request.form.get('pno')
    name = request.form.get('name')
    position = request.form.get('position')
    contact = request.form.get('contact')
    if not all([pno, name, position, contact]):
        return jsonify({"success": False, "message": "缺少必要参数"})
    Db.update_employee(pno, name, position, contact)
    return redirect(url_for('staff'))

@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    pno = request.form.get('pno')
    if not pno:
        return jsonify({"success": False, "message": "缺少员工ID"})
    Db.delete_employee(pno)
    return redirect(url_for('staff'))
























if __name__ == '__main__':
    app.run(debug=True, port=5000)




