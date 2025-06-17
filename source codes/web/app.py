from flask import Flask, render_template, request, redirect, url_for, session, jsonify,flash
import datas_get_operate as Db
import recommends
import recommends as r
import restrant_operate as restr
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



@app.route('/dishes', methods=['GET', 'POST'])
def dishes():
    restaurant_id = request.args.get('restrantid')  # 从URL获取
    if request.method == 'POST':
        dish_id = request.form.get('dish_id')
        dish_price = request.form.get('dish_price')
        restaurant_id = request.form.get('restaurant_id')
        if dish_id and dish_price and restaurant_id:
            import datetime
            order_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Db.add_cart(restaurant_id, dish_id, dish_price, order_time)
            return redirect(url_for('dishes', restrantid=restaurant_id))
        else:
            print("错误: 缺少必要参数")
            return redirect(url_for('dishes', restrantid=restaurant_id))

    # GET请求处理
    if restaurant_id:
        dishes = Db.get_dishs(restaurant_id)
    else:
        dishes = []
        print("未提供餐厅ID")

    return render_template('dishes.html',
                           dishes=dishes,
                           restaurant_id=restaurant_id)





@app.route('/myorders', methods=['GET', 'POST'])
def myorders():
    myorder=Db.get_orders_with_userid(session['user_id'])
    myorder2=[]
    for order in myorder:
        order2=[]
        order2.append(order[0])
        order2.append(order[1])
        order2.append(order[2])
        order2.append(order[3])
        order2.append(order[4])
        order2.append(order[5])
        if Db.get_score_with_orderid(order[0]):
            order2.append(1)
        else:
            order2.append(0)
        myorder2.append(order2)
    return render_template('myorder.html', orders=myorder2)


# 修改后的Flask路由
@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    order_id = session.get('order_id')
    if request.method == 'GET':
        new_order_id = request.args.get('order_id')
        if new_order_id:
            order_id = new_order_id
            session['order_id'] = order_id
    if not order_id:
        return redirect(url_for('myorders'))
    evaluate = Db.get_orders_with_orderid(order_id)
    if not evaluate:
        flash("未找到相关订单")
        return redirect(url_for('myorders'))
    if request.method == 'POST':
        try:
            rating = request.form.get('rating')
            comment = request.form.get('comment')
            if not all([rating, evaluate[1], evaluate[2], evaluate[3]]):
                flash("缺少必要参数")
                return redirect(url_for('myorders'))
            Db.add_score(
                evaluate[1],
                evaluate[2],
                evaluate[3],
                str(rating),
                comment,
                order_id
            )
            return redirect(url_for('myorders'))
        except (IndexError, TypeError) as e:
            print(f"数据库操作异常: {str(e)}")
            flash("提交评价失败，请重试")
            return redirect(url_for('evaluate'))

    return render_template('evaluate.html', evaluate=evaluate)



@app.route('/recommend')
def recommend():
    hots=recommends.hot()
    hotrestrants=[]
    for h in hots:
        hotrestrants.append(Db.get_restrant_id(h[0]))


    high=recommends.high()
    highscore_restrants=[]
    for h in high:
        highscore_restrants.append(Db.get_restrant_id(h[0]))

    history=recommends.history(session['user_id'])
    history_restrant=[]
    for h in history:
        history_restrant.append(Db.get_restrant_id(h[0]))

    cuisine_restrant=[]

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

@app.route('/append')
def append():
    cart_items=Db.get_cart()
    return render_template('append.html', dishes=cart_items)

@app.route('/cancel', methods=['POST'])
def cancel():
    dish_id = int(request.form.get('dish_id'))
    Db.cancel_cart(dish_id)
    return redirect('/append')

@app.route('/single_order', methods=['POST'])
def single_order():
    dish_id = int(request.form.get('dish_id'))
    restrant_id=int(request.form.get('restrant_id'))
    money=float(request.form.get('money'))
    time=(request.form.get('time'))
    Db.add_order( session['user_id'],restrant_id,dish_id,money,time)
    Db.cancel_cart(dish_id)
    return redirect('/append')

@app.route('/total_order', methods=['POST'])
def total_order():
    carts=Db.get_cart()
    for cart in carts:
        dish_id = cart[1]
        restrant_id = cart[0]
        money = cart[2]
        time = cart[3]
        Db.add_order(session['user_id'], restrant_id, dish_id, money, time)
        Db.cancel_cart(cart[1])
    return redirect('/append')


    









