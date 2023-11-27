#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 11:56:02 2023

@author: vinmathi
"""
# pip install pandasql
import pandas as pd
import pandasql as psql
#-----------------------------------------------------------------------------------
# Replace 'your_file.csv' with the actual file path of your CSV data.
file_path = 'Medicare_Part_D.csv'

# The first 50 records will be read.
first_50_records = pd.read_csv(file_path, nrows=500)

# Display the first 50 records.
print(first_50_records)

#
print(first_50_records['Tot_Clms'].head(50))
#-----------------------------------------------------------------------------------
# Write the SQL query to fetch the total number of drugs prescribed by the specific NPI
query = """
SELECT 
     Prscrbr_NPI, 
     sum(tot_Clms) as Total_Drugs_Prescribed , 
     sum(Tot_Drug_Cst) as Total_drug_cost
FROM 
    first_50_records
WHERE 
    Prscrbr_NPI = '1003000126'
GROUP BY 
    Prscrbr_NPI
"""

# Execute the SQL query
result = psql.sqldf(query)

# Print the result
print(result)
#-----------------------------------------------------------------------------------
#find the distint npi - i have 20 NPI , 241 UNIQUE DRUGS , 15 states
query2 = """
SELECT distinct Prscrbr_State_Abrvtn
FROM first_50_records"""

# Execute the SQL query
result = psql.sqldf(query2)

# Print the result
print(result)

#-----------------------------------------------------------------------------------
#top 5 drug commonly prescribed drugs
query3 = """
SELECT  
     Brnd_name , 
     sum(tot_Clms) as Total_claims ,
     sum(Tot_Drug_Cst) as Total_drug_cost
FROM 
     first_50_records
GROUP BY 
     Brnd_name
ORDER BY 
     Total_claims desc
LIMIT 5
"""

# Execute the SQL query
result = psql.sqldf(query3)

# Print the result
print(result)
#------------------------------------------------------------------------------------
#Most common drugs prescribed in each state - one drug for each state 

query4 = """
SELECT  
     Brnd_name , 
     Prscrbr_State_Abrvtn as state , 
     sum(tot_Clms) as Total_claims
FROM 
     first_50_records
GROUP BY 
     Prscrbr_State_Abrvtn 
ORDER BY 
     Total_claims desc

"""

# Execute the SQL query
result = psql.sqldf(query4)

# Print the result
print(result)

#-----------------------------------------------------------------------------------
#drug that is very expensive 

query5 = """
SELECT  
     Brnd_name , 
     sum(Tot_Drug_Cst) as Total_drug_cost ,
     sum(tot_Clms) as Total_claims , 
     sum(tot_Drug_Cst/tot_Clms) as drug_cost
FROM first_50_records
GROUP BY Brnd_name 
ORDER BY drug_cost desc
LIMIT 10
"""

# Execute the SQL query
result = psql.sqldf(query5)

# Print the result
print(result)

#checking
query5 = """
select tot_Drug_Cst ,tot_Clms from first_50_records
where Brnd_name    == 'Humalog Kwikpen U-200'
"""

#----------------------------------------------------------------------------------
#IS DRUGS EXPENSIVE IN CA ? LOOKS LIKE DRUGS ARE EXPENSIVE IN CA WHEN COMPARED TO OH


query6 = """
SELECT 
    CA.Brnd_name, 
    CA.Tot_Drug_Cst / CA.tot_Clms AS CA_cost,
    OH.Tot_Drug_Cst / OH.tot_Clms AS OH_cost,
    CA.Tot_Drug_Cst / CA.tot_Clms -  OH.Tot_Drug_Cst / OH.tot_Clms AS Difference
FROM 
    (SELECT Brnd_name, Tot_Drug_Cst, tot_Clms
     FROM first_50_records
     WHERE Prscrbr_State_Abrvtn = 'CA') AS CA
INNER JOIN
    (SELECT Brnd_name, Tot_Drug_Cst ,tot_Clms
     FROM first_50_records
     WHERE Prscrbr_State_Abrvtn = 'OH') AS OH
ON CA.Brnd_name = OH.Brnd_name
"""

# Execute the SQL query
result = psql.sqldf(query6)

# Print the result
print(result)

#--------------------------------------------------------------------------------------
#prescriber with highest claims

query7 = """
SELECT  
     Prscrbr_NPI , 
     sum(tot_Clms) as tot_Clms , 
     Prscrbr_First_Name, 
     Prscrbr_State_Abrvtn as state
FROM 
     first_50_records
GROUP BY 
     Prscrbr_NPI 
ORDER BY 
     tot_Clms desc
LIMIT 10
"""

# Execute the SQL query
result = psql.sqldf(query7)

# Print the result
print(result)















