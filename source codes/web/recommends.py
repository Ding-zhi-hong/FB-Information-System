from db import create_connection



def hot():
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT 餐厅ID FROM 订单记录  GROUP BY 餐厅ID ORDER BY COUNT(*) DESC "
    cursor.execute(query)
    sum = cursor.fetchall()
    cursor.close()
    connection.close()
    return sum

def high():
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT 餐厅ID FROM 评价  GROUP BY 餐厅ID ORDER BY AVG(评分) DESC "
    cursor.execute(query)
    sum = cursor.fetchall()
    cursor.close()
    connection.close()
    return sum


def history(userid):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT 餐厅ID,COUNT(*) FROM 订单记录 WHERE 用户ID=%s GROUP BY 餐厅ID ORDER BY COUNT(*) DESC "
    cursor.execute(query,(userid))
    sum = cursor.fetchall()
    cursor.close()
    connection.close()
    if sum:
      return sum
    else:
      return ()
