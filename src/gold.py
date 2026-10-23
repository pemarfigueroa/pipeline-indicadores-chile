import duckdb
import json

import pandas as pd

from pathlib import Path


indicador = "uf"
year = 2026

raiz = Path(__file__).resolve().parent.parent

archivo_silver = (raiz / "data" / "silver"
                  / "**"
                  / "*.parquet"
                  ).as_posix()

archivo_gold = (raiz / "data" / "gold"
                / "uf_en_dolares"
                  / f"year={str(year)}"
                  / f"uf_en_dolares_{year}.parquet"
                )


def ejecuta_consulta(archivo):
    consulta = f"""WITH
                 CTE_UF AS (SELECT fecha, valor as valor_uf
                              FROM read_parquet('{archivo}')
                             WHERE indicador = 'uf'),
                 CTE_DOLAR AS (SELECT fecha, valor as valor_dolar
                                 FROM read_parquet('{archivo}')
                                WHERE indicador = 'dolar')
               SELECT UF.fecha,
                      UF.valor_uf,
                      DOL.valor_dolar,
                      ROUND(valor_uf / valor_dolar, 2) valor_uf_en_dolar
                 FROM CTE_UF UF
                    ASOF LEFT JOIN CTE_DOLAR DOL
                               ON  UF.fecha >= DOL.fecha
               ORDER BY UF.fecha
            """
    df = duckdb.sql(consulta).df()
    return df


def guardar_parquet(df, ruta):
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.date
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta, index=False)


def comprobar(ruta):
    cons = F"""SELECT *
                 FROM read_parquet('{ruta}')
                LIMIT 10
    """
    duckdb.sql(cons).show()


if __name__ == "__main__":
    df = ejecuta_consulta(archivo_silver)
    guardar_parquet(df, archivo_gold)
    comprobar(archivo_gold)
