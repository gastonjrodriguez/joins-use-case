# JOINS. Use case.

## Scenario
HR wants a report that combines employees, departments, and salaries.

## Objective
Optimize and automate the report that HR currently generates manually by using queries that combine the necessary tables.

## Solution
The project uses **DuckDB** as an embedded analytics engine and **Python** to execute SQL queries that:

- Join employees and departments (INNER / LEFT JOIN)
- Detect potential referential integrity issues
- Link employees to their managers (SELF JOIN)
- Retrieve the most recent salary for each employee (INNER JOIN, window functions)

## Outputs
The script automatically creates the `output/` directory if it does not exist.
It also generates files in **CSV** and **Parquet** formats containing the results.

## Technologies
- Python
- DuckDB
- Pandas
- PyArrow

## Execution

```bash
pip install -r requirements.txt
python main.py
```

## Author

Gaston Rodriguez

