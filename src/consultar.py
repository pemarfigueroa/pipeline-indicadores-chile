import duckdb
import pyarrow

from pathlib import Path

indicador = "uf"
year = 2026

raiz = Path(__file__).resolve().parent.parent

archivo_silver = (raiz / "data" / "gold"
                  / "indicadores.duckdb"
                  ).as_posix()

conn = duckdb.connect(archivo_silver, read_only=True)
# consulta = f"SELECT * FROM read_parquet('{archivo_silver}', hive_partitioning=True)  LIMIT 10"
consulta = "SELECT * FROM uf_en_dolares LIMIT 10"

conn.sql(consulta).show()
conn.close()
