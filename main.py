import os
import duckdb


def main():

    os.makedirs('output', exist_ok=True)

    con = duckdb.connect()

    # TABLAS RELEVANTES
    con.execute("""
                CREATE TABLE IF NOT EXISTS employees AS
                SELECT
                *
                FROM read_csv_auto('data/rrhh_employees.csv');
                """)

    con.execute("""
                CREATE TABLE IF NOT EXISTS departments AS
                SELECT
                *
                FROM read_csv_auto('data/rrhh_departments.csv');
                """)

    con.execute("""
                CREATE TABLE IF NOT EXISTS salaries AS
                SELECT
                *
                FROM read_csv_auto('data/rrhh_salaries.csv');
                """)


    # INNER JOIN para obtener unicamente los empleados que tienen departamento.

    inner_join_employees_departments = con.execute("""
                                                SELECT
                                                CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
                                                d.department_name
                                                FROM employees e
                                                INNER JOIN departments d
                                                ON e.department_id = d.department_id;
                                                """).fetchdf()

    # con el len() de la siguiente consulta podemos validar que pre y post join el numero de empleados es 500
    #  por lo que todos los empleados tienen departamento.
    # employees = con.execute("""
    #                         SELECT *
    #                         FROM employees
    #                         """).fetchdf()
    # print(len(inner_join_employees_departments))
    # print("-------------------")
    # print(len(employees))


    # LEFT JOIN. En terminos de resultado, para este caso podemos quedarnos con el INNER JOIN.
    # Pero para validacion de integridad referencial (un id que referencia a otra tabla debe existir en dicha tabla),
    # puede ser buena idea usarlo, ya que con el INNER JOIN eliminamos de forma silenciosa
    # a potenciales empleados con departamento invalido o inexistente.

    left_join_employees_departments = con.execute("""
                                                SELECT
                                                e.employee_id,
                                                CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
                                                d.department_name
                                                FROM employees e
                                                LEFT JOIN departments d
                                                ON e.department_id = d.department_id;
    """).fetchdf()

    print(left_join_employees_departments)

    # Se suele usar LEFT JOIN ya que es el estandar por legibilidad, pero se puede obtener lo mismo con RIGHT JOIN. Solo hay que intercambiar lugares entre tabla employees y departments.
    # Si agregamos al final WHERE d.department_name IS NULL, podemos saber cuales son los empleados sin departamento.


    # SELF JOIN para obtener empleados y sus managers

    self_join_employees_with_managers = con.execute("""
                                    SELECT
                                    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
                                    CONCAT(m.first_name, ' ', m.last_name) AS manager_name
                                    FROM employees e
                                    LEFT JOIN employees m
                                    ON e.manager_id = m.employee_id;
    """).fetchdf()

    # Clausula WHERE para detectar aquellos sin manager (generalmente top level, CEOs)
    self_join_employees_without_managers = con.execute("""
                                            SELECT
                                            CONCAT(e.first_name, ' ', e.last_name) AS employee_name
                                            FROM employees e
                                            LEFT JOIN employees m
                                            ON e.manager_id = m.employee_id
                                            WHERE m.employee_id IS NULL;                            
    """).fetchdf()


    # JOIN de 3 tablas (employees, departments, salaries) para obtener el salario mas reciente de cada empleado.

    employees_departments_latest_salaries = con.execute("""
                                            WITH ranked_salaries AS (
                                            SELECT
                                            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
                                            d.department_name,
                                            s.base_salary,
                                            s.effective_date AS salary_date,
                                            ROW_NUMBER() OVER(PARTITION BY e.employee_id ORDER BY s.effective_date DESC) AS salary_ranking
                                            FROM employees e
                                            INNER JOIN departments d
                                            ON e.department_id = d.department_id
                                            INNER JOIN salaries s
                                            ON e.employee_id = s.employee_id
                                            )
                                            SELECT
                                            employee_name,
                                            department_name,
                                            base_salary,
                                            salary_date
                                            FROM ranked_salaries
                                            WHERE salary_ranking = 1;
    """).fetchdf()


    # Load de output en .csv

    inner_join_employees_departments.to_csv('output/employees_and_departments.csv', index=False)
    self_join_employees_with_managers.to_csv('output/employees_with_managers.csv', index=False)
    self_join_employees_without_managers.to_csv('output/employees_without_managers.csv', index=False)
    employees_departments_latest_salaries.to_csv('output/employees_departments_latest_salaries.csv', index=False)

    print('Carga exitosa en .csv!')
    # Load de output en parquet

    inner_join_employees_departments.to_parquet('output/employees_and_departments.parquet', index=False)
    self_join_employees_with_managers.to_parquet('output/employees_with_managers.parquet', index=False)
    self_join_employees_without_managers.to_parquet('output/employees_without_managers.parquet', index=False)
    employees_departments_latest_salaries.to_parquet('output/employees_departments_latest_salaries.parquet', index=False)

    print('Carga exitosa en parquet!')


    con.close()


if __name__ == "__main__":
    main()