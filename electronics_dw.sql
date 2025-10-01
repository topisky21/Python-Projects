-- Create database
CREATE DATABASE IF NOT EXISTS ElectronicsDW;
USE ElectronicsDW;

-- =====================
-- Task 1–4: Dimension & Fact Table Design
-- =====================

-- DimDate
CREATE TABLE DimDate (
    DateID INT PRIMARY KEY,
    FullDate DATE,
    Day INT,
    Month INT,
    Quarter INT,
    Year INT
);

-- DimProduct
CREATE TABLE DimProduct (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    ProductName VARCHAR(100),
    ProductCategory VARCHAR(50),
    ProductType VARCHAR(50)
);

-- DimCustomerSegment
CREATE TABLE DimCustomerSegment (
    CustomerSegmentID INT PRIMARY KEY AUTO_INCREMENT,
    SegmentName VARCHAR(50)
);

-- FactSales
CREATE TABLE FactSales (
    SalesID INT PRIMARY KEY AUTO_INCREMENT,
    DateID INT,
    ProductID INT,
    CustomerSegmentID INT,
    StoreName VARCHAR(100),
    City VARCHAR(100),
    SalesRevenue DECIMAL(10,2),
    QuantitySold INT,
    FOREIGN KEY (DateID) REFERENCES DimDate(DateID),
    FOREIGN KEY (ProductID) REFERENCES DimProduct(ProductID),
    FOREIGN KEY (CustomerSegmentID) REFERENCES DimCustomerSegment(CustomerSegmentID)
);

-- =====================
-- Task 9–12: Load Sample Data
-- =====================

-- Insert DimDate
INSERT INTO DimDate VALUES
(20230101,'2023-01-01',1,1,1,2023),
(20230215,'2023-02-15',15,2,1,2023),
(20230410,'2023-04-10',10,4,2,2023),
(20230720,'2023-07-20',20,7,3,2023),
(20231005,'2023-10-05',5,10,4,2023),
(20240115,'2024-01-15',15,1,1,2024);

-- Insert DimProduct
INSERT INTO DimProduct(ProductName, ProductCategory, ProductType) VALUES
('iPhone 14', 'Smartphone', 'Mobile'),
('Samsung Galaxy S23', 'Smartphone', 'Mobile'),
('MacBook Pro', 'Laptop', 'Computer'),
('Sony Bravia 55"', 'Television', 'Home Entertainment'),
('Xbox Series X', 'Gaming Console', 'Entertainment');

-- Insert DimCustomerSegment
INSERT INTO DimCustomerSegment(SegmentName) VALUES
('Retail'),
('Wholesale'),
('Online');

-- Insert FactSales
INSERT INTO FactSales(DateID, ProductID, CustomerSegmentID, StoreName, City, SalesRevenue, QuantitySold) VALUES
(20230101, 1, 1, 'BestBuy NYC', 'New York', 1200.00, 2),
(20230215, 2, 3, 'Amazon', 'Los Angeles', 800.00, 1),
(20230410, 3, 2, 'BestBuy Chicago', 'Chicago', 2500.00, 1),
(20230720, 4, 1, 'Walmart Dallas', 'Dallas', 1500.00, 3),
(20231005, 5, 3, 'Target Miami', 'Miami', 500.00, 1),
(20240115, 1, 1, 'BestBuy NYC', 'New York', 600.00, 1);

-- =====================
-- Task 13: Grouping Sets
-- =====================
SELECT City, Year, SUM(SalesRevenue) AS TotalRevenue
FROM FactSales f
JOIN DimDate d ON f.DateID = d.DateID
GROUP BY GROUPING SETS ((City, Year), (City), (Year));

-- =====================
-- Task 14: Rollup
-- =====================
SELECT City, Year, SUM(SalesRevenue) AS TotalRevenue
FROM FactSales f
JOIN DimDate d ON f.DateID = d.DateID
GROUP BY ROLLUP (Year, City);

-- =====================
-- Task 15: Cube Query
-- (Simulated using GROUP BY with ROLLUP in MySQL)
SELECT Year, City, ProductID, AVG(SalesRevenue) AS AvgRevenue
FROM FactSales f
JOIN DimDate d ON f.DateID = d.DateID
GROUP BY Year, City, ProductID WITH ROLLUP;

-- =====================
-- Task 16: Materialized View Simulation
-- (MySQL does not support true materialized views, so we use a table)
CREATE TABLE Max_Sales AS
SELECT City, f.ProductID, p.ProductType, MAX(SalesRevenue) AS MaxSales
FROM FactSales f
JOIN DimProduct p ON f.ProductID = p.ProductID
GROUP BY City, f.ProductID, p.ProductType;
