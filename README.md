# JOINS. Caso de uso.

## Escenario
HR desea tener un reporte que combina empleados, departamentos, y salarios.

## Objetivo
Optimizar y automatizar el reporte que HR realiza manualmente, mediante queries que combinan las tablas requeridas.

## Solución
El proyecto utiliza **DuckDB** como motor analitico embebido y **Python** para ejecutar queries SQL que:

- Combinan empleados y departamentos (INNER / LEFT JOIN)
- Detectan posibles problemas de integridad referencial
- Relacionan empleados con sus managers (SELF JOIN)
- Obtienen el salario más reciente por empleado (INNER JOIN, Window functions)

## Outputs
El script crea automáticamente el directorio `output/` si no existe.
Ademas, genera archivos en formato **CSV** y **Parquet** con los resultados.


## Tecnologias
- Python
- DuckDB
- Pandas
- PyArrow

## Ejecucion

```bash
pip install -r requirements.txt
python main.py
```


