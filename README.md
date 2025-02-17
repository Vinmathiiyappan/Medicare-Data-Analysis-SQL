# Medicare Data Analysis - SQL

> Analyzing Medicare prescription trends, inpatient diagnostics, and healthcare costs across the United States.

## Table of Contents
* [Overview](#overview)
* [Technologies Used](#technologies-used)
* [Queries and Results](#queries-and-results)
  * [Total Medications Prescribed by State](#total-medications-prescribed-by-state)
  * [Most Prescribed Medication by State](#most-prescribed-medication-by-state)
  * [Average Inpatient and Outpatient Treatment Cost](#average-inpatient-and-outpatient-treatment-cost)
  * [Most Common Inpatient Diagnostic Conditions](#most-common-inpatient-diagnostic-conditions)
  * [Cities with Most Cases for Each Diagnostic Condition](#cities-with-most-cases-for-each-diagnostic-condition)
  * [Prescription Drug Expenditure](#prescription-drug-expenditure)
* [Challenges](#challenges)
* [Future Enhancements](#future-enhancements)
* [Contact](#contact)

## Overview
This project explores **Medicare data** to uncover trends in prescription drugs, inpatient diagnostic conditions, and healthcare costs across different states and cities in the United States. The dataset is sourced from **BigQuery’s public CMS Medicare data**.

## Technologies Used
- **SQL** (Google BigQuery)
- **Data Cleaning & Analysis**
- **Data Visualization (Optional for Enhancements)**

## Queries and Results

### Total Medications Prescribed by State
**Query:**
```sql
SELECT
  nppes_provider_state as PROVIDER_STATE,
  sum(total_claim_count) as TOTAL_MEDICATION
FROM `bigquery-public-data.cms_medicare.part_d_prescriber_2014`
GROUP BY PROVIDER_STATE
ORDER BY TOTAL_MEDICATION DESC
LIMIT 5;
```

**Top 5 States by Total Prescriptions:**
| Row | PROVIDER_STATE | Total Claim Count (Millions) | Total Drug Cost (Millions) |
|----|----------------|---------------------------|------------------------|
| 1  | CA            | 116                       | 9633                   |
| 2  | FL            | 91                        | 6970                   |
| 3  | NY            | 80                        | 7522                   |
| 4  | TX            | 76                        | 6462                   |
| 5  | PA            | 63                        | 4842                   |

### Most Prescribed Medication by State
**Query:**
```sql
SELECT
  state,
  drug_name,
  total_claim_count,
  day_supply,
  ROUND(total_cost_millions) AS total_cost_millions
FROM (
  SELECT
    generic_name AS drug_name,
    nppes_provider_state AS state,
    ROUND(SUM(total_claim_count)) AS total_claim_count,
    ROUND(SUM(total_day_supply)) AS day_supply,
    ROUND(SUM(total_drug_cost)) / 1e6 AS total_cost_millions
  FROM
    `bigquery-public-data.cms_medicare.part_d_prescriber_2014`
  GROUP BY
    state,
    drug_name) A
ORDER BY
  total_claim_count DESC
LIMIT
  5;
```

**Top 5 Most Prescribed Medications by State:**
| Row | State | Drug Name | Total Claims | Day Supply | Total Cost (Millions) |
|----|------|------------|--------------|------------|--------------------|
| 1  | CA   | Levothyroxine Sodium | 3,844,722  | 211,726,348 | 78 |
| 2  | FL   | Levothyroxine Sodium | 2,982,449  | 163,379,911 | 64 |
| 3  | TX   | Hydrocodone/Acetaminophen | 2,833,795 | 60,404,796  | 63 |
| 4  | NY   | Amlodipine Besylate  | 2,609,790  | 123,221,634 | 21 |
| 5  | PA   | Levothyroxine Sodium | 2,353,753  | 109,162,406 | 44 |

### Average Inpatient and Outpatient Treatment Cost
**Query:**
```sql
SELECT
  OP.provider_state AS State,
  ROUND(OP.average_OP_cost) AS Average_OP_Cost,
  ROUND(IP.average_IP_cost) AS Average_IP_Cost
FROM (
  SELECT
    provider_state,
    SUM(average_total_payments*outpatient_services)/SUM(outpatient_services) AS average_OP_cost
  FROM
    `bigquery-public-data.cms_medicare.outpatient_charges_2014`
  GROUP BY
    provider_state ) AS OP
INNER JOIN (
  SELECT
    provider_state,
    SUM(average_medicare_payments*total_discharges)/SUM(total_discharges) AS average_IP_cost
  FROM
    `bigquery-public-data.cms_medicare.inpatient_charges_2014`
  GROUP BY
    provider_state) AS IP
ON
    OP.provider_state = IP.provider_state
ORDER BY
  Average_IP_Cost DESC
LIMIT
  10;
```

### Most Common Inpatient Diagnostic Conditions
**Query:**
```sql
SELECT
  drg_definition AS DIAGNOSTIC_CONDITION,
  SUM(total_discharges) AS TOTAL_DISCHARGES
FROM
  `bigquery-public-data.cms_medicare.inpatient_charges_2014`
GROUP BY
  DIAGNOSTIC_CONDITION
ORDER BY
  TOTAL_DISCHARGES DESC
LIMIT 5;
```

### Prescription Drug Expenditure (Top 10 by Cost)
**Query:**
```sql
SELECT
 generic_name as drug_name,
 round(sum(total_claim_count)/1e5) as claim_count_lakhs,
 round(sum (total_drug_cost)/1e6) AS total_cost_millions
FROM
`bigquery-public-data.cms_medicare.part_d_prescriber_2014`
group by
    generic_name
order by
    total_cost_millions desc
limit 10;
```

## Challenges
- Handling large datasets with billions of records.
- Managing variations in drug names and missing provider data.
- Analyzing trends across different treatment types efficiently.

## Future Enhancements
- Incorporate **visualizations** for trends using Tableau or Matplotlib.
- Predict prescription trends using **machine learning models**.
- Compare Medicare costs over multiple years.

## Contact
📧 **Email:** [your-email@example.com](mailto:vinmathi.iyappan@gmail.com)  
🔗 **LinkedIn:** [YourLinkedInProfile](https://linkedin.com/in//vinmathi-iyappan/)  
🖥 **GitHub:** [YourGitHubProfile](https://github.com/Vinmathiiyappan)

