
import datas_get_operate as datas
import datetime

import recommends
import restrant_operate as restr
order_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(restr.dishname(1))
print(recommends.hot())
print(recommends.high())
print(recommends.history(1))
print(recommends.history(2))
print(datas.get_score_with_orderid(1))