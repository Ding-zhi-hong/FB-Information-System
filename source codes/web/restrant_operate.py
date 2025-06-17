from db import create_connection



def get_restrantid_with_boss(id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT 餐厅ID FROM 餐厅 WHERE 商家ID = %s"
    cursor.execute(query, (id,))
    sum = cursor.fetchone()
    cursor.close()
    connection.close()
    if sum:
        return sum[0]
    else:
        return sum



def get_sale_money_with_restrantid(id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT SUM(消费Money) FROM 订单记录 WHERE 餐厅ID = %s"
    cursor.execute(query, (id,))
    sum = cursor.fetchone()
    cursor.close()
    connection.close()
    return sum[0]


def get_sum_orders_with_restrantid(id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(订单ID) FROM 订单记录 WHERE 餐厅ID = %s"
    cursor.execute(query, (id,))
    sum = cursor.fetchone()
    cursor.close()
    connection.close()
    return sum[0]



def get_average_score_with_restrantid(id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT AVG(评分) FROM 评价 WHERE 餐厅ID = %s"
    cursor.execute(query, (id,))
    sum = cursor.fetchone()
    cursor.close()
    connection.close()
    return sum[0]



def get_restrant_with_boss(id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM 餐厅 WHERE 商家ID = %s"
    cursor.execute(query, (id,))
    sum = cursor.fetchall()
    cursor.close()
    connection.close()
    return sum

def update_restrant(restaurant_id,name,address,area,price,hours,category,business_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "UPDATE 餐厅 SET 名称= %s,地址=%s,区域ID=%s,人均消费=%s,营业时间=%s,类别id=%s,商家id=%s WHERE 餐厅ID = %s"
    cursor.execute(query,(name,address,area,price,hours,category,business_id,restaurant_id))
    connection.commit()
    cursor.close()
    connection.close()


def add_dish(name, price, description, is_featured, restaurant_id):
    connection = create_connection()
    cursor = connection.cursor()
    query="INSERT INTO 菜品(名称,价格,描述,是否特色菜,餐厅ID) VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(query,(name,price,description,is_featured,restaurant_id))
    connection.commit()
    cursor.close()
    connection.close()

def delete_dish(dish_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "DELETE FROM 菜品 WHERE 菜品ID = %s"
    cursor.execute(query, (dish_id))
    connection.commit()
    cursor.close()
    connection.close()

def update_dish(dish_id, name, price, description, is_featured,restaurant_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "UPDATE 菜品 SET 名称=%s,价格=%s,描述=%s,是否特色菜= %s,餐厅ID= %s WHERE 菜品ID = %s"
    cursor.execute(query, ( name, price, description, is_featured,restaurant_id,dish_id))
    connection.commit()
    cursor.close()
    connection.close()

def restrant_hot_dish(restaurant_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT 菜品ID, COUNT(*) FROM 订单记录 WHERE 餐厅ID = %s GROUP BY 菜品ID ORDER BY COUNT(*) DESC "
    cursor.execute(query, (restaurant_id,))
    sum = cursor.fetchall()
    cursor.close()
    connection.close()
    return sum

def restrant_high_dishe(restaurant_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT 菜品ID, AVG(评分) FROM 评价 WHERE 餐厅ID = %s GROUP BY 菜品ID ORDER BY AVG(评分) DESC "
    cursor.execute(query, (restaurant_id,))
    sum = cursor.fetchall()
    cursor.close()
    connection.close()
    return sum


def dishname(id):
    connection = create_connection()
    cursor = connection.cursor()
    query="SELECT 名称 FROM 菜品 WHERE 菜品ID=%s"
    cursor.execute(query,(id,))
    sum = cursor.fetchone()
    cursor.close()
    connection.close()
    return sum[0]