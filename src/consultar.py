import duckdb
import pyarrow

from pathlib import Path

indicador = "uf"
year = 2026

raiz = Path(__file__).resolve().parent.parent

archivo_silver = (raiz / "data" / "silver"
                  / "**"
                  / "*.parquet"
                  ).as_posix()


# consulta = f"SELECT * FROM read_parquet('{archivo_silver}', hive_partitioning=True)  LIMIT 10"
consulta = f"SELECT indicador, COUNT(1) FROM read_parquet('{archivo_silver}', hive_partitioning=True) GROUP BY indicador"

duckdb.sql(consulta).show()
