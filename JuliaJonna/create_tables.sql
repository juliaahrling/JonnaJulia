CREATE TABLE [User](
id int PRIMARY KEY,
email varchar(50) not null,
f_name varchar(50) not null,
[address] varchar(50) not null,
city varchar(50) not null,
country varchar(50) not null,
phone_number int,
[type] char(1) not null check ([type] in ('A','C'))
);

CREATE TABLE Supplier (
 id int PRIMARY KEY,
 [name] varchar(50) NOT NULL,
 [address] varchar(50) NOT NULL,
 phone_number int
);

CREATE TABLE Product (
 id int PRIMARY KEY,
 [name] varchar(50) NOT NULL,
 [type] varchar(50) NOT NULL,
 quantity int NOT NULL,
 price decimal(12,2) NOT NULL,
 supplier_id int NOT NULL,
 FOREIGN KEY (supplier_id) references Supplier(id)
);

CREATE TABLE Supplied_by (
product_id int,
supplier_id int
PRIMARY KEY (product_id,supplier_id)
);

CREATE TABLE Order_item (
 order_id int identity (100,2) PRIMARY KEY,
 product_id int NOT NULL,
 quantity int NOT NULL,
 FOREIGN KEY (product_id) references Product(id)
);
 
CREATE TABLE [Order] (
 order_id int PRIMARY KEY,
 [user_id] int NOT NULL,
 [stauts] varchar(10),
 FOREIGN KEY (order_id) references Order_item(order_id)
);

CREATE TABLE Discount (
 id int PRIMARY KEY,
 [reason] varchar(50) NOT NULL,
 [percentage] decimal,
);
 
CREATE TABLE On_Sale (
 discount_id int NOT NULL,
 product_id int NOT NULL,
 [start_date] date NOT NULL,
 end_date date not null,
 PRIMARY KEY (discount_id, product_id),
 FOREIGN KEY (discount_id) references Discount(id),
 FOREIGN KEY (product_id) references Product(id)
);