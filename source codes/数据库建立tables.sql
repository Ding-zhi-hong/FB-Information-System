-- 创建数据库
CREATE DATABASE IF NOT EXISTS FB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

DELIMITER //

CREATE TRIGGER AVGMONEY
AFTER INSERT ON 订单记录
FOR EACH ROW
BEGIN
    DECLARE avg_per_user DECIMAL(10,2);
    
    -- 计算每个用户在该餐厅的平均消费（每人总消费平均值）
    SELECT AVG(user_total) INTO avg_per_user
    FROM (
        SELECT 
            用户ID,
            SUM(CAST(消费Money AS DECIMAL(10,2))) AS user_total
        FROM 订单记录
        WHERE 餐厅ID = NEW.餐厅ID
        GROUP BY 用户ID
    ) AS user_totals;
    
    -- 更新餐厅表的人均消费（使用隐式转换而非CAST）
    UPDATE 餐厅
    SET 人均消费 = 
        CASE 
            WHEN avg_per_user IS NULL THEN '0' 
            ELSE FORMAT(avg_per_user, 2) 
        END
    WHERE 餐厅ID = NEW.餐厅ID;
END//

DELIMITER ;












USE FB;
#DROP DATABASE FB;
-- 员工表
CREATE TABLE IF NOT EXISTS 员工 (
    pno VARCHAR(255),
    姓名 VARCHAR(255),
    职位 VARCHAR(255),
    联系方式 VARCHAR(255),
		餐厅ID INT ,
		PRIMARY KEY (pno)
);

-- 评价表
CREATE TABLE IF NOT EXISTS 评价 (
    评价ID INT NOT NULL AUTO_INCREMENT,
    用户ID INT,
    餐厅ID INT,
		菜品ID INT,
    评分 VARCHAR(255),
    评论内容 VARCHAR(255),
		PRIMARY KEY (评价ID)
);




-- 用户表
CREATE TABLE IF NOT EXISTS 用户 (
    用户PID INT NOT NULL AUTO_INCREMENT,
    用户名 VARCHAR(255),
    密码 VARCHAR(255),
    联系方式 VARCHAR(255),
		PRIMARY KEY (用户PID)
);




-- 区域表
CREATE TABLE IF NOT EXISTS 区域表 (
    区域ID INT NOT NULL AUTO_INCREMENT,
    区域名称 VARCHAR(255),
    上级区域ID INT,
    是否热门区域 VARCHAR(255),
		PRIMARY KEY (区域ID)
		
);


INSERT INTO 区域表(区域名称,上级区域ID,是否热门区域)
VALUES('北京',1,'是');







-- 餐厅表
CREATE TABLE IF NOT EXISTS 餐厅 (
    餐厅ID INT NOT NULL AUTO_INCREMENT,
    名称 VARCHAR(255),
    地址 VARCHAR(255),
    区域ID INT,
    人均消费 VARCHAR(255),
    营业时间 VARCHAR(255),
    类别id INT,
    FOREIGN KEY (区域ID) REFERENCES 区域表(区域ID),
		PRIMARY KEY (餐厅ID)
);



CREATE TABLE IF NOT EXISTS 类别 (
    类别id INT NOT NULL AUTO_INCREMENT,
    类别名 VARCHAR(255),
		PRIMARY KEY (类别id)
);

INSERT INTO 类别(`类别名`)
VALUES('西餐');


-- 特色标签表
CREATE TABLE IF NOT EXISTS 特色标签 (
    标签ID INT NOT NULL AUTO_INCREMENT,
    标签名 VARCHAR(255),
		PRIMARY KEY (标签ID)
);

INSERT INTO 特色标签(标签名)
VALUES('海鲜');


-- 订单记录表
CREATE TABLE IF NOT EXISTS 订单记录 (
    订单ID INT NOT NULL AUTO_INCREMENT,
    用户ID INT,
    餐厅ID INT,
    菜品ID INT,
    消费Money VARCHAR(255),
    下单时间 VARCHAR(255),
    #FOREIGN KEY (用户ID) REFERENCES 用户(用户PID),
    #FOREIGN KEY (餐厅ID) REFERENCES 餐厅(餐厅ID),
		PRIMARY KEY (订单ID)
);



-- 菜品表
CREATE TABLE IF NOT EXISTS 菜品 (
    菜品ID INT NOT NULL AUTO_INCREMENT,
    名称 VARCHAR(255),
    价格 VARCHAR(255),
    描述 VARCHAR(255),
    是否特色菜 VARCHAR(255),
		PRIMARY KEY (菜品ID)
);

-- 商家表
CREATE TABLE IF NOT EXISTS 商家 (
    商家id INT NOT NULL AUTO_INCREMENT,
    联系电话 VARCHAR(255),
    商家名 VARCHAR(255),
    密码 VARCHAR(255),
		PRIMARY KEY (商家id)
);



-- 添加外键关系 (图片中未明确但逻辑需要的关联)
###ALTER TABLE 评价
#ADD FOREIGN KEY (用户ID) REFERENCES 用户(用户PID),
#ADD FOREIGN KEY (餐厅ID) REFERENCES 餐厅(餐厅ID);





ALTER TABLE 餐厅
ADD COLUMN 商家id INT;
#ADD FOREIGN KEY (商家id) REFERENCES 商家(商家id);


ALTER TABLE 菜品
ADD COLUMN 餐厅ID INT;
#ADD FOREIGN KEY (餐厅ID) REFERENCES 餐厅(餐厅ID);

ALTER TABLE 评价
ADD COLUMN 订单ID INT;

ALTER TABLE `员工`
CHANGE COLUMN 餐厅ID 商家ID INT;







