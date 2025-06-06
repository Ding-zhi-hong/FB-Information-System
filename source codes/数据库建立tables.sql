-- 创建数据库
CREATE DATABASE IF NOT EXISTS FB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE FB;

-- 员工表
CREATE TABLE IF NOT EXISTS 员工 (
    pno VARCHAR(255),
    姓名 VARCHAR(255),
    职位 VARCHAR(255),
    联系方式 VARCHAR(255)
);

-- 评价表
CREATE TABLE IF NOT EXISTS 评价 (
    评价ID INT,
    用户ID INT,
    餐厅ID INT,
    评分 VARCHAR(255),
    评论内容 VARCHAR(255)
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
    区域ID INT PRIMARY KEY,
    区域名称 VARCHAR(255),
    上级区域ID INT,
    是否热门区域 VARCHAR(255)
);

-- 餐厅表
CREATE TABLE IF NOT EXISTS 餐厅 (
    餐厅ID INT PRIMARY KEY,
    名称 VARCHAR(255),
    地址 VARCHAR(255),
    区域ID INT,
    人均消费 VARCHAR(255),
    营业时间 VARCHAR(255),
    类别id INT,
    FOREIGN KEY (区域ID) REFERENCES 区域表(区域ID)
);

-- 特色标签表
CREATE TABLE IF NOT EXISTS 特色标签 (
    标签ID INT PRIMARY KEY,
    标签名 VARCHAR(255)
);

-- 订单记录表
CREATE TABLE IF NOT EXISTS 订单记录 (
    用户ID INT,
    餐厅ID INT,
    菜品ID INT,
    消费Money VARCHAR(255),
    下单时间 VARCHAR(255),
    FOREIGN KEY (用户ID) REFERENCES 用户(用户PID),
    FOREIGN KEY (餐厅ID) REFERENCES 餐厅(餐厅ID)
);

-- 菜品表
CREATE TABLE IF NOT EXISTS 菜品 (
    菜品ID INT PRIMARY KEY,
    名称 VARCHAR(255),
    价格 VARCHAR(255),
    描述 VARCHAR(255),
    是否特色菜 VARCHAR(255)
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
ALTER TABLE 评价
ADD FOREIGN KEY (用户ID) REFERENCES 用户(用户PID),
ADD FOREIGN KEY (餐厅ID) REFERENCES 餐厅(餐厅ID);

ALTER TABLE 餐厅
ADD COLUMN 商家id INT,
ADD FOREIGN KEY (商家id) REFERENCES 商家(商家id);

ALTER TABLE 菜品
ADD COLUMN 餐厅ID INT,
ADD FOREIGN KEY (餐厅ID) REFERENCES 餐厅(餐厅ID);