#商家界面
@app.route('/businessboard')
def businessboard():
    if restr.get_restrantid_with_boss(session['business_id']):
      restaurantid=restr.get_restrantid_with_boss(session['business_id'])
    else:
      restaurantid=None
    if restaurantid :
        sum_money = restr.get_sale_money_with_restrantid(restaurantid)
        if sum_money ==None:
            sum_money=0
        sum_orders= restr.get_sum_orders_with_restrantid(restaurantid)
        average_score=restr.get_average_score_with_restrantid(restaurantid)
        if average_score ==None:
            average_score=0
    else:
        sum_money=0
        sum_orders=0
        average_score=0

    return  render_template('business.html', restaurantid=restaurantid,
                            sum_money=sum_money,sum_orders=sum_orders,average_score=average_score)

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



@app.route('/restrant_manange')
def restaurant_manange():
    restrants = restr.get_restrant_with_boss(session['business_id'])
    return render_template('operate_restrant.html', restrantdata=restrants)

@app.route('/delete_restrant', methods=['POST'])
def delete_restrant():
    restrantid=request.form.get('restaurant_id')
    Db.delete_dish(restrantid)
    Db.delete_restrant(restrantid)
    return redirect(url_for('restaurant_manange'))

@app.route('/add_restrant', methods=['POST'])
def add_restrant():
    name = request.form.get('name')
    address = request.form.get('address')
    area = request.form.get('area')
    price = request.form.get('price')
    hours = request.form.get('hours')
    category = request.form.get('category')
    Db.add_restrant(name, address, area, price, hours, category, session['business_id'])
    return redirect(url_for('restaurant_manange'))

@app.route('/update_restaurant', methods=['POST'])
def update_restrant():
    restaurant_id=request.form.get('restaurant_id')
    name = request.form.get('name')
    address = request.form.get('address')
    area=request.form.get('area')
    price=request.form.get('price')
    hours=request.form.get('hours')
    category=request.form.get('category')
    restr.update_restrant(restaurant_id,name,address,area,price,hours,category,session['business_id'])
    return redirect(url_for('restaurant_manange'))



@app.route('/operate_dishes', methods=['GET', 'POST'])
def operate_dishes():
    restaurant_id = request.args.get('restrantid')  # 从URL获取
    # GET请求处理
    if restaurant_id:
        dishes = Db.get_dishs(restaurant_id)
    else:
        dishes = []
        print("未提供餐厅ID")
    return render_template('operate_dishes.html',
                           dishes=dishes,
                           restaurant_id=restaurant_id)


@app.route('/add_dish', methods=['POST'])
def add_dish():
    name = request.form.get('name')
    price=request.form.get('price')
    description=request.form.get('description')
    is_featured = 1 if 'is_featured' in request.form else 0
    restaurant_id=request.form.get('restaurant_id')
    restr.add_dish(name, price, description, is_featured, restaurant_id)
    return redirect(url_for('operate_dishes',restrantid=restaurant_id))


@app.route('/update_dish', methods=['POST'])
def update_dish():
    dish_id = request.form.get('dish_id')
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description', '')
    is_featured = 1 if 'is_featured' in request.form else 0
    restaurant_id = request.form.get('restaurant_id')
    restr.update_dish(dish_id, name, price, description, is_featured,restaurant_id)
    return redirect(url_for('operate_dishes',restrantid=restaurant_id))


@app.route('/delete_dish', methods=['POST'])
def delete_dish():
    dish_id = request.form.get('dish_id')
    restaurant_id = request.form.get('restaurant_id')
    restr.delete_dish(dish_id)
    return redirect(url_for('operate_dishes',restrantid=restaurant_id))


@app.route('/restrant_order')
def restrant_order():
    restrants = restr.get_restrant_with_boss(session['business_id'])
    if restrants:
      orders = Db.get_orders_with_restrantid(restrants[0][0])
      hot_dishes=restr.restrant_hot_dish(restrants[0][0])
      high_dishes=restr.restrant_high_dishe(restrants[0][0])
      if len(hot_dishes)!=0:
          dishes=[]
          for dish in hot_dishes:
              name=restr.dishname(dish[0])
              num=dish[1]
              dishes.append([name,num])
      else:
          dishes=[]

      if len(high_dishes)!=0:
          highscores=[]
          for dish in high_dishes:
              name=restr.dishname(dish[0])
              num=dish[1]
              highscores.append([name,num])
      else:
          highscores=[]
      sum_money = restr.get_sale_money_with_restrantid(restrants[0][0])
      if sum_money == None:
         sum_money = 0
      sum_orders = restr.get_sum_orders_with_restrantid(restrants[0][0])


    else:
     orders = []
     sum_money=0
     sum_orders=0
     dishes = []
     highscores=[]

    return render_template('myorder2.html', orders=orders,sum_money=sum_money,
                           sum_orders=sum_orders,dishes=dishes,highscores=highscores)






























if __name__ == '__main__':
    app.run(debug=True, port=5000)




