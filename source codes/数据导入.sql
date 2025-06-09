


INSERT INTO 员工(pno,姓名,职位,联系方式,`餐厅ID`)
VALUES('0001','丁志宏','厨师','15922465921',1);




INSERT INTO 用户(用户名,联系方式,密码)
VALUES('丁志宏','15922465921','dzh1234');

INSERT INTO 区域表(区域名称,上级区域ID,是否热门区域)
VALUES('中科大',1,'是');



INSERT INTO 餐厅(名称,地址,区域ID,人均消费,营业时间,类别id)
VALUES('美食广场','东区活动中心',1,'200','8:00-19:00',1);
INSERT INTO 餐厅(名称,地址,区域ID,人均消费,营业时间,类别id)
VALUES('小高米线','东区活动中心',1,'200','8:00-19:00',1);
INSERT INTO 餐厅(名称,地址,区域ID,人均消费,营业时间,类别id)
VALUES('小马烧烤','东区活动中心',1,'200','8:00-19:00',1);


INSERT INTO 评价(`用户ID`,`餐厅ID`,评分,`评论内容`,`菜品ID`)
VALUES(1,1,'3','菜很好吃就是有点辣',1);

INSERT INTO 类别(类别名)
VALUES ('早餐店');

INSERT INTO 订单记录(用户ID,餐厅ID,菜品ID,消费Money,下单时间)
VALUES (1,1,1,'15','8:00');



INSERT INTO 菜品(名称,价格,描述,是否特色菜,餐厅ID)
VALUES ('京酱肉丝','15','好吃','否',1);


INSERT INTO 商家(联系电话,商家名,密码)
VALUES('15922465921','USTC','USTC1234');

UPDATE 餐厅
SET 商家id=1
WHERE 餐厅ID=1;




