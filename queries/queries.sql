-- Query data from the World Bank database.
USE worldbank;


SHOW VARIABLES LIKE "secure_file_priv";

-- What tables are available inside of the worldbank database?
SHOW TABLES;
 
 
-- What are the column names in the `contracts` table?
SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'contracts'
ORDER BY ORDINAL_POSITION;


-- What does the table look like? Show the first 5 rows of the table
SELECT *
FROM contracts
LIMIT 5;


-- How many records are in the `contracts` table?
SELECT
	COUNT(*) AS total_records
FROM contracts;


-- How many contracts have been approved by the World Bank?
 SELECT COUNT(DISTINCT ProjectID) AS unique_ids
 FROM contracts;
 
 
 -- What day was the first contract approved by the World Bank?
 SELECT MIN(ContractSigningDate)
 FROM contracts;
 
 
 -- What is the date of the most recent contract approved by the World Bank
 SELECT MAX(ContractSigningDate)
 FROM contracts;


 -- How many contracts were approved by the World Bank by FiscalYear?
 SELECT FiscalYear, COUNT(DISTINCT ProjectID) AS Number_of_Contracts_Approved 
 FROM contracts
 GROUP BY FiscalYear;
 
 
 -- Which region has received the most contracts?
 SELECT Region, COUNT(DISTINCT ProjectID) AS Number_of_Contracts_Approved
 FROM contracts
 GROUP BY Region;
 
 
 -- Which region has recieved the most funding from the World Bank?
 SELECT Region, SUM(`TotalContractAmount(USD)`) AS TotalFunding
 FROM contracts
 GROUP BY Region
 ORDER BY TotalFunding DESC
 LIMIT 1;
 
 
 -- What are the top 10 countries by the number of contracts supplied and total funding supplied?
 SELECT SupplierCountry,
	COUNT(DISTINCT WBContractNumber) AS TotalContractsSupplied,
    SUM(`TotalContractAmount(USD)`) AS TotalFundsSupplied
 FROM contracts
 GROUP BY SupplierCountry
 ORDER BY TotalContractsSupplied DESC, TotalFundsSupplied DESC
 LIMIT 10;
 
 
 -- What are the top 10 countries recieving the most contracts and funding from suppliers?
 SELECT BorrowerCountry,
	COUNT(DISTINCT WBContractNumber) AS TotalBorrowingContracts,
    SUM(`TotalContractAmount(USD)`) AS TotalAmountBorrowed
FROM contracts
GROUP BY BorrowerCountry
ORDER BY TotalBorrowingContracts DESC
LIMIT 10;


-- Which countries have a "Positive Net Credit" from the World Bank?
WITH lender AS (
 SELECT SupplierCountry,
	COUNT(DISTINCT WBContractNumber) AS TotalContractsSupplied,
    SUM(`TotalContractAmount(USD)`) AS TotalFundsSupplied
 FROM contracts
 GROUP BY SupplierCountry
 ORDER BY TotalContractsSupplied DESC, TotalFundsSupplied DESC
 ),
 borrower AS (
  SELECT BorrowerCountry,
	COUNT(DISTINCT WBContractNumber) AS TotalBorrowingContracts,
    SUM(`TotalContractAmount(USD)`) AS TotalAmountBorrowed
FROM contracts
GROUP BY BorrowerCountry
ORDER BY TotalBorrowingContracts DESC
 )
SELECT lender.SupplierCountry AS Country,
	lender.TotalFundsSupplied - borrower.TotalAmountBorrowed AS CreditAmount
FROM lender
JOIN borrower ON lender.SupplierCountry = borrower.BorrowerCountry
WHERE lender.TotalFundsSupplied - borrower.TotalAmountBorrowed > 0
ORDER BY CreditAmount DESC;


-- What countries have a "Negative Net Credit" from the World Bank?
WITH lender AS (
 SELECT SupplierCountry,
	COUNT(DISTINCT WBContractNumber) AS TotalContractsSupplied,
    SUM(`TotalContractAmount(USD)`) AS TotalFundsSupplied
 FROM contracts
 GROUP BY SupplierCountry
 ORDER BY TotalContractsSupplied DESC, TotalFundsSupplied DESC
 ),
 borrower AS (
  SELECT BorrowerCountry,
	COUNT(DISTINCT WBContractNumber) AS TotalBorrowingContracts,
    SUM(`TotalContractAmount(USD)`) AS TotalAmountBorrowed
FROM contracts
GROUP BY BorrowerCountry
ORDER BY TotalBorrowingContracts DESC
 )
SELECT lender.SupplierCountry AS Country,
	lender.TotalFundsSupplied - borrower.TotalAmountBorrowed AS CreditAmount
FROM lender
JOIN borrower ON lender.SupplierCountry = borrower.BorrowerCountry
WHERE lender.TotalFundsSupplied - borrower.TotalAmountBorrowed < 0
ORDER BY CreditAmount;


-- What are the top 5 sectors of the economy China helps support other countries through funding?
SELECT MajorSector,
	SUM(`TotalContractAmount(USD)`) AS TotalFunding
FROM contracts
WHERE SupplierCountry = 'China'
GROUP BY MajorSector
ORDER BY TotalFunding DESC
LIMIT 5;
 
 
 -- Which countries receive Transportation Funding from China? Calculate the dollar amount provided.
SELECT BorrowerCountry,
	SupplierCountry,
	SUM(`TotalContractAmount(USD)`) AS TotalFunding
FROM contracts
WHERE SupplierCountry = 'China'
	AND MajorSector = 'Transportation';
 -- Does China Lend to itself?
 
 