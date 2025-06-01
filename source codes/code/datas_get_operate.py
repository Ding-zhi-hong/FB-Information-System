from db import create_connection

#用户操作
def register_user(username, password,phone_number):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO 用户 (用户名, 密码,联系方式) VALUES (%s, %s,%s)"
    cursor.execute(query, (username, password, phone_number))
    connection.commit()
    cursor.close()
    connection.close()


def login_user(username, password):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT 用户PID FROM 用户 WHERE 用户名 = %s AND 密码 = %s"
    cursor.execute(query, (username, password))
    user_id = cursor.fetchone()
    cursor.close()
    connection.close()
    return user_id[0]



#员工操作
def get_employees():
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM 员工"
    cursor.execute(query)
    staffs = cursor.fetchall()
    cursor.close()
    connection.close()
    return staffs

def get_area_with_pno(pno):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM 员工 WHERE pno = %d"
    cursor.execute(query, (pno,))
    employees = cursor.fetchone()
    cursor.close()
    connection.close()
    return employees

def add_employee(pno,name,job,phone_number):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO 员工 (pno,姓名,职位,联系方式) VALUES (%d,%s, %s,%s)"
    cursor.execute(query, (pno,name,job,phone_number))
    connection.commit()
    cursor.close()
    connection.close()

def delete_employee(pno):
    connection = create_connection()
    cursor = connection.cursor()
    query="DELETE FROM 员工 WHERE pno=%s"
    cursor.execute(query,(pno,))
    connection.commit()
    cursor.close()
    connection.close()


#特色标签
def get_label():
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM 特色标签"
    cursor.execute(query)
    labels = cursor.fetchall()
    cursor.close()
    connection.close()
    return labels

def add_label(labelid,label):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO 特色标签 (标签ID,标签名) VALUES (%d,%s)"
    cursor.execute(query, (labelid,label))
    connection.commit()
    cursor.close()
    connection.close()

#商家信息
def register_business(id,phone_number,username, password):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO 商家 (商家id, 联系电话,商家名,密码) VALUES (%d,%s, %s,%s)"
    cursor.execute(query, (id,phone_number,username, password))
    connection.commit()
    cursor.close()
    connection.close()


def login_business(username, password):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT 商家id FROM 商家 WHERE 商家名 = %s AND 密码 = %s"
    cursor.execute(query, (username, password))
    user_id = cursor.fetchone()
    cursor.close()
    connection.close()
    return user_id[0]

#区域信息
def get_area():
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM 区域表"
    cursor.execute(query)
    areas = cursor.fetchall()
    cursor.close()
    connection.close()
    return areas


def get_area_with_ID(id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM 区域表 WHERE 区域ID = %d"
    cursor.execute(query, (id,))
    area = cursor.fetchone()
    cursor.close()
    connection.close()
    return area

def add_area(areaid,name,upperid,hot):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO 区域表 (区域ID, 区域名称,上级区域ID,是否热门区域) VALUES (%d,%s, %d,%s)"
    cursor.execute(query, (areaid,name,upperid,hot))
    connection.commit()
    cursor.close()
    connection.close()

#餐厅
def get_restrant():
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM 餐厅"
    cursor.execute(query)
    restrants = cursor.fetchall()
    cursor.close()
    connection.close()
    return restrants

def get_restrant_with_ID(id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM 餐厅 WHERE 餐厅ID = %d"
    cursor.execute(query, (id,))
    restrant = cursor.fetchone()
    cursor.close()
    connection.close()
    return restrant

def add_restrant(id,name,place,areaid,money,time,labelid,businessid):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO 餐厅 (餐厅ID, 名称,地址,区域ID,人均消费,营业时间,类别id,商家id) VALUES (%d,%s,%s, %d,%s,%s,%d,%d)"
    cursor.execute(query, (id,name,place,areaid,money,time,labelid,businessid))
    connection.commit()
    cursor.close()
    connection.close()

#菜品


'''if __name__ == '__main__':
    #register_user("丁志宏2","1234","15255160712")
    print(login_user("丁志宏2", "1234"))
    print(login_user("丁志宏2", "1234"))
'''